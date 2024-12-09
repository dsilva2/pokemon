import matplotlib.pyplot as plt

win_pct_over_time = {
    "SARSA vs Max-Damage": [(200, 31.5), (400, 34.75), (600, 38.83333333333333), (800, 36.375), (1000, 38.7), (1200, 39.666666666666664), (1400, 40.85714285714286), (1600, 42.5), (1800, 43.888888888888886), (2000, 44.0), (2200, 43.54545454545454), (2400, 44.29166666666667), (2600, 45.11538461538461), (2800, 45.57142857142858), (3000, 45.5), (3200, 45.65625), (3400, 46.294117647058826), (3600, 47.22222222222222), (3800, 47.3421052631579), (4000, 47.5), (4200, 48.285714285714285), (4400, 48.11363636363637), (4600, 48.52173913043478), (4800, 48.75), (5000, 48.86)],
    "SARSA vs Random": [(200, 77.0), (400, 75.5), (600, 76.66666666666667), (800, 76.25), (1000, 75.9), (1200, 75.83333333333333), (1400, 76.35714285714286), (1600, 77.5), (1800, 77.77777777777779), (2000, 78.45), (2200, 78.68181818181819), (2400, 79.08333333333334), (2600, 79.96153846153847), (2800, 80.32142857142858), (3000, 80.33333333333333), (3200, 80.6875), (3400, 80.5), (3600, 80.72222222222221), (3800, 80.26315789473685), (4000, 80.475), (4200, 80.88095238095238), (4400, 81.36363636363636), (4600, 81.69565217391305), (4800, 81.89583333333333), (5000, 82.16)],
    "Q-Learning vs Max-Damage": [(200, 21.5), (400, 23.5), (600, 23.833333333333336), (800, 22.375), (1000, 23.5), (1200, 24.25), (1400, 24.0), (1600, 24.1875), (1800, 23.333333333333332), (2000, 24.15), (2200, 23.59090909090909), (2400, 23.375), (2600, 24.0), (2800, 23.96428571428571), (3000, 24.2), (3200, 24.8125), (3400, 25.558823529411768), (3600, 26.111111111111114), (3800, 26.736842105263158), (4000, 26.525), (4200, 26.261904761904763), (4400, 26.25), (4600, 26.456521739130434), (4800, 26.895833333333336), (5000, 27.04)],
    "Q-Learning vs Random": [(200, 54.0), (400, 51.24999999999999), (600, 50.33333333333333), (800, 50.5), (1000, 50.9), (1200, 51.16666666666667), (1400, 50.78571428571429), (1600, 50.5625), (1800, 50.16666666666667), (2000, 51.1), (2200, 51.63636363636363), (2400, 52.5), (2600, 53.34615384615384), (2800, 53.46428571428572), (3000, 53.833333333333336), (3200, 54.6875), (3400, 54.61764705882353), (3600, 54.80555555555555), (3800, 55.10526315789473), (4000, 55.1), (4200, 55.52380952380952), (4400, 55.20454545454545), (4600, 55.608695652173914), (4800, 55.666666666666664), (5000, 56.02)],
}


# Plotting all comparisons on a single graph
plt.figure(figsize=(10, 6))
for label, data in win_pct_over_time.items():
    battles, win_percentages = zip(*data)
    plt.plot(battles, win_percentages, marker='o', linestyle='-', linewidth=2, label=label)

# Formatting the graph
plt.title("Win Percentage Over Time", fontsize=16)
plt.xlabel("Number of Battles", fontsize=14)
plt.ylabel("Win Percentage (%)", fontsize=14)
plt.grid(True, linestyle='--', linewidth=0.5)
# plt.legend(fontsize=12, loc="center left", bbox_to_anchor=(1, 0.5))  # Legend to the right
# plt.tight_layout(rect=[0, 0, 0.8, 1])
plt.tight_layout()
plt.show()