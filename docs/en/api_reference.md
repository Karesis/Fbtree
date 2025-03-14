# FiberTree API Reference

This document provides detailed descriptions of the main classes and methods of the FiberTree library.

## Core Module

### `create_tree()`

Creates a new FiberTree instance.

**Parameters:**
- `storage_type` (str, optional): Storage backend type, options are 'memory' or 'sqlite'. Default is 'memory'.
- `db_path` (str, optional): SQLite database file path, only valid when storage_type is 'sqlite'.
- `cache_size` (int, optional): Cache size, default is 500.

**Returns:**
- FiberTree: The newly created tree instance.

**Example:**
```python
from fbtree import create_tree

# Create a memory tree
tree = create_tree()

# Create a SQLite tree
tree = create_tree(storage_type='sqlite', db_path='my_tree.db')
```

### `Move` Class

Represents a single action in the decision tree.

**Constructor:**
```python
Move(value)
```

**Parameters:**
- `value` (any type): The value of the action, can be any serializable data type.

**Attributes:**
- `value`: The value of the action.

**Methods:**
- `__str__()`: Returns the string representation of the action.
- `__eq__(other)`: Determines if two actions are equal.
- `serialize()`: Serializes the action to a JSON-compatible format.
- `deserialize(data)`: Restores the action from JSON data.

**Example:**
```python
from fbtree import Move

# Create an action
move = Move("turn left")

# Use numeric value
position_move = Move(42)

# Use complex data
complex_move = Move({"x": 10, "y": 20, "action": "jump"})
```

### `Fiber` Class

Represents a node in the decision tree, containing statistical information.

**Attributes:**
- `move`: The action that reaches this node.
- `stats`: A dictionary containing node statistics.
  - `visit_count`: Number of visits.
  - `win_count`: Number of wins.
  - `loss_count`: Number of losses.
  - `draw_count`: Number of draws.
  - `win_rate`: Win rate.

**Methods:**
- `update_stats(outcome, visits=1)`: Updates node statistics.
- `merge_stats(other_fiber, strategy='sum')`: Merges statistics from another node.
- `serialize()`: Serializes the node to a JSON-compatible format.
- `deserialize(data)`: Restores the node from JSON data.

### `FiberTree` Class

The core class of the decision tree, managing nodes and providing analysis functionality.

#### Basic Operations

**Constructor:**
```python
FiberTree(storage_type='memory', db_path=None, cache_size=500)
```

**Parameters:**
- `storage_type` (str): Storage backend type, options are 'memory' or 'sqlite'.
- `db_path` (str, optional): SQLite database file path.
- `cache_size` (int): Cache size.

**Attributes:**
- `storage`: Storage backend instance.
- `_current_path`: Path currently being constructed.
- `_adding_mode`: Whether in adding mode.

**Path Management Methods:**

- `start_path()`: Starts a new path.
  - **Returns:** None

- `add_move(move)`: Adds an action to the current path.
  - **Parameters:**
    - `move` (Move): The action to add.
  - **Returns:** None

- `get_current_path()`: Gets the current path.
  - **Returns:** List[Move], list of actions in the current path.

- `get_complete_path()`: Gets the complete current path, including action content.
  - **Returns:** List[Move], current path with all actions.

- `record_outcome(outcome, visits=1)`: Records the result of the current path.
  - **Parameters:**
    - `outcome` (str): Path result, can be 'win', 'loss', 'draw', or custom value.
    - `visits` (int, optional): Number of visits, default is 1.
  - **Returns:** None

- `simulate_path(path, outcome='win', visits=1, update_stats=True)`: Simulates a complete path.
  - **Parameters:**
    - `path` (List[Move]): Action sequence.
    - `outcome` (str, optional): Path result, default is 'win'.
    - `visits` (int, optional): Number of visits, default is 1.
    - `update_stats` (bool, optional): Whether to update statistics, default is True.
  - **Returns:** str, fiber_id of the path endpoint.

**Query Methods:**

- `find_path(path)`: Finds the node ID matching the given path.
  - **Parameters:**
    - `path` (List[Move]): Action sequence to find.
  - **Returns:** str or None, fiber_id if found, None otherwise.

