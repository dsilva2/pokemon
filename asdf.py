from agent_team import agent_team
from opponent_team import opponent_team
from poke_env.player import Player
from poke_env.environment import AbstractBattle
import asyncio

def calculate_and_print_damage(opponent_prev_hp, opponent_current_hp, max_hp, turn, pokemon_name):
    """
    Calculates and prints the damage done to the opponent Pokémon.
    """
    if opponent_prev_hp is not None and opponent_current_hp is not None:
        damage = opponent_prev_hp - opponent_current_hp
        damage_percentage = (damage / max_hp) * 100 if max_hp else 0
        print(
            f"Turn {turn}: Damage dealt to {pokemon_name} - "
            f"{damage} HP ({damage_percentage:.2f}%)"
        )
    else:
        print(f"Turn {turn}: Could not calculate damage (missing HP values).")


class CustomPlayer(Player):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opponent_prev_hp = None

    async def choose_move(self, battle: AbstractBattle):
        # Print the team at the start of the battle (only on the first move)
        if battle.turn == 1:
            print(f"\n{self.__class__.__name__}'s team for this battle:")
            for mon in battle.team.values():
                print(f"{mon.species} (Level {mon.level})")

        # Monitor opposing Pokémon's HP
        opposing_pokemon = battle.opponent_active_pokemon
        if opposing_pokemon:
            print(
                f"\nTurn {battle.turn}: Before move - Opposing Pokémon "
                f"({opposing_pokemon.species}) HP: {opposing_pokemon.current_hp}/{opposing_pokemon.max_hp} "
                f"({(opposing_pokemon.current_hp / opposing_pokemon.max_hp) * 100:.2f}%)"
            )

            # Calculate and print the damage done on the previous turn
            if battle.turn > 1:  # No damage to calculate on the first turn
                calculate_and_print_damage(
                    self.opponent_prev_hp,
                    opposing_pokemon.current_hp,
                    opposing_pokemon.max_hp,
                    battle.turn - 1,
                    opposing_pokemon.species,
                )

            # Store the current HP for the next turn's calculation
            self.opponent_prev_hp = opposing_pokemon.current_hp

        # Choose a random move for simplicity
        move = self.choose_random_move(battle)
        print(f"{self.__class__.__name__} selected move: {move.order}")
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


# Run the script
if __name__ == "__main__":
    asyncio.run(main())
