# FiberTree 使用文档

FiberTree 是一个专注于存储和分析顺序决策路径的数据库系统。它能帮助您跟踪、分析和优化决策过程，通过记录决策路径（fiber）及其结果，为您提供深入的数据分析和决策支持。

## 目录

- [核心概念](#核心概念)
- [安装指南](#安装指南)
- [基础使用](#基础使用)
- [高级功能](#高级功能)
- [存储选项](#存储选项)
- [案例分析](#案例分析)
- [API参考](#api参考)
- [常见问题](#常见问题)

## 核心概念

在开始使用 FiberTree 之前，理解其核心概念非常重要：

### Move（移动）

`Move` 代表决策序列中的单个决定或行动。它可以存储任意类型的值，每个移动还可以关联元数据。

```python
from fbtree import Move

# 创建简单的移动
move1 = Move("A")  # 字符串类型的移动
move2 = Move(5)    # 数字类型的移动

# 创建带元数据的移动
move3 = Move("左转", metadata={"时间": 10.5, "信心": 0.8})
```

### Fiber（纤维）

`Fiber` 表示一系列移动的容器，形成一个决策路径。每个 Fiber 包含移动序列和相关统计数据（如访问次数、胜率等）。

```python
from fbtree import Fiber, Move

# 创建一个包含三个移动的 Fiber
fiber = Fiber(moves=[Move("A"), Move("B"), Move("C")])

# 查看 Fiber 长度
print(len(fiber))  # 输出：3

# 访问特定移动
print(fiber[0])    # 输出：A
```

### FiberTree（纤维树）

`FiberTree` 是管理一系列 Fiber 的数据库。它提供添加、查询、分析和可视化功能。

```python
from fbtree import create_tree

# 创建一个新的树
tree = create_tree()
```

## 安装指南

### 使用 pip 安装

```bash
pip install fbtree
```

### 从源码安装

```bash
git clone https://github.com/yourusername/fbtree.git
cd fbtree
pip install -e .
```

## 基础使用

### 创建树

```python
from fbtree import create_tree

# 创建默认内存存储的树
tree = create_tree()

# 创建 SQLite 存储的树
tree = create_tree(storage_type='sqlite', db_path='my_database.db')
```

### 记录决策路径

```python
from fbtree import Move

# 开始构建路径
tree.start_path()

# 添加单个移动
tree.add_move(Move("A"))
tree.add_move(Move("B"))
tree.add_move(Move("C"))

# 记录结果
tree.record_outcome('win')  # 'win', 'loss', 或 'draw'

# 结束当前路径
tree.end_path()
```

### 批量添加移动

```python
# 批量添加多个移动
moves = [Move("A"), Move("B"), Move("C")]
tree.start_path()
tree.add_moves(moves)
tree.record_outcome('win')
```

### 获取统计信息

```python
# 获取当前路径的统计信息
stats = tree.get_statistics()
print(f"访问次数: {stats['visit_count']}")
print(f"胜率: {stats['win_rate']}")

# 获取完整路径
path = tree.get_complete_path()
print(f"当前路径: {[str(move) for move in path]}")
```

### 保存和加载树

```python
# 保存树到文件
tree.save("my_decision_tree.json")

# 加载树
from fbtree import load_tree
loaded_tree = load_tree("my_decision_tree.json")
```

## 高级功能

### 查找最佳后续决策

```python
# 从特定位置查找最佳后续移动
starting_path = [Move("A"), Move("B")]
best_moves = tree.get_best_continuation(starting_path, top_n=3)

print("最佳后续移动:")
for move_info in best_moves:
    print(f"{move_info['move']} - 胜率: {move_info['win_rate']:.2f}, 访问: {move_info['visits']}")
```

### 移动频率分析

```python
# 获取第一步移动的频率统计
first_move_freq = tree.get_move_frequency(depth=1)
print("第一步移动频率:")
for move, count in first_move_freq.items():
    print(f"{move}: {count}次")

# 获取第二步移动的频率统计
second_move_freq = tree.get_move_frequency(depth=2)
```

### 路径多样性分析

```python
# 获取路径多样性统计
diversity = tree.analyze_path_diversity()
print(f"最大深度: {diversity['max_depth']}")
print(f"平均分支因子: {diversity['avg_branching_factor']:.2f}")
print(f"叶节点数: {diversity['leaf_nodes']}")
print(f"深度分布: {diversity['depth_distribution']}")
```

### 热图生成

```python
# 为3x3棋盘游戏生成移动热图
heatmap = tree.generate_move_heatmap(board_size=3)
print("移动热图:")
for row in heatmap:
    print(" ".join(f"{val:3d}" for val in row))
```

### 树可视化

```python
# 文本可视化（默认）
tree.visualize(max_depth=3)

# 生成 Graphviz DOT 格式
dot_str = tree.visualize(max_depth=3, output_format='graphviz')
with open("tree_viz.dot", "w") as f:
    f.write(dot_str)

# 可以使用 Graphviz 工具将 DOT 文件转换为图像
# 例如：dot -Tpng tree_viz.dot -o tree_viz.png
```

### 树修剪

```python
# 修剪访问次数少于5次的路径
removed_count = tree.prune_tree(min_visits=5)
print(f"已删除 {removed_count} 个低频路径")

# 修剪深度超过10的路径
removed_count = tree.prune_tree(max_depth=10)
print(f"已删除 {removed_count} 个深度过大的路径")
```

### 树合并

```python
# 创建两棵树
tree1 = create_tree()
tree2 = create_tree()

# 分别添加路径...

# 将 tree2 合并到 tree1
merged_count = tree1.merge(tree2, conflict_strategy='stats_sum')
print(f"合并了 {merged_count} 个路径")
```

## 存储选项

FiberTree 提供两种存储后端：

### 内存存储

```python
# 默认使用内存存储
tree = create_tree()
```

内存存储的特点：
- 速度快，适合临时分析
- 程序结束后数据丢失，除非使用 `save` 方法导出
- 适合数据量较小的场景

### SQLite 存储

```python
# 使用 SQLite 存储
tree = create_tree(storage_type='sqlite', db_path='my_database.db')
```

SQLite 存储的特点：
- 数据持久保存到磁盘
- 支持更大的数据集
- 适合长期数据收集和分析

## 案例分析

### 案例一：游戏 AI 决策分析

以下示例展示如何使用 FiberTree 分析简单棋盘游戏中的决策：

```python
from fbtree import create_tree, Move
import random

# 模拟100局游戏
tree = create_tree()

for _ in range(100):
    # 模拟一局游戏...
    moves = [Move(random.randint(0, 8)) for _ in range(5)]
    
    tree.start_path()
    tree.add_moves(moves)
    
    # 随机结果
    outcome = random.choice(['win', 'loss', 'draw'])
    tree.record_outcome(outcome)

# 分析结果
best_first_move = tree.get_best_continuation([], top_n=1)[0]
print(f"最佳首步: {best_first_move['move']}, 胜率: {best_first_move['win_rate']:.2f}")

# 生成热图
heatmap = tree.generate_move_heatmap(board_size=3)
print("移动热图:")
for row in heatmap:
    print(row)
```

### 案例二：用户导航路径分析

```python
from fbtree import create_tree, Move

# 创建持久化存储的树
tree = create_tree(storage_type='sqlite', db_path='user_paths.db')

# 记录用户导航路径
def record_user_session(pages_visited, conversion):
    tree.start_path()
    for page in pages_visited:
        tree.add_move(Move(page))
    
    # 转化率作为"胜率"
    outcome = 'win' if conversion else 'loss'
    tree.record_outcome(outcome)

# 示例用户会话
record_user_session(['首页', '产品列表', '产品详情', '购物车', '结账'], True)
record_user_session(['首页', '搜索', '产品详情', '关闭'], False)

# 分析高转化率路径
starting_path = [Move('首页')]
best_next_pages = tree.get_best_continuation(starting_path, top_n=3)
print("最高转化率的下一页面:")
for page_info in best_next_pages:
    print(f"{page_info['move']} - 转化率: {page_info['win_rate']:.2f}")
```

## API参考

### 核心类

#### Move

```python
Move(value, metadata=None)
```

参数:
- `value`: 任意类型，表示移动的值
- `metadata`: 字典，可选，关联的元数据

主要方法:
- `to_dict()`: 将移动转换为字典
- `from_dict(data)`: 从字典创建移动

#### Fiber

```python
Fiber(moves, fiber_id=None, parent_id=None, metadata=None)
```

参数:
- `moves`: Move列表，此Fiber包含的移动
- `fiber_id`: 字符串，可选，唯一标识符
- `parent_id`: 字符串，可选，父Fiber的ID
- `metadata`: 字典，可选，关联的元数据

主要方法:
- `is_empty()`: 检查是否为空Fiber
- `get_win_rate()`: 计算胜率
- `update_stats(outcome)`: 更新统计信息
- `to_dict()`: 将Fiber转换为字典
- `from_dict(data)`: 从字典创建Fiber

#### FiberTree

```python
FiberTree(storage_type='memory', db_path=None, max_cache_size=1000, logger=None)
```

参数:
- `storage_type`: 'memory' 或 'sqlite'
- `db_path`: SQLite数据库路径（当storage_type='sqlite'时需要）
- `max_cache_size`: 内存缓存的最大项数
- `logger`: 可选的日志记录器

主要方法详见[基础使用](#基础使用)和[高级功能](#高级功能)章节。

### 辅助函数

```python
create_tree(storage_type='memory', db_path=None, max_cache_size=1000)
```

创建一个新的FiberTree实例。

```python
load_tree(file_path, storage_type='memory', db_path=None)
```

从JSON文件加载FiberTree。

## 常见问题

### Q: 如何处理不同类型的决策值？

A: `Move` 类可以接受任意类型的值，但请确保在同一个树中使用一致的类型。如果需要混合类型，建议使用字符串表示，或在元数据中存储额外信息。

### Q: 数据库文件会变得多大？

A: 文件大小取决于存储的路径数量和复杂性。SQLite存储模式对于大型数据集比较高效，但如果担心空间问题，可以定期使用 `prune_tree` 方法清理低价值路径。

### Q: 如何提高大数据集的查询性能？

A: 
1. 增加 `max_cache_size` 参数可以提高读取性能
2. 使用 `prune_tree` 定期清理不必要的数据
3. 对于频繁访问的路径，可以将它们存储在单独的变量中，而不是每次都查询树

### Q: 如何在多个应用间共享决策树？

A: 有两种推荐方法：
1. 使用SQLite存储，并让多个应用访问同一个数据库文件（注意并发控制）
2. 使用 `export_to_json` 和 `import_from_json` 方法在应用间传递数据

### Q: 能否用于实时决策系统？

A: 可以，特别是内存存储模式下性能足够快。对于需要极低延迟的场景，建议：
1. 预先加载常用路径到内存
2. 使用 `get_best_continuation` 快速获取推荐决策
3. 异步更新统计数据

---

## 贡献与支持

欢迎通过Issues或Pull Requests贡献代码和反馈。如有问题，请直接联系作者。

## 许可证

MIT