import asyncio
from helpers.helpers import OptimalPolicyPlayer, MaxDamagePlayer, RandomPlayer, load_q_table
from agent_team import agent_team
# from hardcoded_random_team import opponent_team
import random

# Define the list of Pokémon for random team generation
pokemon_list = [
    {
        "name": "Pidgeot",
        "ability": "Keen Eye",
        "moves": ["Hurricane", "Heat Wave", "U-turn", "Roost"]
    },
    {
        "name": "Sandslash",
        "ability": "Sand Veil",
        "moves": ["Earthquake", "Swords Dance", "Rock Slide", "Rapid Spin"]
    },
    {
        "name": "Alakazam",
        "ability": "Synchronize",
        "moves": ["Psychic", "Shadow Ball", "Focus Blast", "Energy Ball"]
    },
    {
        "name": "Arbok",
        "ability": "Intimidate",
        "moves": ["Gunk Shot", "Earthquake", "Crunch", "Coil"]
    },
    {
        "name": "Nidoqueen",
        "ability": "Sheer Force",
        "moves": ["Earth Power", "Sludge Bomb", "Ice Beam", "Thunderbolt"]
    },
    {
        "name": "Nidoking",
        "ability": "Sheer Force",
        "moves": ["Earth Power", "Sludge Bomb", "Thunderbolt", "Ice Beam"]
    },
    {
        "name": "Ninetales",
        "ability": "Drought",
        "moves": ["Flamethrower", "Solar Beam", "Nasty Plot", "Will-O-Wisp"]
    },
    {
        "name": "Golbat",
        "ability": "Inner Focus",
        "moves": ["Brave Bird", "Poison Fang", "Roost", "Defog"]
    },
    {
        "name": "Arcanine",
        "ability": "Intimidate",
        "moves": ["Flare Blitz", "Extreme Speed", "Wild Charge", "Morning Sun"]
    },
    {
        "name": "Poliwrath",
        "ability": "Water Absorb",
        "moves": ["Waterfall", "Ice Punch", "Brick Break", "Bulk Up"]
    },
    {
        "name": "Machamp",
        "ability": "Guts",
        "moves": ["Dynamic Punch", "Knock Off", "Ice Punch", "Bullet Punch"]
    },
    {
        "name": "Golem",
        "ability": "Sturdy",
        "moves": ["Earthquake", "Stone Edge", "Explosion", "Stealth Rock"]
    }
]

def generate_random_team():
    """Generates a random opponent team in the required format."""
    selected_pokemon = random.sample(pokemon_list, 6)
    formatted_team = ""
    for pokemon in selected_pokemon:
        formatted_team += f"{pokemon['name']}\n"
        formatted_team += f"Ability: {pokemon['ability']}\n"
        formatted_team += "EVs: 252 Atk / 4 SpD / 252 Spe\n"
        formatted_team += "Adamant Nature\n"
        for move in pokemon["moves"]:
            formatted_team += f"- {move}\n"
        formatted_team += "\n"
    return formatted_team

async def evaluate_optimal_policy():
    opponent_team = generate_random_team()
    # Load the trained Q-table
    q_table = load_q_table("q_table.txt")

    # Create the optimal policy player
    optimal_player = OptimalPolicyPlayer(
        q_table=q_table,
        battle_format="gen5ubers",
        team=agent_team,
    )

    # Create an opponent
    opponent = MaxDamagePlayer(
        battle_format="gen5ubers",
        team=opponent_team,
    )

    # Run a single battle
    num_battles = 1000
    await optimal_player.battle_against(opponent, n_battles=num_battles)
    print(f"Optimal Policy Player's win rate: {optimal_player.n_won_battles / num_battles}")

if __name__ == "__main__":
    asyncio.run(evaluate_optimal_policy())
