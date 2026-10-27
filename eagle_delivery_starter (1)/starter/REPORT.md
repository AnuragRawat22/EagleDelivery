# Eagle Delivery: Autonomous Campus Navigation via Heuristic Search and Q-Learning

**Author:** Anurag Singh Rawat  
**Institution:** Eastern Michigan University (EMU)  
**Course:** COSC 461/561 — Artificial Intelligence  
**Date:** October 26, 2026  

---

## 1. Introduction & Formal Problem Formulation

Autonomous navigation in structured environments is a foundational challenge in artificial intelligence, bridging classical search and modern reinforcement learning. The **Eagle Delivery** project models an autonomous robotic delivery system designed for the Eastern Michigan University campus. The robot's objective is to accept a delivery request, retrieve a package from a designated building entrance, and navigate across campus walkways to reach the recipient building entrance while minimizing transit time and avoiding obstacles.

```
Campus Layout Coordinate System & Building Entrances (emu_campus.txt):
  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6
0 # # # # # # # # # # # # # # # # #
1 # S . . . . # . . . . . . . . W #   S: Student Center   (1, 1)   W: Walton Hall  (1, 15)
2 # . # # # . # . # # # # # . # . #   L: Halle Library    (5, 1)   D: Downing Hall (5, 15)
3 # . . . # . . . # . . . # . . . #   H: Pray-Harrold     (9, 1)   P: Putnam Hall  (9, 13)
4 # . # . # # # # # . # . # # # . #   .: Traversable Path          #: Obstacle
5 # L # . . . . . . . # . . . . D #
6 # . # # # # # . # . # # # # # . #
7 # . . . . . # . # . . . . . . . #
8 # # # . # . # . # # # # # # # . #
9 # H . . # . . . . . . . . P . . #
0 # # # # # # # # # # # # # # # # #
```

We formulate the campus navigation problem as a deterministic, discrete state-space planning and control problem:

1. **State Space ($S$):**  
   A state $s = (r, c) \in \mathbb{Z}^2$ denotes the 2D discrete grid coordinates of the robot on a traversable walkway (`.`) or a building entrance (`S, L, H, D, P, W`). For an $R \times C$ campus grid, $S \subset \{0, \dots, R-1\} \times \{0, \dots, C-1\} \setminus \{s \mid \text{grid}(s) = \text{'\#'}\}$.
   
2. **Initial State ($s_0$):**  
   The coordinate $(r_0, c_0) \in S$ corresponding to the specified source building entrance symbol (e.g., $s_0 = (1, 1)$ for Student Center `S`).

3. **Action Space ($A(s)$):**  
   At every state, the robot may attempt one of four cardinal, unweighted actions:
   $$A = \{\text{UP}, \text{DOWN}, \text{LEFT}, \text{RIGHT}\}$$
   with unit displacement vectors $\Delta(a) \in \{(-1, 0), (1, 0), (0, -1), (0, 1)\}$. Diagonal transitions are strictly prohibited.

