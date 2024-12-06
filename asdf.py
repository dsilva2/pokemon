from agent_team import agent_team
from opponent_team import opponent_team
from poke_env.player import Player
from poke_env.environment import AbstractBattle
import asyncio


class CustomPlayer(Player):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opponent_prev_hp = None
        self.battle_log = []  # To store the battle events
        self.last_move_used = None  # Track the last move used

    async def choose_move(self, battle: AbstractBattle):
        # Print the team at the start of the battle (only on the first move)
        if battle.turn == 1:
            print(f"\n{self.__class__.__name__}'s team for this battle:")
            for mon in battle.team.values():
                print(f"{mon.species} (Level {mon.level})")

        # Monitor opposing Pokémon's HP
        opposing_pokemon = battle.opponent_active_pokemon
        my_pokemon = battle.active_pokemon
        if opposing_pokemon:
            print(
                f"\nTurn {battle.turn}: Before move - Opposing Pokémon "
                f"({opposing_pokemon.species}) HP: {opposing_pokemon.current_hp}/{opposing_pokemon.max_hp} "
                f"({(opposing_pokemon.current_hp / opposing_pokemon.max_hp) * 100:.2f}%)"
            )

            # Log the damage done on the previous turn
            if battle.turn > 1 and self.opponent_prev_hp is not None:
                damage = self.opponent_prev_hp - opposing_pokemon.current_hp
                damage_percentage = (damage / opposing_pokemon.max_hp) * 100 if opposing_pokemon.max_hp else 0

                # Append the event to the battle log
                self.battle_log.append({
                    "turn": battle.turn - 1,
                    "attacking_pokemon": my_pokemon.species if my_pokemon else "Unknown",
                    "move_used": self.last_move_used if self.last_move_used else "Unknown",
                    "opposing_pokemon": opposing_pokemon.species,
                    "damage": damage,
                    "damage_percentage": round(damage_percentage, 2),
                })

                # print(
                #     f"Turn {battle.turn - 1}: {my_pokemon.species} used {self.last_move_used} on {opposing_pokemon.species} - "
                #     f"{damage} HP ({damage_percentage:.2f}%) damage dealt."
                # )

            # Store the current HP for the next turn's calculation
            self.opponent_prev_hp = opposing_pokemon.current_hp

        # Choose a random move
        move = self.choose_random_move(battle)
        # print('move\n\n\n\n\n\n\n\n\n', move.vars())
        # for value in vars(move.order).items():
        #     print(f"\n\n\n\n\n\n\n\n\n{value}")
        print("move order", move.order, type(move.order), move.order)
        self.last_move_used = move.order if move.order else "Struggle"  # Track the last move used
        print(f"{self.__class__.__name__} selected move: {self.last_move_used}")
        return move


class MaxDamagePlayer(Player):
    def choose_move(self, battle):
        # Chooses a move with the highest base power when possible
        if battle.available_moves:
            best_move = max(battle.available_moves, key=lambda move: move.base_power)
            return self.create_order(best_move)
        else:
            # If no attacking move is available, perform a random switch
            return self.choose_random_move(battle)


# Create two players
player1 = CustomPlayer(
    battle_format="gen5ubers",
    team=agent_team,
)

player2 = MaxDamagePlayer(
    battle_format="gen5ubers",
    team=opponent_team,
)

# Function to start the battle
async def main():
    await player1.battle_against(player2, n_battles=1)
    print(f"\nPlayer 1's win rate: {player1.n_won_battles}")
    print("\nBattle Log:")
    for event in player1.battle_log:
        print(event)


# Run the script
if __name__ == "__main__":
    asyncio.run(main())
