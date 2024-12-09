import random
import poke_env.data.gen_data as gen_data
import poke_env.teambuilder.teambuilder_pokemon as poke_info

# Number of EV points to allocate
# TOTAL_EV_POINTS = 510
# print('start', gen_data.GenData(1).pokedex["ninetales"])
# pokemon_species_pool = list(pokedex.keys())  # Use all Pokémon in the Pokedex
# print('pokemon species pool', pokemon_species_pool)
pokedex = gen_data.GenData(1).pokedex
asdf = gen_data.GenData(1).load_moves("charizard")
print('asdf', asdf)
# moves = gen_data.GenData(1).moves
# print('moves', moves)
print(poke_info.TeambuilderPokemon(species="charizard").formatted_moves)

# pokemon_gen1 = [
#     "bulbasaur", "ivysaur", "venusaur", "charmander", "charmeleon", "charizard",
#     "squirtle", "wartortle", "blastoise", "caterpie", "metapod", "butterfree",
#     "weedle", "kakuna", "beedrill", "pidgey", "pidgeotto", "pidgeot",
#     "rattata", "raticate", "spearow", "fearow", "ekans", "arbok", "pikachu",
#     "raichu", "sandshrew", "sandslash", "nidoran♀", "nidorina", "nidoqueen",
#     "nidoran♂", "nidorino", "nidoking", "clefairy", "clefable", "vulpix",
#     "ninetales", "jigglypuff", "wigglytuff", "zubat", "golbat", "oddish",
#     "gloom", "vileplume", "paras", "parasect", "venonat", "venomoth",
#     "diglett", "dugtrio", "meowth", "persian", "psyduck", "golduck",
#     "mankey", "primeape", "growlithe", "arcanine", "poliwag", "poliwhirl",
#     "poliwrath", "abra", "kadabra", "alakazam", "machop", "machoke",
#     "machamp", "bellsprout", "weepinbell", "victreebel", "tentacool",
#     "tentacruel", "geodude", "graveler", "golem", "ponyta", "rapidash",
#     "slowpoke", "slowbro", "magnemite", "magneton", "farfetch’d", "doduo",
#     "dodrio", "seel", "dewgong", "grimer", "muk", "shellder", "cloyster",
#     "gastly", "haunter", "gengar", "onix", "drowzee", "hypno", "krabby",
#     "kingler", "voltorb", "electrode", "exeggcute", "exeggutor", "cubone",
#     "marowak", "hitmonlee", "hitmonchan", "lickitung", "koffing", "weezing",
#     "rhyhorn", "rhydon", "chansey", "tangela", "kangaskhan", "horsea",
#     "seadra", "goldeen", "seaking", "staryu", "starmie", "mr. mime",
#     "scyther", "jynx", "electabuzz", "magmar", "pinsir", "tauros", "magikarp",
#     "gyarados", "lapras", "ditto", "eevee", "vaporeon", "jolteon",
#     "flareon", "porygon", "omanyte", "omastar", "kabuto", "kabutops",
#     "aerodactyl", "snorlax", "articuno", "zapdos", "moltres", "dratini",
#     "dragonair", "dragonite", "mewtwo", "mew"
# ]

pokemon_no_evolution = [
    "venusaur", "charizard", "blastoise", "butterfree", "beedrill",
    "pidgeot", "raticate", "fearow", "arbok", "raichu", "sandslash",
    "nidoqueen", "nidoking", "clefable", "ninetales", "wigglytuff",
    "vileplume", "parasect", "venomoth", "dugtrio", "persian",
    "golduck", "primeape", "arcanine", "poliwrath", "alakazam",
    "machamp", "victreebel", "tentacruel", "golem", "rapidash",
    "slowbro", "magneton", "farfetch’d", "dodrio", "dewgong", "muk",
    "cloyster", "gengar", "onix", "hypno", "kingler", "electrode",
    "exeggutor", "marowak", "hitmonlee", "hitmonchan", "lickitung",
    "weezing", "rhydon", "chansey", "tangela", "kangaskhan", "seadra",
    "seaking", "starmie", "mr. mime", "scyther", "jynx", "electabuzz",
    "magmar", "pinsir", "tauros", "gyarados", "lapras", "ditto",
    "vaporeon", "jolteon", "flareon", "porygon", "omastar",
    "kabutops", "aerodactyl", "snorlax", "articuno", "zapdos",
    "moltres", "dragonite", "mewtwo", "mew"
]


    

def generate_random_pokemon():
    selected_pokemon = random.sample(pokemon_no_evolution, 6)
    print(selected_pokemon)
    for pokemon in selected_pokemon:
        print(pokedex[pokemon])
        ability = random.choice(list(pokedex[pokemon]["abilities"].values()))
        print('abiliti', pokemon, ability)

generate_random_pokemon()
# print('pokemon names', pokemon_names)


# # Generate random EV spread
# def generate_random_evs():
#     evs = [0] * 6
#     remaining_points = TOTAL_EV_POINTS
#     while remaining_points > 0:
#         stat_index = random.randint(0, 5)  # Choose a random stat
#         points = random.randint(0, min(remaining_points, 252))  # Add points (max 252 per stat)
#         evs[stat_index] += points
#         remaining_points -= points
#     return evs

# # Generate a random team of Pokémon
# def generate_random_team(pokemon_species_pool, team_size=6):
#     team = []
#     for _ in range(team_size):
#         # Choose a random Pokémon species
#         species = random.choice(pokemon_species_pool)

#         # Get Pokémon data from the POKEDEX
#         pokemon_data = pokedex[species]

#         # Randomly select an ability
#         abilities = pokemon_data.get("abilities", {})
#         ability = random.choice(list(abilities.values()))

#         # Randomly select moves
#         available_moves = [
#             move for move in moves if moves[move].get("type")  # Filter valid moves
#         ]
#         moves = random.sample(available_moves, 4)

#         # Generate random EVs
#         evs = generate_random_evs()
#         evs_string = f"EVs: {evs[0]} HP / {evs[1]} Atk / {evs[2]} Def / {evs[3]} SpA / {evs[4]} SpD / {evs[5]} Spe"

#         # Create Pokémon string
#         pokemon_string = f"""
#         {species}
#         Ability: {ability}
#         {evs_string}
#         Adamant Nature
#         - {moves[0]}
#         - {moves[1]}
#         - {moves[2]}
#         - {moves[3]}
#         """
#         team.append(pokemon_string.strip())
#     return "\n\n".join(team)

# # Define a pool of Pokémon species to choose from
# pokemon_species_pool = list(pokedex.keys())  # Use all Pokémon in the Pokedex

# # Generate a random team
# opponent_team = generate_random_team(pokemon_species_pool)
# print(opponent_team)
