# FiberTree API参考

本文档提供FiberTree库的主要类和方法的详细说明。

## 核心模块

### `create_tree()`

创建一个新的FiberTree实例。

**参数:**
- `storage_type` (str, 可选): 存储后端类型，可选值为 'memory' 或 'sqlite'。默认为 'memory'。
- `db_path` (str, 可选): SQLite数据库文件路径，仅当storage_type为'sqlite'时有效。
- `cache_size` (int, 可选): 缓存大小，默认为500。

**返回:**
- FiberTree: 新创建的树实例。

**示例:**
```python
from fbtree import create_tree

# 创建内存树
tree = create_tree()

# 创建SQLite树
tree = create_tree(storage_type='sqlite', db_path='my_tree.db')
```

### `Move`类

表示决策树中的单一动作。

**构造函数:**
```python
Move(value)
```

**参数:**
- `value` (任意类型): 动作的值，可以是任何可序列化的数据类型。

**属性:**
- `value`: 动作的值。

**方法:**
- `__str__()`: 返回动作的字符串表示。
- `__eq__(other)`: 判断两个动作是否相等。
- `serialize()`: 将动作序列化为JSON兼容格式。
- `deserialize(data)`: 从JSON数据还原动作。

**示例:**
```python
from fbtree import Move

# 创建一个动作
move = Move("向左转")

# 使用数值
position_move = Move(42)

# 使用复杂数据
complex_move = Move({"x": 10, "y": 20, "action": "jump"})
```

### `Fiber`类

表示决策树中的一个节点，包含路径和统计信息。

**构造函数:**
```python
Fiber(moves=None, stats=None)
```

**参数:**
- `moves` (List[Move], 可选): 移动序列，默认为空列表。
- `stats` (Dict, 可选): 统计信息，默认为空字典。

**属性:**
- `moves`: 移动序列。
- `stats`: 统计信息字典。

**方法:**
- `add_move(move)`: 添加移动到序列。
- `is_empty()`: 检查是否为空路径。
- `get_path_string()`: 获取路径的字符串表示。
- `get_win_rate()`: 计算胜率。
- `update_stats(outcome)`: 更新统计信息。
- `merge_stats(other_fiber)`: 合并另一个Fiber的统计信息。
- `serialize()`: 将Fiber序列化为JSON兼容格式。
- `deserialize(data)`: 从JSON数据还原Fiber。

### `FiberTree`类

决策树的主类，管理路径和提供分析功能。

**构造函数:**
```python
FiberTree(storage_type='memory', db_path=None, max_cache_size=1000)
```

**参数:**
- `storage_type` (str, 可选): 存储后端类型，可选值为 'memory' 或 'sqlite'。默认为 'memory'。
- `db_path` (str, 可选): SQLite数据库文件路径，仅当storage_type为'sqlite'时有效。
- `max_cache_size` (int, 可选): 最大缓存大小，默认为1000。

#### 路径管理方法

- `start_path(moves=None)`: 开始一个新路径。
  - **参数:**
    - `moves` (List[Move], 可选): 初始移动序列，默认为None。
  - **返回:** None

- `add_move(move)`: 向当前路径添加一个移动。
  - **参数:**
    - `move` (Move): 要添加的移动。
  - **返回:** None

- `record_outcome(outcome='win', **kwargs)`: 记录当前路径的结果。
  - **参数:**
    - `outcome` (str或Dict, 可选): 结果标识符或结果字典，默认为'win'。
    - `**kwargs`: 额外的结果数据，将被添加到outcome字典中。
  - **返回:** None

- `get_path()`: 获取当前路径。
  - **返回:** List[Move]，当前路径的移动列表。

- `clear_path()`: 清除当前路径。
  - **返回:** None

#### 查询方法

- `get_fiber(moves=None)`: 获取特定路径的Fiber。
  - **参数:**
    - `moves` (List[Move], 可选): 要查询的移动序列，默认为当前路径。
  - **返回:** Fiber对象，如果路径不存在则返回None。

