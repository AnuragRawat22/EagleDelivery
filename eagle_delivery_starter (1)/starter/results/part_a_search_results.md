# Part A: Search Formulation, Implementation, and Comparison

## 1. Problem Formulation
- **State Space**: A state $s = (r, c)$ represents the 2D grid coordinates of the robot on a traversable walkway (`.`) or building entrance (`S, L, H, D, P, W`).
- **Initial State**: The coordinate $(r_0, c_0)$ corresponding to the starting building entrance symbol.
- **Actions**: Four discrete cardinal actions: `ACTIONS = ("UP", "DOWN", "LEFT", "RIGHT")`.
- **Transition Model**: Deterministic transition $T(s, a) \to s'$. Attempting to move into an adjacent cell updates position by one unit $(\Delta r, \Delta c)$ if that cell is inside map boundaries and not blocked (`#`). If blocked or out-of-bounds, the robot remains in place ($s' = s$). Diagonal movement is not permitted.
- **Goal Test**: $s = \text{goal}$, testing whether current state matches destination building coordinate $(r_g, c_g)$.
- **Path Cost**: Uniform step cost of $c(s, a, s') = 1$ for each traversable step. The total path cost is the total number of actions along the path: $\text{len}(\text{path}) - 1$.
- **Optimality of BFS**: In graphs where all step costs are identical and positive ($c = 1$), breadth-first search expands states in strictly non-decreasing order of path cost (depth). The first time BFS dequeues the goal state, the path discovered is guaranteed to have the minimal number of steps, ensuring path cost optimality.

## 2. Admissibility of Manhattan Distance Heuristic
- **Formula**: $h(s) = |r_s - r_g| + |c_s - c_g|$
- **Admissibility Explanation**: A heuristic is admissible if $h(s) \le h^*(s)$ for all states $s$, meaning it never overestimates the true remaining cost to the goal. In a 4-connected grid without diagonal movement, the Manhattan distance represents the true shortest path length in the relaxed problem where all obstacles and walls are removed. Because adding walls and obstacles can only increase the actual path length ($h^*(s) \ge h(s)$) and can never create a shorter path than the straight Manhattan distance, $h(s)$ is strictly admissible.

## 3. Six Required BFS vs. A* Comparisons

| Map | Delivery Task | BFS Route Length | A* Route Length | BFS Expanded Node Count | A* Expanded Node Count |
| :--- | :--- | :---: | :---: | :---: | :---: |
| Baseline | S $\to$ W (Student Center to Walton Hall) | 18 | 18 | 67 | 22 |
| Baseline | L $\to$ D (Halle Library to Downing Hall) | 22 | 22 | 79 | 62 |
| Baseline | H $\to$ P (Pray-Harrold to Putnam Hall) | 16 | 16 | 41 | 16 |
| Detour | S $\to$ W (Student Center to Walton Hall) | 26 | 26 | 70 | 51 |
| Detour | L $\to$ D (Halle Library to Downing Hall) | 22 | 22 | 65 | 60 |
| Detour | H $\to$ P (Pray-Harrold to Putnam Hall) | 16 | 16 | 41 | 16 |

## 4. Analysis and Observations
1. **Route Length Equality**: Both BFS and A* consistently found routes of identical lengths across all six tasks. This confirms that both algorithms guarantee optimality under unit edge costs with an admissible heuristic.
2. **Impact of Walkway Detour**: On the Detour map (where cell `(3, 6)` is blocked), the S $\to$ W route length increases by 8 steps (from 18 to 26). The other two tasks (L $\to$ D and H $\to$ P) are unaffected in route length (22 and 16 steps respectively) because their optimal routes do not pass through `(3, 6)`.
3. **Expanded Nodes**: A* expanded significantly fewer nodes than BFS in every scenario. For example, in H $\to$ P on both maps, A* expanded only 16 nodes—exactly equal to the path length—meaning it directed its search straight to the goal without exploring unnecessary branches. In S $\to$ W on the baseline map, A* expanded only 22 nodes compared to 67 nodes for BFS (a 67% reduction).
4. **General Behavior of A* vs BFS**: A* does not necessarily expand fewer nodes than BFS in every conceivable edge case. When heuristics guide the search towards obstacle concavities or dead-ends that point geometrically toward the goal, A* may expand many nodes inside the obstacle trap before discovering that the true path must detour backward. In contrast, on maps with direct corridors or open layouts, A* concentrates expansions along the goal direction.
