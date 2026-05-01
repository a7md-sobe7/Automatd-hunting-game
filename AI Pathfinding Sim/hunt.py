import heapq
import random
import matplotlib.pyplot as plt
import numpy as np
import time
from matplotlib.colors import ListedColormap
# Constants
GRID_SIZE = 50
OBSTACLE_DENSITY = 0.25
DELAY = 0.25
# Cell types
EMPTY, OBSTACLE, START, TREASURE, GREEDY_PATH, ASTAR_PATH, GREEDY_AGENT, ASTAR_AGENT = 0, 1, 2, 3, 4, 5, 6, 7
# Directions: up, down, left, right
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def generate_grid():
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if random.random() < OBSTACLE_DENSITY:
                grid[i][j] = OBSTACLE
    return grid
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
def place_agent_and_treasure(grid):
    empty_cells = list(zip(*np.where(grid == EMPTY)))
    start = random.choice(empty_cells)
    grid[start] = START
    empty_cells.remove(start)

    distant_cells = [cell for cell in empty_cells if heuristic(start, cell) >= 25]
    treasure = random.choice(distant_cells) if distant_cells else random.choice(empty_cells)
    grid[treasure] = TREASURE
    return start, treasure
class Agent:
    def __init__(self, strategy, name, color_id):
        self.strategy = strategy
        self.name = name
        self.color_id = color_id
        self.path = []
        self.visited = set()
        self.parent = {}
        self.frontier = []
        self.current = None
        self.time_taken = 0

    def initialize(self, start, goal):
        self.goal = goal
        self.current = start
        self.visited = set()
        self.parent = {start: None}
        self.path = []
        self.frontier.clear()
        if self.strategy == 'greedy':
            heapq.heappush(self.frontier, (heuristic(start, goal), start))
        else:
            heapq.heappush(self.frontier, (heuristic(start, goal), 0, start))
            self.g_score = {start: 0}

#algorithms
    def step(self, grid):
        if not self.frontier:
            return False
        if self.strategy == 'greedy':
            _, current = heapq.heappop(self.frontier)
        else:
            _, g, current = heapq.heappop(self.frontier)

        if current == self.goal:
            self.current = current
            return True

        self.visited.add(current)
        for dx, dy in DIRECTIONS:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE:
                if grid[neighbor] != OBSTACLE and neighbor not in self.visited:
                    if self.strategy == 'greedy':
                        heapq.heappush(self.frontier, (heuristic(neighbor, self.goal), neighbor))
                        if neighbor not in self.parent:
                            self.parent[neighbor] = current
                    else:
                        tentative_g = g + 1
                        if neighbor not in self.g_score or tentative_g < self.g_score[neighbor]:
                            self.g_score[neighbor] = tentative_g
                            f = tentative_g + heuristic(neighbor, self.goal)
                            heapq.heappush(self.frontier, (f, tentative_g, neighbor))
                            self.parent[neighbor] = current
        self.current = current
        return False
    def reconstruct_path(self):
        path = []
        node = self.current
        while node is not None:
            path.append(node)
            node = self.parent.get(node)
        path.reverse()
        self.path = path
        return path
def draw_arrows(ax, path, color):
    for i in range(1, len(path)):
        y1, x1 = path[i - 1]
        y2, x2 = path[i]
        dx = x2 - x1
        dy = y2 - y1
        ax.arrow(x1, y1, dx * 0.6, dy * 0.6, head_width=0.3, color=color, length_includes_head=True)
def visualize_race(grid, greedy_agent, astar_agent):
    grid_vis = grid.copy()
    fig, axis = plt.subplots(figsize=(10, 10))

    # Updated color map
    cmap = ListedColormap([
        '#D3D3D3',  # 0 EMPTY (grey)
        'black',    # 1 OBSTACLE
        '#ADD8E6',  # 2 START (baby blue)
        'blue',    # 3 TREASURE (goal)
        'purple',   # 4 GREEDY_PATH
        '#FFC0CB',  # 5 ASTAR_PATH (rose)
        'blue',  # 6 GREEDY_AGENT
        'red'  # 7 ASTAR_AGENT
    ])

    greedy_done = astar_done = False
    greedy_start_time = time.time()
    astar_start_time = time.time()

    winner = None
    winner_time = None

    while not (greedy_done or astar_done):
        grid_vis[grid_vis == GREEDY_AGENT] = GREEDY_PATH
        grid_vis[grid_vis == ASTAR_AGENT] = ASTAR_PATH

        if not greedy_done:
            greedy_done = greedy_agent.step(grid)
            if greedy_done:
                greedy_agent.time_taken = time.time() - greedy_start_time
                winner = greedy_agent.name
                winner_time = greedy_agent.time_taken

        if not astar_done:
            astar_done = astar_agent.step(grid)
            if astar_done:
                astar_agent.time_taken = time.time() - astar_start_time
                if winner is None:
                    winner = astar_agent.name
                    winner_time = astar_agent.time_taken

        if greedy_agent.current:
            gy, gx = greedy_agent.current
            grid_vis[gy][gx] = GREEDY_AGENT
        if astar_agent.current:
            ay, ax_ = astar_agent.current
            grid_vis[ay][ax_] = ASTAR_AGENT

        axis.clear()
        axis.imshow(grid_vis, cmap=cmap, interpolation='nearest')
        axis.set_title(f"Greedy: 🟪 | A*: 🌸", fontsize=12)
        axis.axis('off')
        plt.pause(DELAY)

    # Final path drawing
    greedy_path = greedy_agent.reconstruct_path()
    astar_path = astar_agent.reconstruct_path()

    draw_arrows(axis, greedy_path, 'blue')
    draw_arrows(axis, astar_path, 'red')

    title_text = f"🏁 Winner: {winner} (Time: {winner_time:.2f}s)"
    axis.set_title(title_text, fontsize=14)
    plt.show()
def run_simulation():
    grid = generate_grid()
    start, treasure = place_agent_and_treasure(grid)
    greedy_agent = Agent(strategy='greedy', name='Greedy (🟪)', color_id=GREEDY_AGENT)
    astar_agent = Agent(strategy='astar', name='A* (🌸)', color_id=ASTAR_AGENT)
    greedy_agent.initialize(start, treasure)
    astar_agent.initialize(start, treasure)
    visualize_race(grid, greedy_agent, astar_agent)
# Execution loop
while True:
    run_simulation()
    choice = input("Replay? (y/n): ").strip().lower()
    if choice == 'n':
        print("Thank you for trying our simulation")
        break