import asyncio
from helpers.helpers import RandomPlayer
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

async def simulate_random_battles(n_battles=5000):
    """Simulates battles between two random players."""
    total_battles = n_battles
    random_player_1_wins = 0

    for _ in range(total_battles):
        team_1 = generate_random_team()
        team_2 = generate_random_team()

        player_1 = RandomPlayer(battle_format="gen5ubers", team=team_1)
        player_2 = RandomPlayer(battle_format="gen5ubers", team=team_2)

        await player_1.battle_against(player_2, n_battles=1)

        if player_1.n_won_battles > 0:
            random_player_1_wins += 1

    win_percentage = (random_player_1_wins / total_battles) * 100
    print(f"Player 1 Win Percentage: {win_percentage:.2f}% over {total_battles} battles.")

if __name__ == "__main__":
    asyncio.run(simulate_random_battles())
