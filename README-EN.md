# FiberTree - Decision Path Storage and Analysis Library

FiberTree is a database system focused on storing and analyzing sequential decision paths. It efficiently records, stores, and analyzes decision paths, and provides rich statistical functions and visualization tools to help you optimize decision processes.

## Documentation Navigation

📚 **Quick Access to All Documentation Resources**:

- **[API Reference](docs/en/api_reference.md)** - Detailed English API reference containing all classes and methods
- **[中文API参考文档](docs/api_reference.md)** - Detailed Chinese API reference documentation
- **[Getting Started Tutorial](docs/tutorials/en/getting_started.md)** - Quick guide for beginners to start using FiberTree
- **[Advanced Topics](docs/tutorials/en/advanced_topics.md)** - In-depth exploration of FiberTree's advanced features
- **[Example Code](examples/)** - Complete example code demonstrating how to use FiberTree

💡 **Code Examples**:
- **[Basic Usage Example](examples/correct_usage_en.py)** - English version of basic usage example
- **[基础用法示例](examples/correct_usage.py)** - Chinese version of basic usage example

## Features

- **Flexible Path Storage** - Support for storage and retrieval of any serializable decision path
- **Statistical Analysis** - Automatically calculate node visit frequency, win rates, and other statistics
- **Path Learning** - Optimize decision paths based on existing data
- **Visualization Capabilities** - Multiple ways to visualize decision trees (text, graphics)
- **High Performance** - Optimized storage engine, supporting memory and SQLite backends
- **Easy to Extend** - Clear API design for easy integration and extension
- **Path Analysis** - Deep analysis functions for decision paths
- **Multiple Visualization Options** - Support for text, Graphviz, and D3.js visualization formats

## Application Scenarios

- Move analysis and learning in board games
- Decision path optimization in recommendation systems
- User behavior path analysis
- Automated test scenario coverage analysis
- Decision support systems
- Path recording and analysis in reinforcement learning

## Installation

### Using pip

```bash
pip install fbtree
```

### From source

```bash
git clone https://github.com/yourusername/fbtree.git
cd fbtree
pip install -e .
```

## Basic Usage

```python
from fbtree import create_tree, Move

# Create a tree
tree = create_tree()

# Start building a path
tree.start_path()

# Add moves to the path
tree.add_move(Move("A1"))
tree.add_move(Move("B2"))
tree.add_move(Move("C3"))

# Record the outcome
tree.record_outcome("win")

# Get statistics
stats = tree.get_statistics()
print(stats)
```

## Analysis Features

```python
from fbtree import create_tree, Move, analyze_path_frequency, find_winning_paths, calculate_move_impact

# Create and populate a decision tree
tree = create_tree()
# ... add some paths and results ...

# Analyze move frequency at different depths
freq_data = analyze_path_frequency(tree.get_all_fibers())
print("Move frequency analysis:", freq_data)

# Find high win-rate paths
winning_paths = find_winning_paths(tree.get_all_fibers(), min_visits=5, min_win_rate=0.6)
print("High win-rate paths:", winning_paths)

# Calculate the impact of each move on win rates
impact_data = calculate_move_impact(tree.get_all_fibers())
print("Move impact analysis:", impact_data)
```

## Visualization Features

```python
from fbtree import create_tree, Move, visualize_tree_text, generate_path_summary
from fbtree import generate_graphviz, generate_d3_json

# Create and populate a decision tree
tree = create_tree()
# ... add some paths and results ...

# Text visualization
text_tree = visualize_tree_text(tree.get_all_fibers())
print(text_tree)

# Path summary
path_summary = generate_path_summary(tree.get_all_fibers(), min_visits=3)
print(path_summary)

# Graphviz visualization
dot_graph = generate_graphviz(tree.get_all_fibers(), max_depth=3, theme='light')
with open('tree_visualization.dot', 'w') as f:
    f.write(dot_graph)
    
# D3.js data generation
d3_data = generate_d3_json(tree.get_all_fibers())
with open('tree_data.json', 'w') as f:
    f.write(d3_data)
```

## Core Concepts

- **Fiber** - Represents a complete decision path, composed of a series of Moves
- **Move** - A single step or decision in the decision path
- **Tree** - Collection of all related decision paths
- **Storage** - Responsible for persistent storage of decision path data

## Contributing

Contributions in code, issue reporting, or feature suggestions are welcome. Please see the [contribution guidelines](CONTRIBUTING-EN.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details 