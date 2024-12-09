import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Baseline win percentages for a Random Agent
baseline_vs_random = 50.0  # Baseline win percentage for Random Opponent
baseline_vs_max_damage = 10.0  # Baseline win percentage for Max-Damage Opponent

# Actual win percentages for Q-Learning and SARSA against Random and Max-Damage players
win_percentages = {
    "Q-Learning vs Random": 56.02,
    "Q-Learning vs Max-Damage": 27.04,
    "SARSA vs Random": 82.16,
    "SARSA vs Max-Damage": 48.86,
}

# Calculate improvements over the baselines
data = np.array([
    [win_percentages["Q-Learning vs Random"] - baseline_vs_random, win_percentages["Q-Learning vs Max-Damage"] - baseline_vs_max_damage],
    [win_percentages["SARSA vs Random"] - baseline_vs_random, win_percentages["SARSA vs Max-Damage"] - baseline_vs_max_damage]
])

# Labels for rows (players) and columns (opponents)
rows = ["Q-Learning", "SARSA"]
cols = ["Random Opponent", "Max-Damage Opponent"]

# Create a DataFrame for the heatmap
df = pd.DataFrame(data, index=rows, columns=cols)

# Create the heatmap
plt.figure(figsize=(8, 6))
heatmap = sns.heatmap(
    df, annot=True, cmap='RdYlGn', center=0, fmt='.2f',
    cbar_kws={'label': 'Improvement over Random Agent Win (%)'},
    annot_kws={"size": 14, "weight": "bold"}  # Set font size and weight for annotations
)

# Add labels and title
plt.title("Performance Improvement of Q-Learning and SARSA")
plt.xlabel("Opponent Strategy")
plt.ylabel("Agent Strategy")

# Show the heatmap
plt.tight_layout()
plt.show()
