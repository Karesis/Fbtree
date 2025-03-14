# FiberTree Getting Started

This tutorial will help you quickly get started with the FiberTree library, learning its basic usage and core concepts.

## Installation

First, install FiberTree via pip:

```bash
pip install fbtree
```

## Basic Concepts

Before you start using FiberTree, let's understand some core concepts:

### Move

The `Move` class represents a single action or decision in the decision tree. It can contain any type of value to represent the specific action content.

```python
from fbtree import Move

# Create a string-type action
move1 = Move("turn left")

# Create a numeric action (like a board coordinate)
move2 = Move(15)  # For example, representing a position in Go

# You can also use more complex objects
move3 = Move({"x": 10, "y": 20, "action": "jump"})
```

### Fiber

A `Fiber` is a node in the decision tree, representing a state reached through a specific sequence of actions. Each Fiber contains statistical information such as visit count, win rate, etc.

### FiberTree

`FiberTree` is the core class of the entire library, managing Fiber nodes and providing functionality to add, query, and analyze paths.

## Basic Usage

### Creating a Tree

```python
from fbtree import create_tree

# Create a tree using memory storage
tree = create_tree(storage_type='memory')

# Or create a tree using SQLite storage (suitable for large decision trees)
tree = create_tree(storage_type='sqlite', db_path='my_tree.db')
```

### Recording Paths

There are two ways to record paths: step-by-step construction and one-time addition.

#### Step-by-Step Path Construction:

```python
# Start recording a new path
tree.start_path()

# Add a series of decisions
tree.add_move(Move("A"))
tree.add_move(Move("B"))
tree.add_move(Move("C"))

# Record the result (can be 'win', 'loss', 'draw', or custom)
tree.record_outcome('win')
```

#### One-Time Path Addition:

```python
# Create a complete path
path = [Move("A"), Move("B"), Move("C")]

# Simulate this path and record the result
tree.simulate_path(path=path, outcome='win')

# You can also specify the number of visits
tree.simulate_path(path=path, outcome='win', visits=5)
```

### Querying Statistics

```python
# Get statistics for the current path
stats = tree.get_statistics()
print(f"Visit count: {stats['visit_count']}")
print(f"Win rate: {stats['win_rate']}")

# Get statistics for a specific path
path = [Move("A"), Move("B")]
fiber_id = tree.find_path(path)
if fiber_id:
    stats = tree.get_statistics(fiber_id)
    print(stats)
```

### Analyzing Best Continuation

```python
# Starting from a specific path, get the best subsequent actions
starting_path = [Move("A")]
best_moves = tree.get_best_continuation(starting_path, top_n=3)

for i, move_info in enumerate(best_moves, 1):
    print(f"{i}. {move_info['move']} - Win Rate: {move_info['win_rate']:.2f}, Visits: {move_info['visits']}")
```

### Visualizing Decision Trees

```python
# Text visualization
text_viz = tree.visualize(max_depth=3, output_format='text')
print(text_viz)

# Export as an image (requires Graphviz)
tree.visualize(
    max_depth=4,
    output_format='graphviz',
    output_file='decision_tree.png'
)
```

## Persistence

FiberTree supports saving decision trees to files and loading from files:

```python
# Save the tree
tree.save('my_decision_tree.json')

# Load the tree
from fbtree import FiberTree
loaded_tree = FiberTree.import_from_json('my_decision_tree.json')
```

## Advanced Features

### Get Move Frequency

```python
# Get frequency statistics for first-level actions
freq = tree.get_move_frequency(depth=1)
print(freq)

# Only show actions that reach a visit threshold
freq = tree.get_move_frequency(depth=2, min_visits=5)
print(freq)
```

### Generate Heatmap Data

```python
# For board games, generate action heatmap data
heatmap = tree.generate_move_heatmap(board_size=15)  # 15x15 board

# You can visualize this heatmap using tools like matplotlib
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 10))
plt.imshow(heatmap, cmap='viridis')
plt.colorbar(label='Move Frequency')
plt.title('Board Heatmap')
plt.show()
```

### Pruning the Tree

For decision trees used over a long period, you may need to periodically prune nodes with low visit counts to improve performance:

```python
# Remove nodes with fewer than 5 visits
removed_count = tree.prune_tree(min_visits=5)
print(f"Removed {removed_count} low-frequency nodes")
```

## Next Steps

After mastering these basic concepts and usage, you can:

1. Check the [examples directory](../../examples/) for more examples
2. Read the [advanced topics tutorial](./advanced_topics.md) to learn about more complex usage
3. Refer to the [API documentation](../api_reference.md) for detailed interface descriptions

## Common Questions

### How do I save and restore decision trees between sessions?

Create a tree using the SQLite storage backend, which automatically saves data to the specified database file:

```python
tree = create_tree(storage_type='sqlite', db_path='persistent_tree.db')
```

Then in future sessions, create a tree using the same database path:

```python
tree = create_tree(storage_type='sqlite', db_path='persistent_tree.db')
# The tree will automatically load previous data
```

### How do I merge decision trees from different sources?

FiberTree provides merge functionality:

```python
# Merge another tree
tree.merge(another_tree, conflict_strategy='stats_sum')
```

### What if my decision tree gets too large and performance decreases?

1. Use the SQLite storage backend instead of memory storage
2. Periodically prune nodes with low visit counts: `tree.prune_tree(min_visits=threshold)`
3. Consider splitting the tree or implementing more fine-grained caching strategies 