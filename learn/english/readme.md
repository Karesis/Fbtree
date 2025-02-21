# FiberTree Tutorial

## Table of Contents
- [1. Introduction and Installation](#1-introduction-and-installation)
- [2. Core Concepts](#2-core-concepts)
- [3. Basic Tutorial](#3-basic-tutorial) 
- [4. Intermediate Tutorial](#4-intermediate-tutorial)
- [5. Advanced Features](#5-advanced-features)
- [6. Best Practices](#6-best-practices)
- [7. Case Studies](#7-case-studies) 
- [8. API Reference](#8-api-reference)

## 1. Introduction and Installation

### 1.1 What is FiberTree?

FiberTree is a path-oriented database system specialized in storing and analyzing sequential decision paths. In many application domains, decisions are made sequentially, forming decision paths. FiberTree efficiently stores these paths and provides powerful tools to analyze their effectiveness, discover patterns, and provide decision support.

**Key Features**:
- Efficient storage of sequential decision paths
- Statistical analysis of path success rates
- Finding optimal decision sequences
- Visualization of decision tree structures
- Support for both in-memory and SQLite storage modes

### 1.2 Application Domains

FiberTree is particularly well-suited for:
- **Game AI Development**: Recording game decision sequences and their outcomes
- **User Behavior Analysis**: Tracking user navigation paths in websites/applications
- **Automated Decision Systems**: Optimizing decision chains and processes
- **Path Planning**: Analyzing the efficiency and success rates of different paths
- **Knowledge Representation**: Building and querying decision knowledge bases

### 1.3 Installation

**Via pip**:
```bash
pip install fbtree
```

**From source**:
```bash
git clone https://github.com/Karesis/Fbtree.git
cd fbtree
pip install -e .
```

## 2. Core Concepts

Before starting with FiberTree, it's important to understand three key concepts:

### 2.1 Move

A `Move` represents a single decision or action in a sequence. It can store any type of value and can be associated with additional metadata.

```python
from fbtree import Move

# Simple move
move1 = Move("forward")

# Move with metadata
move2 = Move("left", metadata={"angle": 90, "reason": "obstacle avoidance"})
```

### 2.2 Fiber

A `Fiber` is a container for a series of moves, forming a complete decision path. It includes the move sequence and related statistics (e.g., visit count, success rate).

```python
from fbtree import Fiber, Move

# Create a path with three moves
fiber = Fiber(moves=[Move("A"), Move("B"), Move("C")])
```

### 2.3 FiberTree

A `FiberTree` is a database that manages multiple Fibers, providing functions for adding, querying, analyzing, and visualizing them. It builds a tree structure where paths can share prefixes, making it efficient for storing similar decision sequences.

```python
from fbtree import create_tree

# Create a new tree
tree = create_tree()
```

## 3. Basic Tutorial

### 3.1 Creating Your First Tree

Let's start by creating a simple FiberTree:

```python
from fbtree import create_tree, Move

# Create an in-memory tree
tree = create_tree()

# Create a SQLite-backed tree (persistent)
# tree = create_tree(storage_type='sqlite', db_path='my_database.db')
```

### 3.2 Recording Decision Paths

Record a simple decision path:

```python
# Start building a path
tree.start_path()

# Add moves
tree.add_move(Move("A"))
tree.add_move(Move("B"))
tree.add_move(Move("C"))

# Record the outcome: 'win', 'loss', or 'draw'
tree.record_outcome('win')

# End the current path
tree.end_path()
```

You can also add moves in bulk using `add_moves`:

```python
moves = [Move("A"), Move("B"), Move("C")]
tree.start_path()
tree.add_moves(moves)
tree.record_outcome('win')
tree.end_path()
```

### 3.3 Retrieving Statistics

Get statistics for the current path:

```python
# Get statistics for the current path
stats = tree.get_statistics()
print(f"Visit count: {stats['visit_count']}")
print(f"Win rate: {stats['win_rate']}")

# Get the complete path
path = tree.get_complete_path()
print(f"Current path: {[str(move) for move in path]}")
```

### 3.4 Saving and Loading Trees

You can save a tree to a file and load it later:

```python
# Save the tree
tree.save("my_decision_tree.json")

# Load the tree
from fbtree import load_tree
loaded_tree = load_tree("my_decision_tree.json")
```

## 4. Intermediate Tutorial

### 4.1 Finding the Best Continuation

A powerful feature is finding the best next decision from the current position:

```python
# Find the best continuation from a specific position
starting_path = [Move("A"), Move("B")]
best_moves = tree.get_best_continuation(starting_path, top_n=3, min_visits=2)

print("Best continuations:")
for move_info in best_moves:
    print(f"{move_info['move']} - Win rate: {move_info['win_rate']:.2f}, Visits: {move_info['visits']}")
```

### 4.2 Move Frequency Analysis

Analyze the frequency of moves at a specific depth:

```python
# Get frequency statistics for the first move
first_move_freq = tree.get_move_frequency(depth=1)
print("First move frequencies:")
for move, count in first_move_freq.items():
    print(f"{move}: {count} times")

# Get frequency statistics for the second move
second_move_freq = tree.get_move_frequency(depth=2)
```

### 4.3 Generating Heatmaps

For board games or spatial decisions, you can generate heatmaps:

```python
# Generate a move heatmap for a 3x3 board game
heatmap = tree.generate_move_heatmap(board_size=3)
print("Move heatmap:")
for row in heatmap:
    print(" ".join(f"{val:3d}" for val in row))
```

### 4.4 Tree Visualization

Visualizing the tree structure helps in understanding decision patterns:

```python
# Text visualization (suitable for terminal viewing)
tree.visualize(max_depth=3)

# Generate Graphviz DOT format (can be converted to images)
dot_str = tree.visualize(max_depth=3, output_format='graphviz')
with open("tree_viz.dot", "w") as f:
    f.write(dot_str)
```

## 5. Advanced Features

### 5.1 Tree Pruning

As time goes on, the tree may become very large. You can prune infrequently used branches:

```python
# Prune paths with fewer than 5 visits
removed_count = tree.prune_tree(min_visits=5)
print(f"Removed {removed_count} low-frequency paths")

# Prune paths exceeding depth 10
removed_count = tree.prune_tree(max_depth=10)
```

### 5.2 Tree Merging

You can merge knowledge from two trees:

```python
# Create two trees
tree1 = create_tree()
tree2 = create_tree()

# Add paths to each...

# Merge tree2 into tree1
merged_count = tree1.merge(tree2, conflict_strategy='stats_sum')
print(f"Merged {merged_count} paths")
```

Merge strategy options:
- `stats_sum`: Combine statistics (visits, wins, etc.)
- `keep_max`: Keep the one with more visits
- `keep_current`: Keep the current tree's data

### 5.3 Path Diversity Analysis

Analyze the distribution and diversity of paths:

```python
# Get path diversity statistics
diversity = tree.analyze_path_diversity()
print(f"Maximum depth: {diversity['max_depth']}")
print(f"Average branching factor: {diversity['avg_branching_factor']:.2f}")
print(f"Leaf nodes: {diversity['leaf_nodes']}")
print(f"Depth distribution: {diversity['depth_distribution']}")
```

### 5.4 Path Simulation

Simulate paths to initialize or enhance the tree's knowledge:

```python
# Simulate a successful path, repeated 10 times
path = [Move("X"), Move("Y"), Move("Z")]
tree.simulate_path(path, outcome='win', visits=10)
```

## 6. Best Practices

### 6.1 Storage Selection

- **In-memory Storage (default)**: Faster, but data is lost when the program ends
  ```python
  tree = create_tree()  # Uses in-memory storage by default
  ```

- **SQLite Storage**: Persistent, suitable for long-term projects and larger datasets
  ```python
  tree = create_tree(storage_type='sqlite', db_path='my_database.db')
  ```

### 6.2 Performance Optimization

- Increase cache size for better performance on frequently accessed paths
  ```python
  tree = create_tree(max_cache_size=5000)
  ```

- Periodically prune the tree to reduce storage size and improve query speed
  ```python
  # Prune after every 10,000 additions
  if add_count % 10000 == 0:
      tree.prune_tree(min_visits=2)
  ```

### 6.3 Move Value Types

While `Move` can store values of any type, it's important to maintain consistent types within the same tree:

```python
# Good practice - consistently use strings
tree.add_move(Move("left"))
tree.add_move(Move("forward"))

# Good practice - consistently use numbers (like board coordinates)
tree.add_move(Move(1))
tree.add_move(Move(5))

# Avoid mixing types
# Not recommended: tree.add_move(Move("left")), then tree.add_move(Move(5))
```

### 6.4 Using Metadata

Metadata can store additional information that doesn't directly affect path matching:

```python
# Add a move with contextual information
tree.add_move(Move(
    "left",
    metadata={
        "timestamp": 1623451789,
        "environment": "rainy",
        "speed": 30
    }
))
```

## 7. Case Studies

### 7.1 Game AI Development

```python
from fbtree import create_tree, Move
import random

# Create a Tic-Tac-Toe game AI
tic_tac_toe_tree = create_tree()

# Simulate 1,000 games
for _ in range(1000):
    tic_tac_toe_tree.start_path()
    board = [None] * 9
    player = 'X'
    
    # Simulate a game
    while True:
        # Find available positions
        available = [i for i, val in enumerate(board) if val is None]
        if not available:
            tic_tac_toe_tree.record_outcome('draw')
            break
            
        # Choose a random position
        position = random.choice(available)
        tic_tac_toe_tree.add_move(Move(position))
        board[position] = player
        
        # Check for victory (simplified)
        # ...in a real game, you would check victory conditions
        
        # Switch players
        player = 'O' if player == 'X' else 'X'
    
    tic_tac_toe_tree.end_path()

# Find the best first move
best_first_move = tic_tac_toe_tree.get_best_continuation([], top_n=1)[0]
print(f"Best first move: {best_first_move['move'].value}, Win rate: {best_first_move['win_rate']:.2f}")

# Generate move heatmap
heatmap = tic_tac_toe_tree.generate_move_heatmap(board_size=3)
```

### 7.2 User Navigation Analysis

```python
from fbtree import create_tree, Move

# Create a user navigation analysis tree
navigation_tree = create_tree(storage_type='sqlite', db_path='user_paths.db')

def track_user_session(pages_visited, conversion_successful):
    """Record a user session"""
    navigation_tree.start_path()
    for page in pages_visited:
        navigation_tree.add_move(Move(page))
    
    outcome = 'win' if conversion_successful else 'loss'
    navigation_tree.record_outcome(outcome)
    navigation_tree.end_path()

# Record user sessions
track_user_session(['home', 'products', 'product_detail', 'cart', 'checkout'], True)
track_user_session(['home', 'search', 'product_detail', 'close'], False)

# Analyze the best paths starting from the home page
best_paths = navigation_tree.get_best_continuation([Move('home')], top_n=3)
print("Highest conversion rate paths:")
for path_info in best_paths:
    print(f"{path_info['move']} - Conversion rate: {path_info['win_rate']:.2f}")
```

## 8. API Reference

### 8.1 Core Functions

```python
# Create a new tree
create_tree(storage_type='memory', db_path=None, max_cache_size=1000)

# Load an existing tree
load_tree(file_path, storage_type='memory', db_path=None)
```

### 8.2 Path Building

```python
# Start a path
tree.start_path()

# Add a move
tree.add_move(Move(value, metadata=None))

# Add multiple moves
tree.add_moves(moves_list)

# Record outcome
tree.record_outcome(outcome)  # 'win', 'loss', or 'draw'

# End the path
tree.end_path()
```

### 8.3 Querying and Analysis

```python
# Get statistics
tree.get_statistics(fiber_id=None)

# Get complete path
tree.get_complete_path()

# Find best continuation
tree.get_best_continuation(current_path, top_n=3, min_visits=5)

# Get move frequency
tree.get_move_frequency(depth=1, min_visits=0)

# Generate heatmap
tree.generate_move_heatmap(board_size)

# Analyze path diversity
tree.analyze_path_diversity()
```

### 8.4 Management Functions

```python
# Save the tree
tree.save(file_path)

# Prune the tree
tree.prune_tree(min_visits=1, max_depth=None)

# Merge trees
tree.merge(other_tree, conflict_strategy='stats_sum')

# Simulate path
tree.simulate_path(path, outcome, visits=1)

# Visualize tree
tree.visualize(max_depth=5, output_format='text')
```

---

This tutorial is designed to help you progressively master FiberTree. From basic concepts to advanced applications, you can choose sections that match your current needs and skill level. If you have any questions or suggestions, please don't hesitate to contact us.

Happy decision path analysis!