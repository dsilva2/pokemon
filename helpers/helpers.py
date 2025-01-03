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

# Type effectiveness chart
# Full Pokémon type effectiveness chart
# type_effectiveness = {
#     "Normal": {
#         "Rock": 0.5, "Ghost": 0, "Steel": 0.5
#     },
#     "Fire": {
#         "Grass": 2, "Ice": 2, "Bug": 2, "Steel": 2,
#         "Fire": 0.5, "Water": 0.5, "Rock": 0.5, "Dragon": 0.5
#     },
#     "Water": {
#         "Fire": 2, "Ground": 2, "Rock": 2,
#         "Water": 0.5, "Grass": 0.5, "Dragon": 0.5
#     },
#     "Electric": {
#         "Water": 2, "Flying": 2,
#         "Electric": 0.5, "Grass": 0.5, "Ground": 0
#     },
#     "Grass": {
#         "Water": 2, "Ground": 2, "Rock": 2,
#         "Fire": 0.5, "Grass": 0.5, "Poison": 0.5, "Flying": 0.5, "Bug": 0.5, "Dragon": 0.5, "Steel": 0.5
#     },
#     "Ice": {
#         "Grass": 2, "Ground": 2, "Flying": 2, "Dragon": 2,
#         "Fire": 0.5, "Water": 0.5, "Ice": 0.5, "Steel": 0.5
#     },
#     "Fighting": {
#         "Normal": 2, "Ice": 2, "Rock": 2, "Dark": 2, "Steel": 2,
#         "Poison": 0.5, "Flying": 0.5, "Psychic": 0.5, "Bug": 0.5, "Fairy": 0.5, "Ghost": 0
#     },
#     "Poison": {
#         "Grass": 2, "Fairy": 2,
#         "Poison": 0.5, "Ground": 0.5, "Rock": 0.5, "Ghost": 0.5, "Steel": 0
#     },
#     "Ground": {
#         "Fire": 2, "Electric": 2, "Poison": 2, "Rock": 2, "Steel": 2,
#         "Grass": 0.5, "Bug": 0.5, "Flying": 0
#     },
#     "Flying": {
#         "Grass": 2, "Fighting": 2, "Bug": 2,
#         "Electric": 0.5, "Rock": 0.5, "Steel": 0.5
#     },
#     "Psychic": {
#         "Fighting": 2, "Poison": 2,
#         "Psychic": 0.5, "Steel": 0.5, "Dark": 0
#     },
#     "Bug": {
#         "Grass": 2, "Psychic": 2, "Dark": 2,
#         "Fire": 0.5, "Fighting": 0.5, "Poison": 0.5, "Flying": 0.5, "Ghost": 0.5, "Steel": 0.5, "Fairy": 0.5
#     },
#     "Rock": {
#         "Fire": 2, "Ice": 2, "Flying": 2, "Bug": 2,
#         "Fighting": 0.5, "Ground": 0.5, "Steel": 0.5
#     },
#     "Ghost": {
#         "Psychic": 2, "Ghost": 2,
#         "Dark": 0.5, "Normal": 0
#     },
#     "Dragon": {
#         "Dragon": 2,
#         "Steel": 0.5, "Fairy": 0
#     },
#     "Dark": {
#         "Psychic": 2, "Ghost": 2,
#         "Fighting": 0.5, "Dark": 0.5, "Fairy": 0.5
#     },
#     "Steel": {
#         "Ice": 2, "Rock": 2, "Fairy": 2,
#         "Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Steel": 0.5
#     },
#     "Fairy": {
#         "Fighting": 2, "Dragon": 2, "Dark": 2,
#         "Fire": 0.5, "Poison": 0.5, "Steel": 0.5
#     },
# }


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


def choose_action(state, action_space, battle):
    """Choose an action using ε-greedy policy, considering type effectiveness."""
    if random.uniform(0, 1) < epsilon:  # Exploration
        return random.choice(action_space)
    else:  # Exploitation
        # Get Q-values adjusted by type effectiveness
        q_values = []
        for action in action_space:
            if action[0] == "move":
                move = next(m for m in battle.available_moves if m.id == action[1])
                active_type = move.type
                opponent_type = battle.opponent_active_pokemon.types[0] if battle.opponent_active_pokemon else "None"
            #     type_multiplier = type_effectiveness.get(active_type, {}).get(opponent_type, 1)
            # else:
            #     type_multiplier = 1  # No multiplier for switches

            q_value = q_table.get((state, action), default_q_value)
            q_values.append((action, q_value))

        # Select action with the highest adjusted Q-value
        return max(q_values, key=lambda x: x[1])[0]


