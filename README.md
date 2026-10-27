# Eagle Delivery: Campus Autonomous Navigation

**Course:** COSC 461/561 — Artificial Intelligence  
**Institution:** Eastern Michigan University (EMU)  
**Author:** Anurag Singh Rawat  
**Repository Name:** EagleDelivery  

---

## Project Overview

**Eagle Delivery** is an autonomous campus delivery robot simulation designed for Eastern Michigan University. The robot operates on discrete 2D grid campus layouts with building entrances, walkable pathways, and impassable obstacles. The mission is to navigate from a pickup entrance to a designated delivery destination while avoiding obstacles and minimizing total delivery steps.

The project explores two foundational paradigms in Artificial Intelligence:
1. **Classical Heuristic Search (Part A):**
   - Uninformed search using **Breadth-First Search (BFS)**.
   - Informed heuristic search using **A\* Graph Search** guided by the **Manhattan Distance heuristic** ($L_1$ norm) with deterministic tie-breaking via insertion order.
2. **Reinforcement Learning (Part B & C):**
   - Model-free tabular **Q-Learning** with $\epsilon$-greedy exploration to learn optimal navigation policies without access to transition dynamics or prior map layouts.
   - Empirical investigation into the effect of exploration probability ($\epsilon$) on learning dynamics, convergence rates, and final policy quality.

---

## Environment & Problem Formulation

- **State Space ($S$):** Grid coordinates $(r, c)$ corresponding to traversable corridors and campus building entrances:
  - `S`: Student Center
  - `L`: Halle Library
  - `H`: Pray-Harrold
  - `D`: Downing Hall
  - `P`: Putnam Hall
  - `W`: Walton Hall
  - `.`: Traversable walkway
  - `#`: Impassable building/wall
- **Action Space ($A$):** 4 discrete cardinal directions: `UP`, `DOWN`, `LEFT`, `RIGHT`. Diagonal movement is prohibited.
- **Transition Dynamics ($T$):** Deterministic movement by default. Collisions with boundaries or obstacles leave the robot in place.
- **Reward Function ($R$):**
  - Step penalty: $r = -1$ for each attempted action.
  - Goal arrival bonus: $+40$ upon reaching the selected destination ($r = 39$ on the terminal step).
  - Terminal condition: Episode terminates immediately upon reaching the destination, yielding an undiscounted return of $40 - L$, where $L$ is the number of steps taken.

---

## Project Structure

```text
eagle_delivery/
├── agents.py                 # Core implementations: BFS, A*, epsilon_greedy, q_learning_update
├── campus.py                 # Campus grid environment, state transitions, rewards
├── run_project.py            # CLI entry point for visual search, training, and evaluation
├── summarize_results.py      # Statistical aggregation across seeds and learning curve export
├── maps/
│   ├── emu_campus.txt        # Baseline campus map (11x17)
│   ├── emu_detour.txt        # Detour map with blocked walkway at (3,6)
│   └── my_campus.txt         # Custom campus map (10x15) with cycle & dead-end
├── tests/
│   ├── test_environment.py  # Environment test suite
│   └── test_student.py      # Search and Q-learning unit tests
├── results/
│   ├── part_a_search_results.md # Part A 6-task comparison table & analysis
│   ├── baseline_SW/         # Q-learning results: S -> W baseline (seeds 0, 1, 2)
│   ├── baseline_LD/         # Q-learning results: L -> D baseline (seeds 0, 1, 2)
│   ├── baseline_HP/         # Q-learning results: H -> P baseline (seeds 0, 1, 2)
│   ├── custom_e005/         # Custom map experiment: epsilon = 0.05
│   ├── custom_e020/         # Custom map experiment: epsilon = 0.20
│   └── custom_e050/         # Custom map experiment: epsilon = 0.50
├── REPORT.md                 # Full comprehensive academic project report
├── Eagle_Delivery_Report.pdf # Final 3-page publication-ready PDF submission report
└── README.md                 # Project documentation and reproduction instructions
```

---

## Requirements & Setup

- **Python Version:** Python 3.9 or newer (tested with Python 3.14).
- **Dependencies:** Standard Library only for core algorithms (`collections`, `heapq`, `itertools`, `csv`, `statistics`, `pathlib`, `argparse`).
- **Optional Dependencies:** `matplotlib` (used for plotting learning curves in the report).

To verify the test suite:
```bash
python -m unittest discover -v
```

---

## Reproduction Commands

### Part A: Planning with Search (BFS & A\*)

Run BFS and A\* across the six required delivery scenarios on both the baseline and detour maps:

#### 1. Baseline Map (`maps/emu_campus.txt`)
```bash
# Student Center (S) -> Walton Hall (W)
python run_project.py search --algorithm bfs --start S --goal W
python run_project.py search --algorithm astar --start S --goal W

# Halle Library (L) -> Downing Hall (D)
python run_project.py search --algorithm bfs --start L --goal D
python run_project.py search --algorithm astar --start L --goal D

# Pray-Harrold (H) -> Putnam Hall (P)
python run_project.py search --algorithm bfs --start H --goal P
python run_project.py search --algorithm astar --start H --goal P
```