- `get_statistics(fiber_id=None)`: Gets node statistics.
  - **Parameters:**
    - `fiber_id` (str, optional): Node ID, default is the endpoint of the current path.
  - **Returns:** Dict, dictionary containing node statistics.

- `get_path_statistics(path)`: Gets statistics for a specific path.
  - **Parameters:**
    - `path` (List[Move]): Action sequence.
  - **Returns:** Dict, dictionary containing statistics, or None if the path doesn't exist.

#### Analysis Methods

- `get_best_continuation(path=None, top_n=3, min_visits=0)`: Gets the best subsequent actions.
  - **Parameters:**
    - `path` (List[Move], optional): Starting path, default is the current path.
    - `top_n` (int, optional): Number of best actions to return, default is 3.
    - `min_visits` (int, optional): Minimum visit count threshold, default is 0.
  - **Returns:** List[Dict], list containing subsequent action information, sorted by win rate.

- `get_move_frequency(depth=1, min_visits=0)`: Gets action frequency at a specific depth.
  - **Parameters:**
    - `depth` (int, optional): Depth, default is 1.
    - `min_visits` (int, optional): Minimum visit count threshold, default is 0.
  - **Returns:** Dict, mapping of action values to frequencies.

- `generate_move_heatmap(board_size)`: Generates action heatmap data.
  - **Parameters:**
    - `board_size` (int): Board size.
  - **Returns:** List[List[int]], two-dimensional heatmap data.

- `get_common_path_statistics(min_visits=10, max_paths=100)`: Gets statistics for common paths.
  - **Parameters:**
    - `min_visits` (int, optional): Minimum visit count threshold, default is 10.
    - `max_paths` (int, optional): Maximum number of paths to return, default is 100.
  - **Returns:** List[Dict], list containing path statistics, sorted by visit count.

- `analyze_path_diversity()`: Analyzes the diversity of tree paths.
  - **Returns:** Dict, dictionary containing diversity metrics.

#### Maintenance Methods

- `prune_tree(min_visits=1, custom_condition=None)`: Prunes low-frequency nodes from the tree.
  - **Parameters:**
    - `min_visits` (int, optional): Minimum visit count threshold, default is 1.
    - `custom_condition` (function, optional): Custom pruning condition function.
  - **Returns:** int, number of nodes removed.

- `merge(other_tree, conflict_strategy='stats_sum')`: Merges another tree.
  - **Parameters:**
    - `other_tree` (FiberTree): Tree to merge.
    - `conflict_strategy` (str, optional): Conflict resolution strategy, default is 'stats_sum'.
  - **Returns:** int, number of nodes merged.

- `start_batch_mode()`: Starts batch operation mode.
  - **Returns:** None

- `end_batch_mode()`: Ends batch operation mode, updates statistics.
  - **Returns:** None

#### Persistence Methods

- `save(file_path)`: Saves the tree to a JSON file.
  - **Parameters:**
    - `file_path` (str): File path.
  - **Returns:** None

- `export_to_json(file_path)`: Exports the tree to a JSON file.
  - **Parameters:**
    - `file_path` (str): File path.
  - **Returns:** None

- `import_from_json(file_path, storage_type='memory', db_path=None)`: Imports a tree from a JSON file.
  - **Parameters:**
    - `file_path` (str): File path.
    - `storage_type` (str, optional): Storage backend type, default is 'memory'.
    - `db_path` (str, optional): SQLite database path.
  - **Returns:** FiberTree, imported tree instance.

#### Visualization Methods

- `visualize(max_depth=None, output_format='text', output_file=None)`: Visualizes the decision tree.
  - **Parameters:**
    - `max_depth` (int, optional): Maximum visualization depth, default is None (all).
    - `output_format` (str, optional): Output format, options are 'text' or 'graphviz', default is 'text'.
    - `output_file` (str, optional): Output file path, default is None.
  - **Returns:** 
    - If format is 'text', returns a string.
    - If format is 'graphviz' and output_file is None, returns a Graphviz DOT string.
    - If format is 'graphviz' and output_file is specified, saves the image to the file and returns None.

## Storage Module

### `StorageBase` Class (Abstract Base Class)

Interface definition for storage backends.

