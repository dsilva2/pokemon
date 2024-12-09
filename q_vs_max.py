import asyncio
import random
from helpers.helpers import QLearningPlayer, OptimalPolicyPlayer, MaxDamagePlayer, save_q_table, load_q_table, q_table
from agent_team import agent_team
import matplotlib.pyplot as plt

# Define Pokémon for random team generation
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

async def train_q_learning_agent(n_battles=1000, eval_interval=200):
    total_wins = 0
    win_pct_over_time = []
    player = QLearningPlayer(battle_format="gen5ubers", team=agent_team)

    for i in range(1, n_battles + 1):
        # Generate a new random opponent team for each battle
        opponent_team = generate_random_team()
        opponent = MaxDamagePlayer(battle_format="gen5ubers", team=opponent_team)

        # Conduct a battle and track wins
        await player.battle_against(opponent, n_battles=1)
        if player.n_won_battles > total_wins:
            total_wins += 1

        # Store win percentage at intervals
        if i % eval_interval == 0:
            win_percentage = (total_wins / i) * 100
            win_pct_over_time.append((i, win_percentage))
            print(f"After {i} battles: Win percentage = {win_percentage:.2f}%")

    # Save the Q-table after training
    save_q_table(q_table, "q_vs_max.txt")
    return win_pct_over_time

async def evaluate_optimal_policy(n_battles=1000):
    # Load the trained Q-table
    q_table = load_q_table("q_vs_max.txt")

    # Create the optimal policy player
    optimal_player = OptimalPolicyPlayer(
        q_table=q_table,
        battle_format="gen5ubers",
        team=agent_team,
    )

    # Evaluate against a random opponent
    total_wins = 0
    for i in range(n_battles):
        opponent_team = generate_random_team()
        opponent = MaxDamagePlayer(battle_format="gen5ubers", team=opponent_team)
        await optimal_player.battle_against(opponent, n_battles=1)
        if optimal_player.n_won_battles > total_wins:
            total_wins += 1

    win_percentage = (total_wins / n_battles) * 100
    print(f"Optimal Policy Player's win percentage: {win_percentage:.2f}%")

async def main():
    # Train the Q-Learning agent
    print("Training Q-Learning agent...")
    win_pct_over_time = await train_q_learning_agent(n_battles=5000, eval_interval=200)
    print('win pct over time', win_pct_over_time)

    # Plot win percentage over time
    battles, win_percentages = zip(*win_pct_over_time)
    plt.figure(figsize=(10, 6))
    plt.plot(battles, win_percentages, marker='o', linestyle='-', label="Q-Learning Training")
    plt.xlabel("Number of Battles")
    plt.ylabel("Win Percentage")
    plt.title("Q-Learning: Win Percentage Over Time")
    plt.grid(True)
    plt.legend()
    plt.show()

    # Evaluate the trained Q-Learning agent
    print("Evaluating trained Q-Learning agent...")
    await evaluate_optimal_policy(n_battles=5000)

if __name__ == "__main__":
    asyncio.run(main())
