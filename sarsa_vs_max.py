import asyncio
import random
from helpers.helpers import QLearningPlayer, MaxDamagePlayer, RandomPlayer, save_q_table, q_table, SarsaPlayer
from agent_team import agent_team

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

async def train_sarsa_agent_with_win_tracking(n_battles=1000, eval_interval=200):
    total_wins = 0

    player = SarsaPlayer(battle_format="gen5ubers", team=agent_team)
    for i in range(1, n_battles + 1):
        # Generate a new random opponent team for each battle
        opponent_team = generate_random_team()
        opponent = MaxDamagePlayer(battle_format="gen5ubers", team=opponent_team)

        # Conduct a battle and track wins
        await player.battle_against(opponent, n_battles=1)
        if player.n_won_battles > total_wins:  # Increment wins if player wins
            total_wins += 1

        # Print win percentage at intervals
        if i % eval_interval == 0:
            win_percentage = (total_wins / i) * 100
            print(f"After {i} battles: Win percentage = {win_percentage:.2f}%")

if __name__ == "__main__":
    asyncio.run(train_sarsa_agent_with_win_tracking(n_battles=5000))
