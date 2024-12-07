import asyncio
from helpers.helpers import QLearningPlayer, MaxDamagePlayer, save_q_table, q_table
from agent_team import agent_team
from opponent_team import opponent_team

async def train_q_learning_agent(n_battles=1000):
    for i in range(n_battles):
        # print(f"Starting battle {i+1}")
        player = QLearningPlayer(battle_format="gen5ubers", team=agent_team)
        opponent = MaxDamagePlayer(battle_format="gen5ubers", team=opponent_team)
        await player.battle_against(opponent, n_battles=1)
        # if i % 100 == 0:
        #     print(f"Battle {i+1} complete")

    # Save Q-table after training
    save_q_table(q_table, "q_table.txt")

if __name__ == "__main__":
    asyncio.run(train_q_learning_agent(n_battles=5000))
