import random
import numpy as np
from poke_env.player import Player

# Q-table to store state-action pairs and their values
q_table = {}
default_q_value = 0  # Default Q-value for unseen state-action pairs

# Q-Learning Parameters
alpha = 0.1  # Learning rate
gamma = 0.9  # Discount factor
epsilon = 0.1  # Exploration rate


def save_q_table(q_table, file_path="q_table.txt"):
    """Save the Q-table to a file."""
    with open(file_path, "w") as f:
        for key, value in q_table.items():
            f.write(f"{key}: {value}\n")


def load_q_table(file_path="q_table.txt"):
    """Load the Q-table from a file."""
    q_table = {}
    with open(file_path, "r") as f:
        for line in f:
            key, value = line.strip().split(":")
            q_table[eval(key)] = float(value)
    return q_table


def get_action_space(battle):
    """Get all possible actions for the current state."""
    actions = []
    if battle.available_moves:
        actions.extend(("move", move.id) for move in battle.available_moves)
    if battle.available_switches:
        actions.extend(("switch", pokemon.species) for pokemon in battle.available_switches)
    return actions


def choose_action(state, action_space):
    """Choose an action using ε-greedy policy."""
    if random.uniform(0, 1) < epsilon:  # Exploration
        return random.choice(action_space)
    else:  # Exploitation
        return max(action_space, key=lambda a: q_table.get((state, a), default_q_value))


def update_q_table(state, action, reward, next_state, next_action_space):
    """Update the Q-table using the Q-learning formula."""
    max_future_q = max(q_table.get((next_state, a), default_q_value) for a in next_action_space)
    current_q = q_table.get((state, action), default_q_value)
    q_table[(state, action)] = current_q + alpha * (reward + gamma * max_future_q - current_q)


def calculate_reward(my_hp_before, my_hp_after, opponent_hp_before, opponent_hp_after, battle):
    """
    Calculate the reward based on the reward structure:
    - Winning: +30
    - Losing: -30
    - Opponent Pokémon fainted: +1
    - % HP damage to opponent: +% (of HP lost)
    - % HP damage to self: -% (of HP lost)
    """
    # 1. Winning or Losing
    if battle.won:
        return 30  # Winning
    elif battle.lost:
        return -30  # Losing

    # 2. HP Percentage Change
    opponent_hp_lost = opponent_hp_before - opponent_hp_after
    opponent_max_hp = battle.opponent_active_pokemon.max_hp
    opponent_hp_loss_percentage = (opponent_hp_lost / opponent_max_hp) * 10 if opponent_max_hp else 0

    my_hp_lost = my_hp_before - my_hp_after
    my_max_hp = battle.active_pokemon.max_hp
    my_hp_loss_percentage = (my_hp_lost / my_max_hp) * 10 if my_max_hp else 0

    # 3. Fainting
    opponent_fainted_reward = 10 if opponent_hp_after == 0 else 0
    my_fainted_penalty = -10 if my_hp_after == 0 else 0

    # print('oppononent fainted', opponent_fainted_reward, my_fainted_penalty, opponent_hp_loss_percentage, my_hp_loss_percentage)

    # Calculate total reward
    reward = (
        opponent_fainted_reward +  # Opponent Pokémon fainted
        -my_fainted_penalty +  # Self fainted penalty
        opponent_hp_loss_percentage -  # Positive reward for % damage to opponent
        my_hp_loss_percentage  # Negative penalty for % damage to self
    )

    return reward



class QLearningPlayer(Player):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_state = None
        self.last_action = None
        self.opponent_prev_hp = None
        self.my_prev_hp = None

    def get_state(self, battle):
        """Create a representation of the current battle state."""
        return (
            battle.active_pokemon.species,
            # battle.active_pokemon.current_hp,
            battle.opponent_active_pokemon.species,
            # battle.opponent_active_pokemon.current_hp,
        )

    async def choose_move(self, battle):
        """Choose a move based on Q-learning."""
        # Get the current state
        state = self.get_state(battle)

        # Get the action space
        action_space = get_action_space(battle)

        # Choose an action using ε-greedy policy
        action = choose_action(state, action_space)

        # Translate the action to an order
        if action[0] == "move":
            move = next(m for m in battle.available_moves if m.id == action[1])
            move_order = self.create_order(move)
        elif action[0] == "switch":
            switch = next(p for p in battle.available_switches if p.species == action[1])
            move_order = self.create_order(switch)

        # Update the Q-table if this is not the first move
        if self.last_state and self.last_action:
            reward = calculate_reward(
                self.my_prev_hp,
                battle.active_pokemon.current_hp,
                self.opponent_prev_hp,
                battle.opponent_active_pokemon.current_hp,
                battle,
            )
            update_q_table(self.last_state, self.last_action, reward, state, action_space)

        # Save the current state and action for the next turn
        self.last_state = state
        self.last_action = action
        self.opponent_prev_hp = battle.opponent_active_pokemon.current_hp
        self.my_prev_hp = battle.active_pokemon.current_hp

        return move_order

    
class MaxDamagePlayer(Player):
    def choose_move(self, battle):
        # Chooses a move with the highest base power when possible
        if battle.available_moves:
            best_move = max(battle.available_moves, key=lambda move: move.base_power)
            return self.create_order(best_move)
        else:
            # If no attacking move is available, perform a random switch
            return self.choose_random_move(battle)

class RandomPlayer(Player):
    def choose_move(self, battle):
        # Chooses a move with the highest base power when possible
        return self.choose_random_move(battle)


class OptimalPolicyPlayer(Player):
    def __init__(self, q_table, **kwargs):
        super().__init__(**kwargs)
        self.q_table = q_table

    def get_state(self, battle):
        """Create a representation of the current battle state."""
        return (
            battle.active_pokemon.species,
            # battle.active_pokemon.current_hp,
            battle.opponent_active_pokemon.species,
            # battle.opponent_active_pokemon.current_hp,
        )

    async def choose_move(self, battle):
        """Choose a move based on the optimal policy."""
        state = self.get_state(battle)
        action_space = get_action_space(battle)
        # print('action space', action_space)
        # for ac in action_space:
        #     print(ac, self.q_table.get((state, ac), default_q_value))
        action = max(action_space, key=lambda a: self.q_table.get((state, a), default_q_value))
        # print('action', action, 'state', state)
        # print('state', state, '\n action', action)

        if action[0] == "move":
            move = next(m for m in battle.available_moves if m.id == action[1])
            move_order = self.create_order(move)
        elif action[0] == "switch":
            switch = next(p for p in battle.available_switches if p.species == action[1])
            move_order = self.create_order(switch)

        return move_order