4. **Transition Model ($T: S \times A \to S$):**  
   The motion dynamics are deterministic. Let $s' = s + \Delta(a)$. If $s'$ lies within grid boundaries and is traversable ($\text{grid}(s') \neq \text{'\#'}$), the robot successfully moves to $s'$. If $s'$ is out-of-bounds or an obstacle wall, the robot collides and remains in place ($T(s, a) = s$).

5. **Goal Test ($G(s)$):**  
   A boolean predicate $G(s) = \mathbb{I}(s = s_{\text{goal}})$, evaluating to true if and only if the robot's current coordinate matches the destination building entrance $(r_g, c_g)$. Intermediate building entrances encountered along the route are treated as traversable walkways and do not trigger termination.

6. **Path Cost ($c(s, a, s')$):**  
   Each attempted action incurs a uniform step cost of $c(s, a, s') = 1$, regardless of whether motion succeeds or is blocked by an obstacle. The total cost of an execution trajectory $\pi = (s_0, s_1, \dots, s_k)$ is the total step count:
   $$\text{Cost}(\pi) = \sum_{t=0}^{k-1} c(s_t, a_t, s_{t+1}) = k = \text{len}(\pi) - 1$$

7. **Optimality of Breadth-First Search (BFS):**  
   In graphs where all edge transition costs are identical and positive ($c = 1$), Breadth-First Search expands nodes in strictly non-decreasing order of path cost (depth levels $d = 0, 1, 2, \dots$). By using a FIFO queue, all states at depth $d$ are expanded before any state at depth $d+1$ is explored. When BFS first selects the goal node from the frontier, no undiscovered path to the goal can have cost less than $d$. Therefore, the first path discovered by BFS is mathematically guaranteed to be cost-optimal.

---

## 2. Heuristic Admissibility Proof for Manhattan Distance

In Part A, informed heuristic search uses the Manhattan distance (taxicab metric / $L_1$ norm) between the current state $s = (r_s, c_s)$ and the goal state $g = (r_g, c_g)$:

$$h(s) = |r_s - r_g| + |c_s - c_g|$$

### Formal Theorem: Admissibility of Manhattan Distance
A heuristic function $h: S \to \mathbb{R}_{\ge 0}$ is defined as **admissible** if it never overestimates the true minimal cost $h^*(s)$ required to reach the goal state $g$ from state $s$:

$$\forall s \in S, \quad 0 \le h(s) \le h^*(s)$$

### Mathematical Proof:
1. **The Relaxed Problem:**  
   Consider a relaxed formulation of the grid navigation task where all obstacle walls (`#`) and campus boundaries are removed, allowing unrestricted movement across the entire $\mathbb{Z}^2$ integer lattice.
   
2. **Minimal Coordinate Displacements in 4-Connected Grids:**  
   To navigate from $(r_s, c_s)$ to $(r_g, c_g)$, the agent must change its vertical coordinate by $|r_s - r_g|$ and its horizontal coordinate by $|c_s - c_g|$.  
   At each transition step $t$, the agent selects an action $a_t \in \{\text{UP}, \text{DOWN}, \text{LEFT}, \text{RIGHT}\}$. By definition of cardinal moves:
   $$|\Delta r_t| + |\Delta c_t| \le 1$$
   Summing across all $k$ steps of an arbitrary valid path from $s$ to $g$:
   $$|r_s - r_g| = \left| \sum_{t=1}^k \Delta r_t \right| \le \sum_{t=1}^k |\Delta r_t|$$
   $$|c_s - c_g| = \left| \sum_{t=1}^k \Delta c_t \right| \le \sum_{t=1}^k |\Delta c_t|$$
   Adding these two inequalities together yields:
   $$|r_s - r_g| + |c_s - c_g| \le \sum_{t=1}^k (|\Delta r_t| + |\Delta c_t|) \le \sum_{t=1}^k 1 = k$$
   Consequently, any valid path in the relaxed grid requires at least $k \ge |r_s - r_g| + |c_s - c_g|$ steps. The minimal relaxed path cost is exactly $h_{\text{relaxed}}^*(s) = |r_s - r_g| + |c_s - c_g| = h(s)$.

3. **Obstacle Constraints:**  
   The actual campus environment contains impassable obstacle walls (`#`). Introducing obstacles restricts the set of available transitions without permitting any shortcut or diagonal transition. Therefore, the optimal path cost in the constrained graph $h^*(s)$ can never be strictly less than the optimal path cost in the unconstrained relaxed graph:
   $$h^*(s) \ge h_{\text{relaxed}}^*(s) = h(s)$$

4. **Consistency (Monotonicity):**  
   Furthermore, for any transition between adjacent states $s$ and $s'$, the triangle inequality ensures:
   $$|h(s) - h(s')| = \big| (|r_s - r_g| + |c_s - c_g|) - (|r_{s'} - r_g| + |c_{s'} - c_g|) \big| \le |r_s - r_{s'}| + |c_s - c_{s'}| = 1 = c(s, a, s')$$
   Thus, $h(s) \le c(s, a, s') + h(s')$, establishing that the Manhattan metric is also **consistent (monotone)**.

Because $h(g) = 0$ and $h(s) \le h^*(s)$ everywhere, A* graph search equipped with this heuristic is guaranteed to yield an optimal path without reopening expanded nodes. $\blacksquare$

---

## 3. Part A: Heuristic Search Implementation & Empirical Evaluation

### Implementation Architecture
The search algorithms were implemented in `agents.py`:
- **BFS (`bfs`)**: Utilizes a double-ended queue (`collections.deque`) as a FIFO frontier. Visited states are recorded in a parent dictionary `parents = {start: None}` upon frontier insertion. Goal detection occurs upon node expansion.
- **A\* (`astar`)**: Employs a min-priority queue (`heapq`) storing tuples of `(f, insertion_counter, g, state)` where $f(s) = g(s) + h(s)$. To guarantee strict reproducibility and resolve equal-$f$ ties deterministically by insertion order without attempting invalid state coordinate comparisons, a unique monotonically increasing integer `counter = itertools.count()` is injected. A lookup dictionary `best_g` tracks the lowest known cost to each state. Stale queue entries whose recorded $g$ exceeds `best_g[state]` are lazily pruned. Successors are expanded in the exact specified cardinal order (`UP`, `DOWN`, `LEFT`, `RIGHT`).

### Empirical Comparison
We evaluated BFS and A* across the six required campus navigation benchmarks spanning the baseline campus (`emu_campus.txt`) and detour campus (`emu_detour.txt`), where walkway coordinate $(3, 6)$ is obstructed:

| Map Environment | Delivery Task | BFS Route Length | A\* Route Length | BFS Node Expansions | A\* Node Expansions | Expansion Reduction (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Baseline** (`emu_campus`) | S $\to$ W (Student Center to Walton Hall) | 18 | 18 | 67 | 22 | **-67.2%** |
| **Baseline** (`emu_campus`) | L $\to$ D (Halle Library to Downing Hall) | 22 | 22 | 79 | 62 | **-21.5%** |
| **Baseline** (`emu_campus`) | H $\to$ P (Pray-Harrold to Putnam Hall) | 16 | 16 | 41 | 16 | **-61.0%** |
| **Detour** (`emu_detour`) | S $\to$ W (Student Center to Walton Hall) | 26 | 26 | 70 | 51 | **-27.1%** |
| **Detour** (`emu_detour`) | L $\to$ D (Halle Library to Downing Hall) | 22 | 22 | 65 | 60 | **-7.7%** |
| **Detour** (`emu_detour`) | H $\to$ P (Pray-Harrold to Putnam Hall) | 16 | 16 | 41 | 16 | **-61.0%** |

### Analysis of Search Results
1. **Route Optimality:**  
   In all six configurations, BFS and A* returned identical route lengths. This empirical equivalence confirms our theoretical proof: both algorithms are strictly optimal under unit edge costs with an admissible heuristic.
   
2. **Impact of Walkway Detour:**  
   Blocking cell $(3, 6)$ in `emu_detour.txt` directly impacts the corridor normally used for S $\to$ W transit. As a result, the S $\to$ W optimal path length increases from 18 to 26 (+8 steps), forcing the robot around the central academic building complex. Conversely, tasks L $\to$ D (22 steps) and H $\to$ P (16 steps) maintain identical route lengths because their optimal trajectories do not traverse cell $(3, 6)$.

3. **Node Expansion Efficiency:**  
   A* expanded substantially fewer nodes than BFS across every test case. The efficiency gain is most dramatic in H $\to$ P, where A* expanded exactly 16 nodes—matching the path length. Because the walkway between H and P offers a direct, unblocked route toward the goal, the Manhattan heuristic perfectly reflects the true cost ($h(s) = h^*(s)$), directing A* straight along the optimal path with zero wasted expansions. For Baseline S $\to$ W, A* achieved a **67.2% reduction** in node expansions (22 vs. 67).

4. **Theoretical Limits: Does A\* Always Expand Fewer Nodes?**  
   While A* dominates in open layouts and direct corridors, **A\* does not expand fewer nodes than BFS in every conceivable scenario**. In environments featuring deep concave obstacles (e.g., U-shaped building walls whose openings face away from the goal), the Manhattan heuristic pulls A* aggressively into the dead-end because the geometric distance to the goal decreases. A* must exhaustively expand all interior nodes of the trap before $f = g + h$ rises enough to prioritize the escape route. In contrast, BFS radiates outward in concentric diamond shells and may circumvent the obstacle boundary with comparable or fewer node expansions.

---

## 4. Part B: Model-Free Reinforcement Learning via Q-Learning

When prior map geometry is unavailable, the robot must learn optimal navigation policies through environmental feedback using reinforcement learning.

### Reinforcement Learning Formulation
- **Markov Decision Process (MDP):** Modeled by $(S, A, T, R, \gamma)$.
- **Reward Dynamics:** Each attempted move incurs a step penalty $r = -1$. First arrival at the goal yields a $+40$ delivery bonus:
  $$r(s, a, s') = \begin{cases} +39 & \text{if } s' = s_{\text{goal}} \\ -1 & \text{otherwise} \end{cases}$$
  An episode terminates upon reaching $s_{\text{goal}}$ or after exceeding the 200-step horizon. Undiscounted return for an optimal $L$-step path is $R = 40 - L$.
- **Action-Value Function ($Q(s, a)$):**  
  Maintained as a dictionary mapping state-action pairs $((r, c), a) \mapsto \mathbb{R}$, initialized to $0.0$ for all unseen transitions.
- **Exploration Strategy ($\epsilon$-greedy):**  
  With probability $\epsilon$, the agent chooses a random action uniformly from $A$; with probability $1 - \epsilon$, it exploits the greedy action $\arg\max_a Q(s, a)$. Ties among maximal actions are broken uniformly at random via `rng.choice()`.
- **Q-Learning Update Rule (Watkins' Off-Policy Control):**
  $$y = \begin{cases} r & \text{if } s' \text{ is terminal} \\ r + \gamma \max_{a' \in A} Q(s', a') & \text{otherwise} \end{cases}$$
  $$Q(s, a) \leftarrow Q(s, a) + \alpha \big[ y - Q(s, a) \big]$$

### Experimental Setup & Hyperparameters
- **Learning rate:** $\alpha = 0.3$ (moderates temporal-difference updates, ensuring stability).
- **Discount factor:** $\gamma = 0.95$ (balances immediate step penalties against terminal rewards).
- **Exploration probability:** $\epsilon = 0.20$ (maintains sufficient state-space coverage).
- **Training regime:** 2,000 episodes per seed across 3 independent seeds (`0, 1, 2`).
- **Evaluation regime:** 100 episodes per seed with learning frozen ($\alpha = 0$) and exploration disabled ($\epsilon = 0$).

### Baseline Results & Discussion
The three required baseline tasks on `emu_campus.txt` were trained and evaluated:

| Baseline Delivery Task | Target Shortest Path ($L$) | Theoretical Return ($40 - L$) | Evaluation Success Rate | Evaluation Mean Return | Evaluation Mean Steps |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **S $\to$ W** (Student $\to$ Walton) | 18 | 22.0 | **100%** ($1.0 \pm 0.0$) | **22.0** $\pm 0.0$ | **18.0** $\pm 0.0$ |
| **L $\to$ D** (Library $\to$ Downing) | 22 | 18.0 | **100%** ($1.0 \pm 0.0$) | **18.0** $\pm 0.0$ | **22.0** $\pm 0.0$ |
| **H $\to$ P** (Harrold $\to$ Putnam) | 16 | 24.0 | **100%** ($1.0 \pm 0.0$) | **24.0** $\pm 0.0$ | **16.0** $\pm 0.0$ |

### Findings:
1. **Convergence to Global Optimality:** Across all nine independent training runs (3 tasks $\times$ 3 seeds), the greedy evaluation policy achieved a flawless 100% delivery rate ($1.0 \pm 0.0$).
2. **Alignment with Heuristic Search:** In every task, the mean evaluation path length matched the exact optimal path length determined by BFS and A* ($L = 18, 22, 16$). The mean returns ($22.0, 18.0, 24.0$) exactly satisfied the theoretical return equation $R = 40 - L$, proving that model-free tabular Q-learning successfully converges to the globally optimal shortest-path policy without map information.
3. **Training Dynamics:** As illustrated in the training curves, initial episodes exhibit negative returns as the agent randomly explores and frequently reaches the 200-step truncation limit. Within 300 to 500 episodes, the success rate reaches 100%, and returns stabilize near asymptotic levels.

---

## 5. Part C: Custom Campus Design & Epsilon Exploration Study

### Custom Campus Design (`maps/my_campus.txt`)
We designed an asymmetric $10 \times 15$ campus layout satisfying all specification criteria:
- Enclosed completely by perimeter wall boundaries (`#`).
- Features all six building entrance symbols exactly once:
  - `S`: Student Center at coordinate $(1, 1)$
  - `W`: Walton Hall at coordinate $(1, 12)$
  - `L`: Halle Library at coordinate $(5, 1)$
  - `D`: Downing Hall at coordinate $(5, 13)$
  - `H`: Pray-Harrold at coordinate $(9, 1)$
  - `P`: Putnam Hall at coordinate $(9, 12)$
- **Structural Topology:**
  1. *Primary Corridor:* A straight northern walkway directly connecting S to W across row 1 (optimal length = 11 steps).
  2. *Internal Cyclic Loop:* A loop spanning rows 3 through 7 between columns 3 and 11, providing alternative paths between north and south campus.
  3. *Dead-End Corridors:* Multiple dead-end branches (e.g., column 5 row 4, column 9 row 4, column 7 row 6) creating deceptive local attractors.

On task S $\to$ W:
- **BFS:** 11 steps, **35** node expansions.
- **A\*:** 11 steps, **11** node expansions (only path nodes expanded).

### Controlled Experiment: Exploration Rate ($\epsilon$)
We formulated the following research question:
> **Research Question:** How does the exploration parameter $\epsilon \in \{0.05, 0.20, 0.50\}$ affect online training efficiency, transient episode returns, and final greedy policy quality in grid campus navigation?

- **Hypothesis / Prediction:**  
  Because Q-learning is an **off-policy algorithm** where updates target the Bellman optimality operator $\max_{a'} Q(s', a')$ independently of the action selected, all three exploration rates will converge to the identical optimal greedy policy during frozen evaluation ($\epsilon=0$). However, during training, higher exploration ($\epsilon=0.50$) will cause significant random dithering, sharply reducing online returns, while low exploration ($\epsilon=0.05$) will maximize online returns but may exhibit slower early discovery.

### Empirical Results

#### Evaluation Performance (100 episodes per seed, $\epsilon = 0$, $\alpha = 0$):
| Exploration Setting ($\epsilon$) | Evaluation Success Rate | Evaluation Mean Return | Evaluation Mean Steps | Optimal Path Recovered |
| :--- | :---: | :---: | :---: | :---: |
| $\epsilon = 0.05$ (Low Exploration) | **1.00** $\pm 0.0$ | **29.0** $\pm 0.0$ | **11.0** $\pm 0.0$ | Yes (Optimal 11 steps) |
| $\epsilon = 0.20$ (Baseline Exploration) | **1.00** $\pm 0.0$ | **29.0** $\pm 0.0$ | **11.0** $\pm 0.0$ | Yes (Optimal 11 steps) |
| $\epsilon = 0.50$ (High Exploration) | **1.00** $\pm 0.0$ | **29.0** $\pm 0.0$ | **11.0** $\pm 0.0$ | Yes (Optimal 11 steps) |

#### Training Dynamics Comparison (Binned into 100-episode blocks):
| Episode Interval | Metric | $\epsilon = 0.05$ | $\epsilon = 0.20$ | $\epsilon = 0.50$ |
| :--- | :--- | :---: | :---: | :---: |
| **Episodes 1–100** | Success Rate (%) | 93.3% | 93.3% | 90.3% |
| | Mean Return | **-3.1** | **-5.1** | **-18.2** |
| **Episodes 401–500** | Success Rate (%) | 100.0% | 100.0% | 100.0% |
| | Mean Return | **+28.5** | **+26.0** | **+16.5** |
| **Episodes 1901–2000** | Success Rate (%) | 100.0% | 100.0% | 100.0% |
| | Mean Return | **+28.3** | **+26.3** | **+16.0** |

### Synthesis and Key Insights
1. **Validation of Off-Policy Separation:**  
   Our experimental results provide clear empirical verification of the core distinction between behavior and target policies in reinforcement learning. While during training the agents experienced radically different return trajectories—with $\epsilon = 0.50$ averaging a return of only $+16.0$ compared to $+28.3$ for $\epsilon = 0.05$—all three configurations converged to the exact same optimal policy upon evaluation ($L = 11$, Return $= 29.0$).
   
2. **The Exploration Cost in Online Performance:**  
   In online deployment where learning occurs in real-time, high exploration incurs a severe penalty. With $\epsilon = 0.50$, the agent takes an exploratory random action on every other step, causing it to bounce off walls and drift into dead-ends. This results in an average online episode length of $\approx 24$ steps ($40 - 24 = 16$), wasting substantial energy and time. In contrast, $\epsilon = 0.05$ achieved near-optimal online performance ($+28.5$) while still exploring sufficiently to discover the optimal corridor.

---

## 6. Conclusion

This project implemented and empirically validated both planning and learning approaches to autonomous mobile robot navigation:
- **Part A:** Confirmed the admissibility and consistency of the Manhattan heuristic on 4-connected grid maps, demonstrating that A* reduces node expansions by up to 67.2% relative to BFS while guaranteeing cost optimality.
- **Part B:** Proved that model-free tabular Q-learning converges reliably across diverse random seeds to the exact optimal shortest paths discovered by informed search, without requiring map transition models.
- **Part C:** Designed a custom campus topology and demonstrated that while exploration parameter $\epsilon$ drastically dictates online operational efficiency, Q-learning's off-policy nature ensures robust asymptotic convergence to the globally optimal navigation policy.
