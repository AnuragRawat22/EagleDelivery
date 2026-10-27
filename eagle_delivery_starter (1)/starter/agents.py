from collections import deque
import heapq
from itertools import count


class SearchResult:
    def __init__(self, path, expanded):
        self.path = path
        self.expanded = expanded


def reconstruct_path(parents, goal):
    """Backtrack from goal to start using parent pointers, then reverse."""
    path = []
    state = goal
    while state is not None:
        path.append(state)
        state = parents[state]
    path.reverse()
    return path


def bfs(campus, start, goal):
    """Breadth-first search on grid using a FIFO queue."""
    frontier = deque([start])
    parents = {start: None}
    expanded = 0

    while frontier:
        state = frontier.popleft()
        if state == goal:
            return SearchResult(reconstruct_path(parents, goal), expanded)
        expanded += 1
        for action, successor in campus.neighbors(state):
            if successor not in parents:
                parents[successor] = state
                frontier.append(successor)

    return SearchResult(None, expanded)


def manhattan(state, goal):
    """Return Manhattan distance (L1 norm) between two (row, column) coordinates."""
    return abs(state[0] - goal[0]) + abs(state[1] - goal[1])


def astar(campus, start, goal):
    """Return SearchResult(path, expanded) for A* graph search."""
    # Trivial edge case: already at the goal
    if start == goal:
        return SearchResult([start], 0)

    # Priority queue stores tuples of: (f, insertion_order, g, state)
    # The insertion counter breaks f-ties by FIFO order without state comparison
    counter = count()
    frontier = []
    heapq.heappush(frontier, (manhattan(start, goal), next(counter), 0, start))

    # Track lowest g-cost discovered so far and parent pointers for path reconstruction
    best_g = {start: 0}
    parents = {start: None}
    expanded = 0

    while frontier:
        f, _, g, state = heapq.heappop(frontier)

        # Skip stale priority queue entries if we already reached this state via a cheaper route
        if g > best_g[state]:
            continue

        # Check goal condition when expanding the node
        if state == goal:
            return SearchResult(reconstruct_path(parents, goal), expanded)

        expanded += 1

        # Evaluate neighbors in campus order: UP, DOWN, LEFT, RIGHT
        for action, successor in campus.neighbors(state):
            new_g = g + 1
            # If we found a strictly cheaper path to successor, update and enqueue
            if new_g < best_g.get(successor, float('inf')):
                best_g[successor] = new_g
                parents[successor] = state
                f_succ = new_g + manhattan(successor, goal)
                heapq.heappush(frontier, (f_succ, next(counter), new_g, successor))

    return SearchResult(None, expanded)


def epsilon_greedy(q_values, state, actions, epsilon, rng):
    """Choose an action with epsilon-greedy exploration."""
    # Explore: choose an action uniformly at random with probability epsilon
    if rng.random() < epsilon:
        return rng.choice(actions)

    # Exploit: retrieve Q-values for available actions (unseen defaults to 0.0)
    q_by_action = [q_values.get((state, a), 0.0) for a in actions]
    max_q = max(q_by_action)

    # Break ties among multiple actions with the same maximum Q-value uniformly at random
    best_actions = [a for a, q in zip(actions, q_by_action) if q == max_q]
    return rng.choice(best_actions)


def q_learning_update(q_values, state, action, reward, next_state,
                      actions, alpha, gamma, terminal):
    """Update exactly one Q-table entry in place using the Bellman equation."""
    # Terminal transitions have zero continuation value
    if terminal:
        target = reward
    else:
        # Include unseen actions with default value 0.0 in max Q calculation
        max_next_q = max(q_values.get((next_state, a), 0.0) for a in actions)
        target = reward + gamma * max_next_q

    # In-place Temporal Difference (TD) update
    current_q = q_values.get((state, action), 0.0)
    q_values[(state, action)] = current_q + alpha * (target - current_q)

