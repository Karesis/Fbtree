# FiberTree

FiberTree is a flexible, extensible decision path management and analysis library designed for sequential decision problems. It's not just a Monte Carlo Tree Search (MCTS) implementation, but a complete decision analysis framework that helps you store, manage, analyze, and visualize decision paths.

## Key Features

- **Flexible Path Storage**: Supports both memory and SQLite storage backends to meet different application scenarios
- **Statistical Analysis**: Tracks visit counts, win rates, and other key metrics
- **Path Learning**: Identifies optimal decision paths based on historical data
- **Visualization**: Supports both text and graphical visualization of decision trees
- **Lightweight**: Core design is concise and efficient, easy to integrate
- **Extensible**: Modular design, easy to customize and extend

## Application Scenarios

FiberTree is suitable for various scenarios requiring sequential decision analysis:

- **Game AI**: Decision analysis for board games and strategy games
- **User Behavior Analysis**: Track user decision paths and discover behavior patterns
- **Business Process Optimization**: Analyze the effects of different decision paths
- **Risk Assessment**: Evaluate risks and returns of different decision sequences
- **Recommendation Systems**: Recommend optimal next steps based on historical paths

## Installation

```bash
pip install fbtree
```

Or install from source:

```bash
git clone https://github.com/yourusername/fbtree.git
cd fbtree
pip install -e .
```

## Quick Start

### Basic Usage

```python
from fbtree import create_tree, Move

# Create a new decision tree
tree = create_tree()

# Start a new path
tree.start_path()

# Add a series of decisions
tree.add_move(Move("left"))
tree.add_move(Move("straight"))
tree.add_move(Move("right"))

# Record the outcome of this path
tree.record_outcome('success')

# Get statistics for the current path
stats = tree.get_statistics()
print(stats)
```

### Analyzing Best Continuation

```python
# Starting from a specific path, analyze the best subsequent actions
starting_path = [Move("left"), Move("straight")]
best_moves = tree.get_best_continuation(starting_path)

for move in best_moves:
    print(f"Action: {move['move']}, Win Rate: {move['win_rate']}, Visits: {move['visits']}")
```

### Visualizing the Decision Tree

```python
# Visualize the tree as text
visualization = tree.visualize(max_depth=3, output_format='text')
print(visualization)

# Save a graphical visualization (requires graphviz)
tree.visualize(max_depth=3, output_format='graphviz', output_file='my_tree.png')
```

## Core Concepts

- **Move**: Represents a single decision or action in a decision sequence
- **Fiber**: Represents a node in the decision tree, containing statistical information and state
- **FiberTree**: The core class managing the entire decision tree, providing path addition, query, and analysis functionality

## Documentation

For more detailed documentation, please refer to the [docs/](docs/) directory or visit our online documentation.

## Examples

Check the [examples/](examples/) directory for more usage examples.

## Contributing

We welcome all forms of contributions. Please refer to [CONTRIBUTING.md](CONTRIBUTING.md) for information on how to participate in the project.

## License

This project is licensed under the [MIT License](LICENSE). 