**Methods:**
- `get_fiber(fiber_id)`: Gets a node.
- `save_fiber(fiber_id, fiber)`: Saves a node.
- `remove_fiber(fiber_id)`: Deletes a node.
- `get_all_fibers()`: Gets all nodes.
- `clear()`: Clears the storage.

### `MemoryStorage` Class

Memory storage backend implementation.

**Methods:**
- Implements all methods of `StorageBase`.
- Uses Python dictionary to store nodes.

### `SQLiteStorage` Class

SQLite storage backend implementation.

**Constructor:**
```python
SQLiteStorage(db_path, table_name='fibers')
```

**Parameters:**
- `db_path` (str): SQLite database file path.
- `table_name` (str, optional): Table name, default is 'fibers'.

**Methods:**
- Implements all methods of `StorageBase`.
- Uses SQLite database to store nodes.

## Utilities Module

### `LRUCache` Class

Implements a least recently used cache.

**Constructor:**
```python
LRUCache(max_size=100)
```

**Parameters:**
- `max_size` (int, optional): Maximum number of cache items, default is 100.

**Methods:**
- `get(key)`: Gets a cache item.
- `set(key, value)`: Sets a cache item.
- `clear()`: Clears the cache.

### Serialization Functions

- `serialize_fiber(fiber)`: Serializes a Fiber object to a JSON-compatible format.
- `deserialize_fiber(data)`: Restores a Fiber object from JSON data.
- `serialize_move(move)`: Serializes a Move object to a JSON-compatible format.
- `deserialize_move(data)`: Restores a Move object from JSON data.

## Visualization Module

### Text Visualization

- `visualize_text(tree, max_depth=None)`: Generates a text representation of the tree.

**Parameters:**
- `tree` (FiberTree): Tree to visualize.
- `max_depth` (int, optional): Maximum visualization depth, default is None (all).

**Returns:**
- str: Text representation of the tree.

### Graphviz Visualization

- `generate_graphviz(tree, max_depth=None)`: Generates a Graphviz DOT representation of the tree.

**Parameters:**
- `tree` (FiberTree): Tree to visualize.
- `max_depth` (int, optional): Maximum visualization depth, default is None (all).

**Returns:**
- str: Graphviz DOT representation of the tree.

- `save_graphviz(dot_string, output_file, format='png')`: Saves a Graphviz image.

**Parameters:**
- `dot_string` (str): Graphviz DOT string.
- `output_file` (str): Output file path.
- `format` (str, optional): Output format, default is 'png'.

**Returns:**
- None

## Analysis Module

### `analyze_path_frequency()`

Analyzes the frequency distribution of moves at different depths.

**Function Signature:**
```python
analyze_path_frequency(fibers, depth=None)
```

**Parameters:**
- `fibers` (Dict[str, Fiber]): Dictionary of all Fibers, obtained using `tree.get_all_fibers()`.
- `depth` (int, optional): Maximum depth to analyze, None means analyze all depths.

**Returns:**
- Dict[int, Dict[str, int]]: Move frequency at each depth, in the format {depth: {move: frequency}}.

**Example:**
```python
from fbtree import create_tree, analyze_path_frequency

tree = create_tree()
# ... add paths and results ...

freq_data = analyze_path_frequency(tree.get_all_fibers())
print(freq_data)
```

### `find_winning_paths()`

Finds paths with high win rates.

**Function Signature:**
```python
find_winning_paths(fibers, min_visits=1, min_win_rate=0.5)
```

**Parameters:**
- `fibers` (Dict[str, Fiber]): Dictionary of all Fibers, obtained using `tree.get_all_fibers()`.
- `min_visits` (int, optional): Minimum visit count to filter low-confidence paths, default is 1.
- `min_win_rate` (float, optional): Minimum win rate threshold, default is 0.5.

**Returns:**
- List[Tuple[List[Move], float]]: List of qualifying paths, each including a move sequence and win rate.

**Example:**
```python
from fbtree import create_tree, find_winning_paths

tree = create_tree()
# ... add paths and results ...

winning_paths = find_winning_paths(tree.get_all_fibers(), min_visits=5, min_win_rate=0.6)
for path, win_rate in winning_paths:
    print(f"Path: {path}, Win Rate: {win_rate:.2f}")
```