def update_q_table(state, action, reward, next_state, next_action_space):
    """Update the Q-table using the Q-learning formula."""
    max_future_q = max(q_table.get((next_state, a), default_q_value) for a in next_action_space)
    current_q = q_table.get((state, action), default_q_value)
    q_table[(state, action)] = current_q + alpha * (reward + gamma * max_future_q - current_q)


def calculate_reward(my_hp_before, my_hp_after, opponent_hp_before, opponent_hp_after, battle):
    """
    Calculate the reward based on the reward structure:
    - Winning: +100
    - Losing: -100
    - Opponent Pokémon fainted: +10
    - % HP damage to opponent: +% (of HP lost)
    - % HP damage to self: -% (of HP lost)
    """

    type_effectiveness = {
    "NORMAL": {"ROCK": 0.5, "GHOST": 0, "STEEL": 0.5},
    "FIRE": {"GRASS": 2, "ICE": 2, "BUG": 2, "STEEL": 2, "FIRE": 0.5, "WATER": 0.5, "ROCK": 0.5, "DRAGON": 0.5},
    "WATER": {"FIRE": 2, "GROUND": 2, "ROCK": 2, "WATER": 0.5, "GRASS": 0.5, "DRAGON": 0.5},
    "ELECTRIC": {"WATER": 2, "FLYING": 2, "ELECTRIC": 0.5, "GRASS": 0.5, "GROUND": 0},
    "GRASS": {"WATER": 2, "GROUND": 2, "ROCK": 2, "FIRE": 0.5, "GRASS": 0.5, "POISON": 0.5, "FLYING": 0.5, "BUG": 0.5, "DRAGON": 0.5, "STEEL": 0.5},
    "ICE": {"GRASS": 2, "GROUND": 2, "FLYING": 2, "DRAGON": 2, "FIRE": 0.5, "WATER": 0.5, "ICE": 0.5, "STEEL": 0.5},
    "FIGHTING": {"NORMAL": 2, "ICE": 2, "ROCK": 2, "DARK": 2, "STEEL": 2, "POISON": 0.5, "FLYING": 0.5, "PSYCHIC": 0.5, "BUG": 0.5, "FAIRY": 0.5, "GHOST": 0},
    "POISON": {"GRASS": 2, "FAIRY": 2, "POISON": 0.5, "GROUND": 0.5, "ROCK": 0.5, "GHOST": 0.5, "STEEL": 0},
    "GROUND": {"FIRE": 2, "ELECTRIC": 2, "POISON": 2, "ROCK": 2, "STEEL": 2, "GRASS": 0.5, "BUG": 0.5, "FLYING": 0},
    "FLYING": {"GRASS": 2, "FIGHTING": 2, "BUG": 2, "ELECTRIC": 0.5, "ROCK": 0.5, "STEEL": 0.5},
    "PSYCHIC": {"FIGHTING": 2, "POISON": 2, "PSYCHIC": 0.5, "STEEL": 0.5, "DARK": 0},
    "BUG": {"GRASS": 2, "PSYCHIC": 2, "DARK": 2, "FIRE": 0.5, "FIGHTING": 0.5, "POISON": 0.5, "FLYING": 0.5, "GHOST": 0.5, "STEEL": 0.5, "FAIRY": 0.5},
    "ROCK": {"FIRE": 2, "ICE": 2, "FLYING": 2, "BUG": 2, "FIGHTING": 0.5, "GROUND": 0.5, "STEEL": 0.5},
    "GHOST": {"PSYCHIC": 2, "GHOST": 2, "DARK": 0.5, "NORMAL": 0},
    "DRAGON": {"DRAGON": 2, "STEEL": 0.5, "FAIRY": 0},
    "DARK": {"PSYCHIC": 2, "GHOST": 2, "FIGHTING": 0.5, "DARK": 0.5, "FAIRY": 0.5},
    "STEEL": {"ICE": 2, "ROCK": 2, "FAIRY": 2, "FIRE": 0.5, "WATER": 0.5, "ELECTRIC": 0.5, "STEEL": 0.5},
    "FAIRY": {"FIGHTING": 2, "DRAGON": 2, "DARK": 2, "FIRE": 0.5, "POISON": 0.5, "STEEL": 0.5},
}

    # 1. Winning or Losing
    if battle.won:
        return 100  # Winning
    elif battle.lost:
        return -100  # Losing

    # 2. HP Percentage Change
    opponent_hp_lost = opponent_hp_before - opponent_hp_after
    opponent_max_hp = battle.opponent_active_pokemon.max_hp
    opponent_hp_loss_percentage = (opponent_hp_lost / opponent_max_hp) * 10 if opponent_max_hp else 0

    my_hp_lost = my_hp_before - my_hp_after
    my_max_hp = battle.active_pokemon.max_hp
    my_hp_loss_percentage = (my_hp_lost / my_max_hp) * 10 if my_max_hp else 0

    # 3. Fainting
    opponent_fainted_reward = 50 if opponent_hp_after == 0 else 0

    # 4. Own pokemon fainting
    my_fainted_reward = -50 if my_hp_after == 0 else 0

    


    # Type effectiveness multiplier
    active_type = battle.active_pokemon.types[0].name if battle.active_pokemon else "None"
    opponent_type = battle.opponent_active_pokemon.types[0].name if battle.opponent_active_pokemon else "None"
    type_multiplier = type_effectiveness.get(active_type, {}).get(opponent_type, 1)
    

    # Reward based on type effectiveness
    type_effectiveness_bonus = (type_multiplier - 1) * 5
    # type_multiplier = type_effectiveness.get(active_type, {}).get(opponent_type, 1)

    # type_effectiveness_bonus = 0



    reward = (opponent_hp_loss_percentage -  # Positive reward for damage dealt
        my_hp_loss_percentage +  # Negative penalty for damage received
        opponent_fainted_reward +   # Bonus for fainting opponent
        my_fainted_reward)
    
    if opponent_hp_before == opponent_hp_after and my_hp_before == my_hp_after:
        reward -= 5  # Penalize stalling or ineffective moves
    

    # Total reward
    return (
        opponent_hp_loss_percentage -  # Positive reward for damage dealt
        my_hp_loss_percentage +  # Negative penalty for damage received
        opponent_fainted_reward +   # Bonus for fainting opponent
        my_fainted_reward +
        type_effectiveness_bonus  # Bonus for type effectiveness
    )


