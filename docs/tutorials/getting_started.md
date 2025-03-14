# FiberTree 入门教程

本教程将帮助您快速上手FiberTree库，学习其基本用法和核心概念。

## 安装

首先，通过pip安装FiberTree：

```bash
pip install fbtree
```

## 基本概念

在开始使用FiberTree之前，让我们了解一些核心概念：

### Move（动作）

`Move` 类代表决策树中的一个单一动作或决策。它可以包含任何类型的值来表示具体的动作内容。

```python
from fbtree import Move

# 创建一个字符串类型的动作
move1 = Move("向左转")

# 创建一个数值类型的动作（如棋盘坐标）
move2 = Move(15)  # 例如代表五子棋的某个位置

# 也可以使用更复杂的对象
move3 = Move({"x": 10, "y": 20, "action": "jump"})
```

### Fiber（纤维）

`Fiber` 是决策树中的节点，代表通过特定动作序列到达的状态。每个Fiber包含统计信息如访问次数、胜率等。

### FiberTree（纤维树）

`FiberTree` 是整个库的核心类，管理Fiber节点集合，并提供添加、查询和分析路径的功能。

## 基本用法

### 创建树

```python
from fbtree import create_tree

# 创建一个使用内存存储的树
tree = create_tree(storage_type='memory')

# 或创建一个使用SQLite存储的树（适用于大型决策树）
tree = create_tree(storage_type='sqlite', db_path='my_tree.db')
```

### 记录路径

有两种方式可以记录路径：逐步构建和一次性添加。

#### 逐步构建路径：

```python
# 开始记录新路径
tree.start_path()

# 添加一系列决策
tree.add_move(Move("A"))
tree.add_move(Move("B"))
tree.add_move(Move("C"))

# 记录结果（可以是'win'、'loss'或'draw'，也可以自定义）
tree.record_outcome('win')
```

#### 一次性添加路径：

```python
# 创建完整路径
path = [Move("A"), Move("B"), Move("C")]

# 模拟这条路径，并记录结果
tree.simulate_path(path=path, outcome='win')

# 也可以指定访问次数
tree.simulate_path(path=path, outcome='win', visits=5)
```

### 查询统计信息

```python
# 获取当前路径的统计信息
stats = tree.get_statistics()
print(f"访问次数: {stats['visit_count']}")
print(f"胜率: {stats['win_rate']}")

# 获取特定路径的统计信息
path = [Move("A"), Move("B")]
fiber_id = tree.find_path(path)
if fiber_id:
    stats = tree.get_statistics(fiber_id)
    print(stats)
```

### 分析最佳后续动作

```python
# 从特定路径开始，获取最佳后续动作
starting_path = [Move("A")]
best_moves = tree.get_best_continuation(starting_path, top_n=3)

for i, move_info in enumerate(best_moves, 1):
    print(f"{i}. {move_info['move']} - 胜率: {move_info['win_rate']:.2f}, 访问: {move_info['visits']}")
```

### 可视化决策树

```python
# 文本可视化
text_viz = tree.visualize(max_depth=3, output_format='text')
print(text_viz)

# 导出为图像（需要安装Graphviz）
tree.visualize(
    max_depth=4,
    output_format='graphviz',
    output_file='decision_tree.png'
)
```

## 持久化

FiberTree支持将决策树保存到文件和从文件加载：

```python
# 保存树
tree.save('my_decision_tree.json')

# 加载树
from fbtree import FiberTree
loaded_tree = FiberTree.import_from_json('my_decision_tree.json')
```

## 高级功能

### 获取移动频率

```python
# 获取第一层动作的频率统计
freq = tree.get_move_frequency(depth=1)
print(freq)

# 只显示访问次数达到阈值的动作
freq = tree.get_move_frequency(depth=2, min_visits=5)
print(freq)
```

### 生成热图数据

```python
# 对于棋盘类游戏，生成动作热图数据
heatmap = tree.generate_move_heatmap(board_size=15)  # 15x15的棋盘

# 可以使用matplotlib等工具可视化此热图
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 10))
plt.imshow(heatmap, cmap='viridis')
plt.colorbar(label='移动频率')
plt.title('棋盘热图')
plt.show()
```

### 修剪树

对于长期使用的决策树，可能需要定期修剪访问次数少的节点，以提高性能：

```python
# 移除访问次数少于5的节点
removed_count = tree.prune_tree(min_visits=5)
print(f"已移除 {removed_count} 个低频节点")
```

## 下一步

在掌握了这些基本概念和用法后，您可以：

1. 查看[示例目录](../../examples/)中的更多示例
2. 阅读[高级教程](./advanced_topics.md)了解更复杂的用法
3. 参考[API文档](../api_reference.md)获取详细的接口说明

## 常见问题

### 如何在多个会话间保存和恢复决策树？

使用SQLite存储后端创建树，它会自动将数据保存到指定的数据库文件：

```python
tree = create_tree(storage_type='sqlite', db_path='persistent_tree.db')
```

然后在未来的会话中，使用相同的数据库路径创建树：

```python
tree = create_tree(storage_type='sqlite', db_path='persistent_tree.db')
# 树将自动加载之前的数据
```

### 如何合并来自不同来源的决策树？

FiberTree提供了合并功能：

```python
# 合并另一棵树
tree.merge(another_tree, conflict_strategy='stats_sum')
```

### 决策树变得太大，性能下降怎么办？

1. 使用SQLite存储后端代替内存存储
2. 定期修剪访问次数低的节点：`tree.prune_tree(min_visits=threshold)`
3. 考虑分割树或实现更细粒度的缓存策略 