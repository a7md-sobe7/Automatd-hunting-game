# AI Pathfinding Race — Greedy vs A*

A visual simulation that pits two AI search agents against each other in a race to find hidden treasure on a randomly generated grid. The agents use **Greedy Best-First Search** and **A\* Search** respectively, and their paths are animated in real time using Matplotlib.

---

## Table of Contents

- [Overview](#overview)
- [Algorithms](#algorithms)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Grid & Color Legend](#grid--color-legend)
- [How It Works](#how-it-works)
- [Example Output](#example-output)

---

## Overview

| Property         | Details                              |
|------------------|--------------------------------------|
| Language         | Python 3                             |
| Visualization    | Matplotlib                           |
| Grid Size        | 50 × 50                              |
| Obstacle Density | 25%                                  |
| Algorithms       | Greedy Best-First Search, A* Search  |
| Heuristic        | Manhattan Distance                   |
| Movement         | 4-directional (Up, Down, Left, Right)|

At the start of each simulation:
- A 50×50 grid is randomly generated with ~25% obstacles.
- A **Start** position and a **Treasure** position are placed at least 25 cells apart (Manhattan distance).
- Both agents begin from the same start and race to the treasure simultaneously, one step at a time.
- The winner (the agent that reaches the treasure first) is announced at the end along with the time taken.

---

## Algorithms

### Greedy Best-First Search (🟪)

Greedy search expands the node that appears closest to the goal based purely on the heuristic function — in this case, **Manhattan distance**. It does not account for the actual cost of the path already traveled.

- **Fast** in many cases, as it heads straight toward the goal.
- **Not guaranteed to find the shortest path** — it can get trapped in suboptimal routes.
- Uses a min-heap (priority queue) ordered by `h(n)` (heuristic only).

### A\* Search (🌸)

A\* combines the actual cost to reach a node and the estimated cost to reach the goal:

```
f(n) = g(n) + h(n)
```

Where:
- `g(n)` = cost from start to node `n` (number of steps taken)
- `h(n)` = Manhattan distance heuristic from `n` to goal

- **Guaranteed to find the shortest path** when the heuristic is admissible (Manhattan distance is admissible on a uniform-cost grid).
- Generally **slower than Greedy** due to more thorough exploration, but produces optimal routes.
- Uses a min-heap ordered by `f(n)`.

---

## Project Structure

```
Ai Project/
└── hunt/
    └── hunt.py       # Main simulation script (all logic in one file)
```

---

## Requirements

- Python 3.7+
- `matplotlib`
- `numpy`

---

## Installation

### 1. Clone or extract the project

```bash
unzip Ai_Project.zip
cd "Ai Project/hunt"
```

### 2. (Recommended) Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install matplotlib numpy
```

---

## Usage

Run the simulation directly:

```bash
python hunt.py
```

The Matplotlib window will open and animate both agents simultaneously as they navigate the grid toward the treasure.

When both agents have either reached the goal or exhausted their frontiers:
- Final paths are drawn with directional arrows.
- The window title shows the **winner** and their **time taken**.

You will then be prompted in the terminal:

```
Replay? (y/n):
```

- Enter `y` to generate a brand new grid and run again.
- Enter `n` to exit.

```
Thank you for trying our simulation
```

---

## Configuration

All key constants are defined at the top of `hunt.py` and can be easily adjusted:

| Constant           | Default | Description                                                  |
|--------------------|---------|--------------------------------------------------------------|
| `GRID_SIZE`        | `50`    | Width and height of the grid (N × N)                         |
| `OBSTACLE_DENSITY` | `0.25`  | Fraction of cells that are obstacles (0.0 – 1.0)             |
| `DELAY`            | `0.25`  | Pause in seconds between each animation frame                |

**Example — larger grid, faster animation:**

```python
GRID_SIZE = 75
OBSTACLE_DENSITY = 0.20
DELAY = 0.1
```

> Increasing `GRID_SIZE` significantly will slow down rendering. Reduce `DELAY` to compensate.

---

## Grid & Color Legend

| Color        | Cell Type    | ID | Description                        |
|--------------|--------------|----|------------------------------------|
| Light Grey   | Empty        | 0  | Traversable open cell              |
| Black        | Obstacle     | 1  | Impassable wall                    |
| Baby Blue    | Start        | 2  | Shared starting position           |
| Blue         | Treasure     | 3  | Goal — both agents race to this    |
| Purple       | Greedy Path  | 4  | Cells already visited by Greedy    |
| Rose / Pink  | A\* Path     | 5  | Cells already visited by A\*       |
| Blue (agent) | Greedy Agent | 6  | Current position of Greedy agent   |
| Red (agent)  | A\* Agent    | 7  | Current position of A\* agent      |

---

## How It Works

### Grid Generation

A 50×50 NumPy array is initialized to zeros (empty). Each cell is independently given a 25% chance of becoming an obstacle.

### Agent & Treasure Placement

- The **Start** position is chosen randomly from all empty cells.
- The **Treasure** is placed in a cell at least **25 Manhattan-distance units** away from the start, ensuring a non-trivial search challenge.

### Simulation Loop

Each iteration of the main loop advances **both agents by one step** before redrawing the grid:

```
1. Clear agent markers from the previous frame
2. Step Greedy agent → pop the node with the lowest h(n) from its frontier
3. Step A* agent     → pop the node with the lowest f(n) = g(n)+h(n) from its frontier
4. Mark the new agent positions on the grid
5. Redraw and pause for DELAY seconds
6. Repeat until one or both agents reach the treasure
```

### Path Reconstruction

Once an agent reaches the treasure, it walks back through its `parent` dictionary from goal to start to reconstruct the full path, which is then drawn with directional arrows on the final frame.

### Winner Declaration

The first agent whose `step()` returns `True` (i.e., its current node equals the goal) is declared the winner. Time is measured with `time.time()` from initialization to goal-reach.

---

## Example Output

```
Greedy: 🟪 | A*: 🌸
🏁 Winner: A* (🌸) (Time: 1.43s)

Replay? (y/n): y
```

The final Matplotlib window shows both complete paths overlaid on the grid with color-coded arrows — purple for Greedy, rose/pink for A\* — so you can visually compare the routes each agent chose.

Author
Ahmad sobeh
ahmadaymansobeh@gmail.com