- `get_all_fibers()`: 获取所有存储的Fiber。
  - **返回:** Dict，fiber_id到Fiber对象的映射。

- `get_statistics(path=None)`: 获取特定路径的统计信息。
  - **参数:**
    - `path` (List[Move], 可选): 要查询的路径，默认为当前路径。
  - **返回:** Dict，包含统计信息的字典，如果路径不存在则返回None。

#### 分析方法

- `get_best_continuation(path=None, top_n=3, min_visits=0)`: 获取最佳后续动作。
  - **参数:**
    - `path` (List[Move], 可选): 起始路径，默认为当前路径。
    - `top_n` (int, 可选): 返回的最佳动作数量，默认为3。
    - `min_visits` (int, 可选): 最小访问次数阈值，默认为0。
  - **返回:** List[Dict]，包含后续动作信息的列表，按胜率排序。

- `get_move_frequency(depth=1, min_visits=0)`: 获取特定深度的动作频率。
  - **参数:**
    - `depth` (int, 可选): 深度，默认为1。
    - `min_visits` (int, 可选): 最小访问次数阈值，默认为0。
  - **返回:** Dict，动作值到频率的映射。

- `generate_move_heatmap(board_size)`: 生成动作热图数据。
  - **参数:**
    - `board_size` (int): 棋盘大小。
  - **返回:** List[List[int]]，二维热图数据。

- `get_common_path_statistics(min_visits=10, max_paths=100)`: 获取常用路径统计。
  - **参数:**
    - `min_visits` (int, 可选): 最小访问次数阈值，默认为10。
    - `max_paths` (int, 可选): 最大返回路径数，默认为100。
  - **返回:** List[Dict]，包含路径统计信息的列表，按访问次数排序。

- `analyze_path_diversity()`: 分析树的路径多样性。
  - **返回:** Dict，包含多样性指标的字典。

#### 维护方法

- `prune_tree(min_visits=1, custom_condition=None)`: 修剪树中低频节点。
  - **参数:**
    - `min_visits` (int, 可选): 最小访问次数阈值，默认为1。
    - `custom_condition` (函数, 可选): 自定义修剪条件函数。
  - **返回:** int，移除的节点数量。

- `merge(other_tree, conflict_strategy='stats_sum')`: 合并另一棵树。
  - **参数:**
    - `other_tree` (FiberTree): 要合并的树。
    - `conflict_strategy` (str, 可选): 冲突解决策略，默认为'stats_sum'。
  - **返回:** int，合并的节点数量。

- `start_batch_mode()`: 开始批量操作模式。
  - **返回:** None

- `end_batch_mode()`: 结束批量操作模式，更新统计信息。
  - **返回:** None

#### 持久化方法

- `save(file_path)`: 将树保存到JSON文件。
  - **参数:**
    - `file_path` (str): 文件路径。
  - **返回:** None

- `export_to_json(file_path)`: 导出树到JSON文件。
  - **参数:**
    - `file_path` (str): 文件路径。
  - **返回:** None

- `import_from_json(file_path, storage_type='memory', db_path=None)`: 从JSON文件导入树。
  - **参数:**
    - `file_path` (str): 文件路径。
    - `storage_type` (str, 可选): 存储后端类型，默认为'memory'。
    - `db_path` (str, 可选): SQLite数据库路径。
  - **返回:** FiberTree，导入的树实例。

#### 可视化方法

- `visualize(max_depth=None, output_format='text', output_file=None)`: 可视化决策树。
  - **参数:**
    - `max_depth` (int, 可选): 最大可视化深度，默认为None（全部）。
    - `output_format` (str, 可选): 输出格式，可选值为'text'或'graphviz'，默认为'text'。
    - `output_file` (str, 可选): 输出文件路径，默认为None。
  - **返回:** 
    - 如果format为'text'，返回字符串。
    - 如果format为'graphviz'且output_file为None，返回Graphviz DOT字符串。
    - 如果format为'graphviz'且指定了output_file，将图像保存到文件并返回None。