#### 2. Detour Map (`maps/emu_detour.txt`)
```bash
# Student Center (S) -> Walton Hall (W) [detour active]
python run_project.py search --algorithm bfs --map maps/emu_detour.txt --start S --goal W
python run_project.py search --algorithm astar --map maps/emu_detour.txt --start S --goal W

# Halle Library (L) -> Downing Hall (D)
python run_project.py search --algorithm bfs --map maps/emu_detour.txt --start L --goal D
python run_project.py search --algorithm astar --map maps/emu_detour.txt --start L --goal D

# Pray-Harrold (H) -> Putnam Hall (P)
python run_project.py search --algorithm bfs --map maps/emu_detour.txt --start H --goal P
python run_project.py search --algorithm astar --map maps/emu_detour.txt --start H --goal P
```

---

### Part B: Q-Learning Policy Training & Evaluation

Train Q-learning agents across 3 random seeds (`0`, `1`, `2`) for 2,000 episodes per seed with baseline hyperparameters ($\alpha=0.3, \gamma=0.95, \epsilon=0.2, \text{slip}=0.0$):

```bash
# Train on Task 1: S -> W
python run_project.py train --start S --goal W --output results/baseline_SW

# Train on Task 2: L -> D
python run_project.py train --start L --goal D --output results/baseline_LD

# Train on Task 3: H -> P
python run_project.py train --start H --goal P --output results/baseline_HP
```

Summarize evaluation metrics (100 greedy evaluation episodes per seed) and generate `learning_curve.csv`:
```bash
python summarize_results.py results/baseline_SW
python summarize_results.py results/baseline_LD
python summarize_results.py results/baseline_HP
```

---

### Part C: Custom Campus Experiments (`maps/my_campus.txt`)

Our custom campus layout measures $10 \times 15$ cells and features an open perimeter corridor, an internal cycle loop, and dead-end corridor branches.

#### 1. Search on Custom Map
```bash
# Compare BFS vs. A* from S to W
python run_project.py search --map maps/my_campus.txt --algorithm bfs --start S --goal W
python run_project.py search --map maps/my_campus.txt --algorithm astar --start S --goal W
```
- **BFS:** 11 route steps, **35** nodes expanded.
- **A\*:** 11 route steps, **11** nodes expanded (expanded only the optimal path states).

#### 2. Controlled Experiment: Varying Exploration Rate ($\epsilon$)
Investigating the research question: *How does the exploration rate $\epsilon \in \{0.05, 0.20, 0.50\}$ impact online training performance versus asymptotic greedy policy quality?*

```bash
# Train with low exploration (epsilon = 0.05)
python run_project.py train --map maps/my_campus.txt --epsilon 0.05 --output results/custom_e005

# Train with baseline exploration (epsilon = 0.20)
python run_project.py train --map maps/my_campus.txt --epsilon 0.20 --output results/custom_e020

# Train with high exploration (epsilon = 0.50)
python run_project.py train --map maps/my_campus.txt --epsilon 0.50 --output results/custom_e050
```

Summarize statistical results across seeds and generate learning curves:
```bash
python summarize_results.py results/custom_e005
python summarize_results.py results/custom_e020
python summarize_results.py results/custom_e050
```

---

## Summary of Results

### Part A: Search Comparisons
| Map | Delivery Task | BFS Route Length | A\* Route Length | BFS Expansions | A\* Expansions | Expansion Reduction |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Baseline** | S $\to$ W | 18 | 18 | 67 | 22 | **-67.2%** |
| **Baseline** | L $\to$ D | 22 | 22 | 79 | 62 | **-21.5%** |
| **Baseline** | H $\to$ P | 16 | 16 | 41 | 16 | **-61.0%** |
| **Detour** | S $\to$ W | 26 | 26 | 70 | 51 | **-27.1%** |
| **Detour** | L $\to$ D | 22 | 22 | 65 | 60 | **-7.7%** |
| **Detour** | H $\to$ P | 16 | 16 | 41 | 16 | **-61.0%** |

### Part B & C: Q-Learning Summary
- Across all baseline tasks (`S->W`, `L->D`, `H->P`) and custom map tasks, the greedy evaluation policy ($\epsilon=0$) achieves a **100% delivery success rate** ($1.0 \pm 0.0$) and finds the optimal path length discovered by A\* (18, 22, 16, and 11 steps respectively).
- In the Part C exploration experiment, varying $\epsilon \in \{0.05, 0.20, 0.50\}$ confirms the off-policy optimality of Q-learning: all three agents learn the exact same optimal greedy route (11 steps, mean return 29.0). However, higher $\epsilon$ significantly penalizes online training returns during exploration (mean training return drops from $\approx 28.4$ at $\epsilon=0.05$ to $\approx 16.2$ at $\epsilon=0.50$).

---

## Detailed Report

For the full theoretical formulations, formal proof of Manhattan distance admissibility, detailed empirical discussions, and learning curve visualizations, please refer to:
- [`REPORT.md`](REPORT.md) — Comprehensive markdown report.
- [`Eagle_Delivery_Report.pdf`](Eagle_Delivery_Report.pdf) — Complete 3-page academic submission report.