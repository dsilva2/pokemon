import asyncio
from helpers.helpers import OptimalPolicyPlayer, MaxDamagePlayer, RandomPlayer, load_q_table
from agent_team import agent_team
from opponent_team import opponent_team

async def evaluate_optimal_policy():
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
    await optimal_player.battle_against(opponent, n_battles=100)
    print(f"Optimal Policy Player's win rate: {optimal_player.n_won_battles}")

if __name__ == "__main__":
    asyncio.run(evaluate_optimal_policy())