## 存储模块

### `StorageBase`类 (抽象基类)

存储后端的接口定义。

**方法:**
- `get_fiber(fiber_id)`: 获取节点。
- `save_fiber(fiber_id, fiber)`: 保存节点。
- `remove_fiber(fiber_id)`: 删除节点。
- `get_all_fibers()`: 获取所有节点。
- `clear()`: 清空存储。

### `MemoryStorage`类

内存存储后端实现。

**方法:**
- 实现了`StorageBase`的所有方法。
- 使用Python字典存储节点。

### `SQLiteStorage`类

SQLite存储后端实现。

**构造函数:**
```python
SQLiteStorage(db_path, table_name='fibers')
```

**参数:**
- `db_path` (str): SQLite数据库文件路径。
- `table_name` (str, 可选): 表名，默认为'fibers'。

**方法:**
- 实现了`StorageBase`的所有方法。
- 使用SQLite数据库存储节点。

## 工具模块

### `LRUCache`类

实现最近最少使用缓存。

**构造函数:**
```python
LRUCache(max_size=100)
```

**参数:**
- `max_size` (int, 可选): 最大缓存项数，默认为100。

**方法:**
- `get(key)`: 获取缓存项。
- `set(key, value)`: 设置缓存项。
- `clear()`: 清空缓存。

### 序列化函数

- `serialize_fiber(fiber)`: 将Fiber对象序列化为JSON兼容格式。
- `deserialize_fiber(data)`: 从JSON数据还原Fiber对象。
- `serialize_move(move)`: 将Move对象序列化为JSON兼容格式。
- `deserialize_move(data)`: 从JSON数据还原Move对象。

## 分析模块

### `analyze_path_frequency()`

分析不同深度上移动的频率分布。

**函数签名:**
```python
analyze_path_frequency(fibers, depth=None)
```

**参数:**
- `fibers` (Dict[str, Fiber]): 包含所有Fiber的字典，使用`tree.get_all_fibers()`获取。
- `depth` (int, 可选): 要分析的最大深度，None表示分析所有深度。

**返回:**
- Dict[int, Dict[str, int]]: 每个深度的移动频率，格式为 {深度: {移动: 频率}}。

**示例:**
```python
from fbtree import create_tree, analyze_path_frequency

tree = create_tree()
# ... 添加路径和结果 ...

freq_data = analyze_path_frequency(tree.get_all_fibers())
print(freq_data)
```

### `find_winning_paths()`

寻找胜率高的路径。

**函数签名:**
```python
find_winning_paths(fibers, min_visits=1, min_win_rate=0.5)
```

**参数:**
- `fibers` (Dict[str, Fiber]): 包含所有Fiber的字典，使用`tree.get_all_fibers()`获取。
- `min_visits` (int, 可选): 最小访问次数，用于过滤低置信度的路径，默认为1。
- `min_win_rate` (float, 可选): 最小胜率阈值，默认为0.5。

**返回:**
- List[Tuple[List[Move], float]]: 符合条件的路径列表，每项包含移动序列和胜率。

**示例:**
```python
from fbtree import create_tree, find_winning_paths

tree = create_tree()
# ... 添加路径和结果 ...

winning_paths = find_winning_paths(tree.get_all_fibers(), min_visits=5, min_win_rate=0.6)
for path, win_rate in winning_paths:
    print(f"路径: {path}, 胜率: {win_rate:.2f}")
```

### `calculate_move_impact()`

计算每个移动对胜率的影响。

**函数签名:**
```python
calculate_move_impact(fibers)
```

**参数:**
- `fibers` (Dict[str, Fiber]): 包含所有Fiber的字典，使用`tree.get_all_fibers()`获取。