class QLearningPlayer(Player):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_state = None
        self.last_action = None
        self.opponent_prev_hp = None
        self.my_prev_hp = None
        self.num_switches = 0  # Tracks if the last action was a switch

    def get_state(self, battle):
        """Create a representation of the current battle state."""
        active_type = battle.active_pokemon.types[0] if battle.active_pokemon else "None"
        opponent_type = battle.opponent_active_pokemon.types[0] if battle.opponent_active_pokemon else "None"
        return (
            battle.active_pokemon.species,
            battle.opponent_active_pokemon.species,
        )

    async def choose_move(self, battle):
        """Choose a move based on Q-learning."""
        # Get the current state
        state = self.get_state(battle)

        # Get the action space
        action_space = get_action_space(battle)

        # Filter out switch actions if the last action was also a switch
        if self.num_switches > 2:
            old_action_space = action_space
            action_space = [action for action in action_space if action[0] != "switch"]
            # print(len(action_space), action_space, "\n\n\n\n\n\n\n\n\n\n")
            # action_space = action_space if len(action_space) > 0 else old_action_space

        # Fallback: If action_space is empty, repopulate it and reset last_was_switch
        if not action_space:
            action_space = get_action_space(battle)
            self.last_was_switch = False  # Allow switching again as a fallback

        # Choose an action using ε-greedy policy
        action = choose_action(state, action_space, battle)

        # Translate the action to an order
        if action[0] == "move":
            move = next(m for m in battle.available_moves if m.id == action[1])
            move_order = self.create_order(move)
            self.last_was_switch = False  # Reset switch tracking
            self.num_switches = 0
        elif action[0] == "switch":
            switch = next(p for p in battle.available_switches if p.species == action[1])
            move_order = self.create_order(switch)
            self.num_switches += 1 # Update switch tracking

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
        self.num_switches = 0  # Tracks if the last action was a switch


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
        if self.num_switches > 1:
            old_action_space = action_space
            action_space = [action for action in action_space if action[0] != "switch"]
            # print(len(action_space), action_space, "\n\n\n\n\n\n\n\n\n\n")
            # action_space = action_space if len(action_space) > 0 else old_action_space

        # Fallback: If action_space is empty, repopulate it and reset last_was_switch
        if not action_space:
            action_space = get_action_space(battle)
            self.last_was_switch = False
        # print('action space', action_space)
        # for ac in action_space:
        #     print(ac, self.q_table.get((state, ac), default_q_value))
        action = max(action_space, key=lambda a: self.q_table.get((state, a), default_q_value))
        # print('action', action, 'state', state)
        # print('state', state, '\n action', action)

        if action[0] == "move":
            move = next(m for m in battle.available_moves if m.id == action[1])
            move_order = self.create_order(move)
            self.num_switches = 0
        elif action[0] == "switch":
            switch = next(p for p in battle.available_switches if p.species == action[1])
            move_order = self.create_order(switch)
            self.num_switches += 1

        return move_order

