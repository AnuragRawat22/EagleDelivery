import csv
import os
import matplotlib.pyplot as plt
import numpy as np

# Ensure output directory exists
os.makedirs("figures", exist_ok=True)

# Set publication style
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.labelsize": 11,
    "axes.titlesize": 12,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "figure.titlesize": 13,
    "lines.linewidth": 1.8,
    "figure.autolayout": True
})

# -------------------------------------------------------------
# Figure 1: Search Node Expansions Comparison (BFS vs A*)
# -------------------------------------------------------------
tasks = [
    "Baseline\nS->W", "Baseline\nL->D", "Baseline\nH->P",
    "Detour\nS->W", "Detour\nL->D", "Detour\nH->P",
    "Custom\nS->W"
]
bfs_expansions = [67, 79, 41, 70, 65, 41, 35]
astar_expansions = [22, 62, 16, 51, 60, 16, 11]

x = np.arange(len(tasks))
width = 0.35

fig, ax = plt.subplots(figsize=(8, 3.8), dpi=300)
rects1 = ax.bar(x - width/2, bfs_expansions, width, label="BFS (Uninformed)", color="#4682B4", edgecolor="#224466")
rects2 = ax.bar(x + width/2, astar_expansions, width, label="A* (Manhattan Heuristic)", color="#2E8B57", edgecolor="#144A29")

ax.set_ylabel("Expanded Node Count")
ax.set_title("Search Efficiency: BFS vs. A* Node Expansions Across Campus Tasks", pad=12, fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels(tasks)
ax.legend(frameon=True, facecolor="white", edgecolor="#cccccc")
ax.grid(axis="y", linestyle="--", alpha=0.5)

# Add values above bars
for rect in rects1:
    h = rect.get_height()
    ax.annotate(f"{h}", xy=(rect.get_x() + rect.get_width() / 2, h),
                xytext=(0, 2), textcoords="offset points", ha="center", va="bottom", fontsize=8)
for rect in rects2:
    h = rect.get_height()
    ax.annotate(f"{h}", xy=(rect.get_x() + rect.get_width() / 2, h),
                xytext=(0, 2), textcoords="offset points", ha="center", va="bottom", fontsize=8, fontweight="bold")

plt.savefig("figures/search_expansion_comparison.png", dpi=300)
plt.close()
print("Saved figures/search_expansion_comparison.png")

# -------------------------------------------------------------
# Figure 2: Q-Learning Training Curves (Baseline & Epsilon Study)
# -------------------------------------------------------------
def load_curve(folder):
    path = os.path.join("results", folder, "learning_curve.csv")
    with open(path) as f:
        rows = list(csv.DictReader(f))
    episodes = [int(r["episode_end"]) for r in rows]
    returns = [float(r["mean_training_return"]) for r in rows]
    success_rates = [float(r["mean_training_success_rate"]) for r in rows]
    return episodes, returns, success_rates

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.0), dpi=300)

# Subplot 1: Baseline tasks
ep_sw, ret_sw, _ = load_curve("baseline_SW")
ep_ld, ret_ld, _ = load_curve("baseline_LD")
ep_hp, ret_hp, _ = load_curve("baseline_HP")

ax1.plot(ep_sw, ret_sw, label="S -> W (Target Return = 22)", color="#1f77b4")
ax1.plot(ep_ld, ret_ld, label="L -> D (Target Return = 18)", color="#ff7f0e")
ax1.plot(ep_hp, ret_hp, label="H -> P (Target Return = 24)", color="#2ca02c")
ax1.set_xlabel("Training Episodes")
ax1.set_ylabel("Mean Training Return (100-ep block)")
ax1.set_title("(a) Baseline Campus Tasks (ε = 0.20)", pad=10, fontweight="bold")
ax1.legend(loc="lower right", frameon=True, fontsize=8)
ax1.grid(True, linestyle="--", alpha=0.5)
ax1.set_ylim(-30, 30)

# Subplot 2: Custom map epsilon comparison
ep_e005, ret_e005, _ = load_curve("custom_e005")
ep_e020, ret_e020, _ = load_curve("custom_e020")
ep_e050, ret_e050, _ = load_curve("custom_e050")

ax2.plot(ep_e005, ret_e005, label="ε = 0.05 (Low Exploration)", color="#2ca02c", linestyle="-")
ax2.plot(ep_e020, ret_e020, label="ε = 0.20 (Baseline)", color="#1f77b4", linestyle="--")
ax2.plot(ep_e050, ret_e050, label="ε = 0.50 (High Exploration)", color="#d62728", linestyle="-.")
ax2.set_xlabel("Training Episodes")
ax2.set_ylabel("Mean Training Return (100-ep block)")
ax2.set_title("(b) Custom Map S->W with Varying ε", pad=10, fontweight="bold")
ax2.legend(loc="lower right", frameon=True, fontsize=8)
ax2.grid(True, linestyle="--", alpha=0.5)
ax2.set_ylim(-25, 32)

plt.savefig("figures/q_learning_curves.png", dpi=300)
plt.close()
print("Saved figures/q_learning_curves.png")