**返回:**
- Dict[str, Dict[str, Union[float, int]]]: 每个移动的影响统计，格式为 {移动: {'win_rate': 胜率, 'count': 出现次数}}。

**示例:**
```python
from fbtree import create_tree, calculate_move_impact

tree = create_tree()
# ... 添加路径和结果 ...

impact_data = calculate_move_impact(tree.get_all_fibers())
for move, stats in impact_data.items():
    print(f"移动 {move}: 胜率={stats['win_rate']:.2f}, 次数={stats['count']}")
```

## 可视化模块

### 文本可视化

#### `visualize_tree_text()`

生成树的文本表示。

**函数签名:**
```python
visualize_tree_text(fibers, max_depth=None, indent=2)
```

**参数:**
- `fibers` (Dict[str, Fiber]): 包含所有Fiber的字典，使用`tree.get_all_fibers()`获取。
- `max_depth` (int, 可选): 最大可视化深度，None表示不限制。
- `indent` (int, 可选): 缩进空格数，默认为2。

**返回:**
- str: 树的文本表示。

**示例:**
```python
from fbtree import create_tree, visualize_tree_text

tree = create_tree()
# ... 添加路径和结果 ...

text_viz = visualize_tree_text(tree.get_all_fibers(), max_depth=3)
print(text_viz)
```

#### `generate_path_summary()`

生成路径摘要信息。

**函数签名:**
```python
generate_path_summary(fibers, min_visits=1, sort_by='win_rate')
```

**参数:**
- `fibers` (Dict[str, Fiber]): 包含所有Fiber的字典，使用`tree.get_all_fibers()`获取。
- `min_visits` (int, 可选): 最小访问次数阈值，默认为1。
- `sort_by` (str, 可选): 排序依据，'win_rate'或'visits'，默认为'win_rate'。

**返回:**
- str: 路径摘要文本。

**示例:**
```python
from fbtree import create_tree, generate_path_summary

tree = create_tree()
# ... 添加路径和结果 ...

summary = generate_path_summary(tree.get_all_fibers(), min_visits=3, sort_by='visits')
print(summary)
```

### 图形可视化

#### `generate_graphviz()`

生成Graphviz DOT格式的树表示。

**函数签名:**
```python
generate_graphviz(fibers, root_id='root', max_depth=None, include_stats=True, theme='light')
```

**参数:**
- `fibers` (Dict[str, Fiber]): 包含所有Fiber的字典，使用`tree.get_all_fibers()`获取。
- `root_id` (str, 可选): 根节点的ID，默认为'root'。
- `max_depth` (int, 可选): 最大可视化深度，None表示不限制。
- `include_stats` (bool, 可选): 是否包含统计信息，默认为True。
- `theme` (str, 可选): 可视化主题，'light'或'dark'，默认为'light'。

**返回:**
- str: Graphviz DOT格式表示。

**示例:**
```python
from fbtree import create_tree, generate_graphviz

tree = create_tree()
# ... 添加路径和结果 ...

dot_string = generate_graphviz(tree.get_all_fibers(), max_depth=3, theme='dark')
with open('tree.dot', 'w') as f:
    f.write(dot_string)
```

#### `generate_d3_json()`

生成用于D3.js可视化的JSON数据。

**函数签名:**
```python
generate_d3_json(fibers, root_id='root', max_depth=None)
```

**参数:**
- `fibers` (Dict[str, Fiber]): 包含所有Fiber的字典，使用`tree.get_all_fibers()`获取。
- `root_id` (str, 可选): 根节点的ID，默认为'root'。
- `max_depth` (int, 可选): 最大可视化深度，None表示不限制。

**返回:**
- str: JSON字符串，可用于D3.js树形图。

**示例:**
```python
from fbtree import create_tree, generate_d3_json

tree = create_tree()
# ... 添加路径和结果 ...

json_data = generate_d3_json(tree.get_all_fibers())
with open('tree_data.json', 'w') as f:
    f.write(json_data)
``` 