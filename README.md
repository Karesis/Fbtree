# FiberTree

FiberTree is a path-oriented database for storing and analyzing sequential decision paths. It helps you track, analyze, and optimize decision processes by recording decision paths (fibers) and their outcomes.

## Core Concepts

FiberTree is built around three key concepts:

### Move
Represents a single decision or action in a sequence. Can store any type of value and optional metadata.

### Fiber
A container for a sequence of moves forming a decision path. Each Fiber contains move sequences and related statistics (visit count, win rate, etc.).

### FiberTree
A database that manages a collection of Fibers, providing functionality for adding, querying, analyzing, and visualizing decision paths.

## Installation

```bash
pip install fbtree
```

## Basic Usage

```python
from fbtree import create_tree, Move

# Create a tree
tree = create_tree()

# Record a decision path
tree.start_path()
tree.add_move(Move("A"))
tree.add_move(Move("B"))
tree.add_move(Move("C"))
tree.record_outcome('win')

# Get statistics
stats = tree.get_statistics()
print(f"Path statistics: {stats}")

# Find the best continuation from a specific position
best_moves = tree.get_best_continuation([Move("A")], top_n=2)
for move_info in best_moves:
    print(f"{move_info['move']} - Win rate: {move_info['win_rate']:.2f}")

# Save the tree
tree.save("my_decision_tree.json")
```

## Advanced Features

- **Statistical Analysis**: Track win rates, visit counts, and other metrics
- **Path Finding**: Search for specific decision paths and find optimal continuations
- **Move Frequency Analysis**: Analyze frequency of moves at specific depths
- **Path Diversity Analysis**: Get insights into path distribution and branching factors
- **Heatmap Generation**: Create heatmaps for board games
- **Tree Visualization**: Visualize the decision tree structure as text or Graphviz diagrams
- **Tree Pruning**: Remove low-value or overly deep paths
- **Tree Merging**: Combine knowledge from multiple trees

## Storage Options

FiberTree provides two storage backends:

### Memory Storage
```python
# Default in-memory storage
tree = create_tree()
```
- Fast, suitable for temporary analysis
- Data is lost when the program ends unless exported with `save`
- Ideal for smaller datasets

### SQLite Storage
```python
# SQLite persistent storage
tree = create_tree(storage_type='sqlite', db_path='my_database.db')
```
- Data persists on disk
- Supports larger datasets
- Suitable for long-term data collection and analysis

## Use Cases

FiberTree is particularly well-suited for:

1. **Game AI Development**: Store and analyze game decision trees
2. **User Behavior Analysis**: Track user navigation paths in apps or websites
3. **Sequential Decision Optimization**: Industrial process optimization, medical diagnosis paths
4. **Knowledge Representation**: Build decision knowledge bases and capture expert decision patterns

## API Reference

See the [full documentation](https://github.com/yourusername/fbtree#documentation) for complete API reference.

## License

MIT