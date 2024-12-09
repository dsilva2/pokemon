import random

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
        "moves": ["Waterfall", "Ice Punch", "Close Combat", "Bulk Up"]
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

opponent_team = generate_random_team()
print(opponent_team)
