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

表示决策树中的节点，包含统计信息。

**属性:**
- `move`: 到达此节点的动作。
- `stats`: 包含节点统计信息的字典。
  - `visit_count`: 访问次数。
  - `win_count`: 胜利次数。
  - `loss_count`: 失败次数。
  - `draw_count`: 平局次数。
  - `win_rate`: 胜率。

**方法:**
- `update_stats(outcome, visits=1)`: 更新节点统计信息。
- `merge_stats(other_fiber, strategy='sum')`: 合并另一个节点的统计信息。
- `serialize()`: 将节点序列化为JSON兼容格式。
- `deserialize(data)`: 从JSON数据还原节点。

### `FiberTree`类

决策树的核心类，管理节点和提供分析功能。

#### 基本操作

**构造函数:**
```python
FiberTree(storage_type='memory', db_path=None, cache_size=500)
```

**参数:**
- `storage_type` (str): 存储后端类型，可选值为 'memory' 或 'sqlite'。
- `db_path` (str, 可选): SQLite数据库文件路径。
- `cache_size` (int): 缓存大小。

**属性:**
- `storage`: 存储后端实例。
- `_current_path`: 当前构建中的路径。
- `_adding_mode`: 是否处于添加模式。

**路径管理方法:**

- `start_path()`: 开始一个新路径。
  - **返回:** None

- `add_move(move)`: 向当前路径添加一个动作。
  - **参数:**
    - `move` (Move): 要添加的动作。
  - **返回:** None

- `get_current_path()`: 获取当前路径。
  - **返回:** List[Move]，当前路径中的动作列表。

- `get_complete_path()`: 获取完整的当前路径，包括动作内容。
  - **返回:** List[Move]，包含所有动作的当前路径。

- `record_outcome(outcome, visits=1)`: 记录当前路径的结果。
  - **参数:**
    - `outcome` (str): 路径结果，可以是 'win', 'loss', 'draw' 或自定义值。
    - `visits` (int, 可选): 访问次数，默认为1。
  - **返回:** None

- `simulate_path(path, outcome='win', visits=1, update_stats=True)`: 模拟一条完整路径。
  - **参数:**
    - `path` (List[Move]): 动作序列。
    - `outcome` (str, 可选): 路径结果，默认为'win'。
    - `visits` (int, 可选): 访问次数，默认为1。
    - `update_stats` (bool, 可选): 是否更新统计信息，默认为True。
  - **返回:** str，路径终点的fiber_id。

**查询方法:**

- `find_path(path)`: 查找与给定路径匹配的节点ID。
  - **参数:**
    - `path` (List[Move]): 要查找的动作序列。
  - **返回:** str 或 None，如果找到则返回fiber_id，否则返回None。

- `get_statistics(fiber_id=None)`: 获取节点的统计信息。
  - **参数:**
    - `fiber_id` (str, 可选): 节点ID，默认为当前路径的终点。
  - **返回:** Dict，包含节点统计信息的字典。

- `get_path_statistics(path)`: 获取特定路径的统计信息。
  - **参数:**
    - `path` (List[Move]): 动作序列。
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

## 可视化模块

### 文本可视化

- `visualize_text(tree, max_depth=None)`: 生成树的文本表示。

**参数:**
- `tree` (FiberTree): 要可视化的树。
- `max_depth` (int, 可选): 最大可视化深度，默认为None（全部）。

**返回:**
- str: 树的文本表示。

### Graphviz可视化

- `generate_graphviz(tree, max_depth=None)`: 生成树的Graphviz DOT表示。

**参数:**
- `tree` (FiberTree): 要可视化的树。
- `max_depth` (int, 可选): 最大可视化深度，默认为None（全部）。

**返回:**
- str: 树的Graphviz DOT表示。

- `save_graphviz(dot_string, output_file, format='png')`: 保存Graphviz图像。

**参数:**
- `dot_string` (str): Graphviz DOT字符串。
- `output_file` (str): 输出文件路径。
- `format` (str, 可选): 输出格式，默认为'png'。

**返回:**
- None 