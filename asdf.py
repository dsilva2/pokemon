from agent_team import agent_team
from opponent_team import opponent_team
from poke_env.player import Player
from poke_env.environment import AbstractBattle
import asyncio

class CustomPlayer(Player):
    async def choose_move(self, battle: AbstractBattle):
        # Print the team at the start of the battle (only on the first move)
        if battle.turn == 1:
            max_damage_pokemon, agent_pokemon = battle.all_active_pokemons
            print('all active',  battle.all_active_pokemons)
            print('hello')
            # my_pokemon = battle.all_active_pokemons[1]
            # max_damage_pokemon = battle.all_active_pokemons[1]
            print('my pokemon', agent_pokemon, 'other pokemon', max_damage_pokemon)
            print('my pokemon hp', agent_pokemon.current_hp, 'other hp', max_damage_pokemon.current_hp)
            print(f"\n{self.__class__.__name__}'s team for this battle:")
            for mon in battle.team.values():
                print(f"{mon.species} (Level {mon.level})")

        # Choose a random move for simplicity
        move = self.choose_random_move(battle)
        print(f'Agent move: {move.order}')
        return move
print('agent team', agent_team)
class MaxDamagePlayer(Player):
    def choose_move(self, battle):
        # Chooses a move with the highest base power when possible
        if battle.available_moves:
            # Iterating over available moves to find the one with the highest base power
            best_move = max(battle.available_moves, key=lambda move: move.base_power)
            # print(f"Opponent selected move: {best_move}")
            # print('battle all active pokemon', battle.all_active_pokemons)
            # max_damage_pokemon, agent_pokemon = battle.all_active_pokemons
            # # my_pokemon = battle.all_active_pokemons[1]
            # # max_damage_pokemon = battle.all_active_pokemons[1]
            # print('my pokemon', agent_pokemon, 'other pokemon', max_damage_pokemon)
            # print('my pokemon hp', agent_pokemon.current_hp, 'other hp', max_damage_pokemon.current_hp)

            # remaining_hp = battle.all_active_pokemons[1].current_hp if battle.all_active_pokemons else ""
            # print('battle', remaining_hp) 
            # Creating an order for the selected move
            return self.create_order(best_move)
        else:
            # If no attacking move is available, perform a random switch
            # This involves choosing a random move, which could be a switch or another available action
            return self.choose_random_move(battle)

# Create two custom players with imported custom teams
player1 = CustomPlayer(
    # username="UniqueCustomPlayer1",
    battle_format="gen5ubers",
    team=agent_team,
)

player2 = MaxDamagePlayer(
    # username="UniqueMaxDamagePlayer1",
    battle_format="gen5ubers",
    team=opponent_team,
)
print('player creeated', player1)

# Function to start a battle between the two players
async def main():
    # Run a series of battles
    await player1.battle_against(player2, n_battles=1)
    print(f"\nPlayer 1's win rate: {player1.n_won_battles}")

# Run the script
if __name__ == "__main__":
    asyncio.run(main())