### `calculate_move_impact()`

Calculates the impact of each move on win rates.

**Function Signature:**
```python
calculate_move_impact(fibers)
```

**Parameters:**
- `fibers` (Dict[str, Fiber]): Dictionary of all Fibers, obtained using `tree.get_all_fibers()`.

**Returns:**
- Dict[str, Dict[str, Union[float, int]]]: Impact statistics for each move, in the format {move: {'win_rate': win_rate, 'count': appearance_count}}.

**Example:**
```python
from fbtree import create_tree, calculate_move_impact

tree = create_tree()
# ... add paths and results ...

impact_data = calculate_move_impact(tree.get_all_fibers())
for move, stats in impact_data.items():
    print(f"Move {move}: Win Rate={stats['win_rate']:.2f}, Count={stats['count']}")
```

## Visualization Module

### Text Visualization

#### `visualize_tree_text()`

Generates a text representation of the tree.

**Function Signature:**
```python
visualize_tree_text(fibers, max_depth=None, indent=2)
```

**Parameters:**
- `fibers` (Dict[str, Fiber]): Dictionary of all Fibers, obtained using `tree.get_all_fibers()`.
- `max_depth` (int, optional): Maximum visualization depth, None means no limit.
- `indent` (int, optional): Number of spaces for indentation, default is 2.

**Returns:**
- str: Text representation of the tree.

**Example:**
```python
from fbtree import create_tree, visualize_tree_text

tree = create_tree()
# ... add paths and results ...

text_viz = visualize_tree_text(tree.get_all_fibers(), max_depth=3)
print(text_viz)
```

#### `generate_path_summary()`

Generates path summary information.

**Function Signature:**
```python
generate_path_summary(fibers, min_visits=1, sort_by='win_rate')
```

**Parameters:**
- `fibers` (Dict[str, Fiber]): Dictionary of all Fibers, obtained using `tree.get_all_fibers()`.
- `min_visits` (int, optional): Minimum visit count threshold, default is 1.
- `sort_by` (str, optional): Sorting criterion, 'win_rate' or 'visits', default is 'win_rate'.

**Returns:**
- str: Path summary text.

**Example:**
```python
from fbtree import create_tree, generate_path_summary

tree = create_tree()
# ... add paths and results ...

summary = generate_path_summary(tree.get_all_fibers(), min_visits=3, sort_by='visits')
print(summary)
```

### Graphical Visualization

#### `generate_graphviz()`

Generates a Graphviz DOT format representation of the tree.

**Function Signature:**
```python
generate_graphviz(fibers, root_id='root', max_depth=None, include_stats=True, theme='light')
```

**Parameters:**
- `fibers` (Dict[str, Fiber]): Dictionary of all Fibers, obtained using `tree.get_all_fibers()`.
- `root_id` (str, optional): ID of the root node, default is 'root'.
- `max_depth` (int, optional): Maximum visualization depth, None means no limit.
- `include_stats` (bool, optional): Whether to include statistics, default is True.
- `theme` (str, optional): Visualization theme, 'light' or 'dark', default is 'light'.

**Returns:**
- str: Graphviz DOT format representation.

**Example:**
```python
from fbtree import create_tree, generate_graphviz

tree = create_tree()
# ... add paths and results ...

dot_string = generate_graphviz(tree.get_all_fibers(), max_depth=3, theme='dark')
with open('tree.dot', 'w') as f:
    f.write(dot_string)
```

#### `generate_d3_json()`

Generates JSON data for D3.js visualization.

**Function Signature:**
```python
generate_d3_json(fibers, root_id='root', max_depth=None)
```

**Parameters:**
- `fibers` (Dict[str, Fiber]): Dictionary of all Fibers, obtained using `tree.get_all_fibers()`.
- `root_id` (str, optional): ID of the root node, default is 'root'.
- `max_depth` (int, optional): Maximum visualization depth, None means no limit.

**Returns:**
- str: JSON string, usable for D3.js tree diagrams.

**Example:**
```python
from fbtree import create_tree, generate_d3_json

tree = create_tree()
# ... add paths and results ...

json_data = generate_d3_json(tree.get_all_fibers())
with open('tree_data.json', 'w') as f:
    f.write(json_data)
``` 