class SarsaPlayer(Player):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_state = None
        self.last_action = None
        self.opponent_prev_hp = None
        self.my_prev_hp = None
        self.q_table = {}  # Q-table to store state-action pairs
        self.default_q_value = 0
        self.alpha = 0.1  # Learning rate
        self.gamma = 0.9  # Discount factor
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_decay = 0.995
        self.min_epsilon = 0.1
        self.last_was_switch = False

    def get_state(self, battle):
        """Get the current state representation."""
        active_type = battle.active_pokemon.types[0] if battle.active_pokemon else "None"
        opponent_type = battle.opponent_active_pokemon.types[0] if battle.opponent_active_pokemon else "None"
        return (
            battle.active_pokemon.species,
            battle.opponent_active_pokemon.species,
        )

    def get_action_space(self, battle):
        """Get all possible actions for the current state."""
        actions = []
        if battle.available_moves:
            actions.extend(("move", move.id) for move in battle.available_moves)
        if battle.available_switches:
            actions.extend(("switch", pokemon.species) for pokemon in battle.available_switches)
        return actions

    def choose_action(self, state, action_space):
        """Choose an action using ε-greedy policy."""
        if random.uniform(0, 1) < self.epsilon:  # Exploration
            return random.choice(action_space)
        else:  # Exploitation
            q_values = [(action, self.q_table.get((state, action), self.default_q_value)) for action in action_space]
            return max(q_values, key=lambda x: x[1])[0]

    async def choose_move(self, battle):
        """Choose a move based on SARSA."""
        # Get the current state
        state = self.get_state(battle)
        action_space = self.get_action_space(battle)

        # Get the action space
        if self.last_was_switch:
            action_space = [action for action in action_space if action[0] != "switch"]

        # If no valid actions remain, reset to allow any action
        if not action_space:
            action_space = self.get_action_space(battle)
        # Choose the current action
        action = self.choose_action(state, action_space)

        # Translate the action to an order
        if action[0] == "move":
            move = next(m for m in battle.available_moves if m.id == action[1])
            move_order = self.create_order(move)
            self.last_was_switch = False
        elif action[0] == "switch":
            switch = next(p for p in battle.available_switches if p.species == action[1])
            move_order = self.create_order(switch)
            self.last_was_switch = True

        # Update the Q-table if this is not the first move
        if self.last_state is not None and self.last_action is not None:
            # Calculate the reward
            reward = calculate_reward(
                self.my_prev_hp,
                battle.active_pokemon.current_hp,
                self.opponent_prev_hp,
                battle.opponent_active_pokemon.current_hp,
                battle,
            )

            # Get the next state and next action
            next_state = state
            next_action = self.choose_action(next_state, action_space)

            # SARSA update rule
            current_q = self.q_table.get((self.last_state, self.last_action), self.default_q_value)
            next_q = self.q_table.get((next_state, next_action), self.default_q_value)
            self.q_table[(self.last_state, self.last_action)] = current_q + self.alpha * (
                reward + self.gamma * next_q - current_q
            )

        # Save the current state and action for the next turn
        self.last_state = state
        self.last_action = action
        self.opponent_prev_hp = battle.opponent_active_pokemon.current_hp
        self.my_prev_hp = battle.active_pokemon.current_hp
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

        return move_order
