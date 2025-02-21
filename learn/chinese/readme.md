# FiberTree 教学文档

## 目录
- [1. 简介与安装](#1-简介与安装)
- [2. 核心概念](#2-核心概念)
- [3. 基础教程](#3-基础教程) 
- [4. 进阶教程](#4-进阶教程)
- [5. 高级功能](#5-高级功能)
- [6. 最佳实践](#6-最佳实践)
- [7. 案例分析](#7-案例分析) 
- [8. API 参考](#8-api-参考)

## 1. 简介与安装

### 1.1 什么是 FiberTree？

FiberTree 是一个专注于存储和分析顺序决策路径的数据库系统。在很多应用场景中，决策是按一定顺序依次做出的，形成一条决策路径。FiberTree 可以高效地存储这些路径，并提供强大的工具来分析它们的效果、发现模式并提供决策支持。

**主要特点**：
- 高效存储顺序决策路径
- 统计分析路径的成功率
- 查找最佳决策序列
- 可视化决策树结构
- 支持内存和 SQLite 存储模式

### 1.2 应用场景

FiberTree 特别适合以下场景：
- **游戏 AI 开发**：记录游戏中的决策序列及其结果
- **用户行为分析**：追踪网站/应用中的用户导航路径
- **自动化决策系统**：优化决策链和流程
- **路径规划**：分析不同路径的效率和成功率
- **知识表示**：构建和查询决策知识库

### 1.3 安装

**通过 pip 安装**：
```bash
pip install fbtree
```

**从源码安装**：
```bash
git clone https://github.com/Karesis/Fbtree.git
cd fbtree
pip install -e .
```

## 2. 核心概念

在开始使用 FiberTree 之前，先了解三个核心概念：

### 2.1 Move（移动）

`Move` 表示序列中的单个决策或行动。可以存储任意类型的值，还可以关联额外的元数据。

```python
from fbtree import Move

# 简单移动
move1 = Move("前进")

# 带元数据的移动
move2 = Move("左转", metadata={"角度": 90, "原因": "避障"})
```

### 2.2 Fiber（纤维）

`Fiber` 是一系列移动的容器，形成一个完整的决策路径。它包含移动序列和相关统计数据（如访问次数、成功率）。

```python
from fbtree import Fiber, Move

# 创建一个包含三个移动的路径
fiber = Fiber(moves=[Move("A"), Move("B"), Move("C")])
```

### 2.3 FiberTree（纤维树）

`FiberTree` 是管理多个 Fiber 的数据库，提供添加、查询、分析和可视化功能。它构建了一个树形结构，其中路径可以共享前缀，从而高效存储相似的决策序列。

```python
from fbtree import create_tree

# 创建一个新的树
tree = create_tree()
```

## 3. 基础教程

### 3.1 创建你的第一个树

让我们从创建一个简单的 FiberTree 开始：

```python
from fbtree import create_tree, Move

# 创建一个内存存储的树
tree = create_tree()

# 创建一个 SQLite 存储的树（持久化）
# tree = create_tree(storage_type='sqlite', db_path='my_database.db')
```

### 3.2 记录决策路径

记录一条简单的决策路径：

```python
# 开始构建路径
tree.start_path()

# 添加移动
tree.add_move(Move("A"))
tree.add_move(Move("B"))
tree.add_move(Move("C"))

# 记录结果：win（成功）、loss（失败）或 draw（平局）
tree.record_outcome('win')

# 结束当前路径
tree.end_path()
```

你也可以通过 `add_moves` 批量添加移动：

```python
moves = [Move("A"), Move("B"), Move("C")]
tree.start_path()
tree.add_moves(moves)
tree.record_outcome('win')
tree.end_path()
```

### 3.3 检索统计信息

获取当前路径的统计信息：

```python
# 获取当前路径的统计信息
stats = tree.get_statistics()
print(f"访问次数: {stats['visit_count']}")
print(f"胜率: {stats['win_rate']}")

# 获取完整路径
path = tree.get_complete_path()
print(f"当前路径: {[str(move) for move in path]}")
```

### 3.4 保存和加载树

你可以将树保存到文件，并在以后加载：

```python
# 保存树
tree.save("my_decision_tree.json")

# 加载树
from fbtree import load_tree
loaded_tree = load_tree("my_decision_tree.json")
```

## 4. 进阶教程

### 4.1 查找最佳后续决策

一个强大的功能是从当前位置找出最佳的下一步决策：

```python
# 从特定位置查找最佳后续移动
starting_path = [Move("A"), Move("B")]
best_moves = tree.get_best_continuation(starting_path, top_n=3, min_visits=2)

print("最佳后续移动:")
for move_info in best_moves:
    print(f"{move_info['move']} - 胜率: {move_info['win_rate']:.2f}, 访问: {move_info['visits']}")
```

### 4.2 移动频率分析

分析特定深度的移动频率：

```python
# 获取第一步移动的频率统计
first_move_freq = tree.get_move_frequency(depth=1)
print("第一步移动频率:")
for move, count in first_move_freq.items():
    print(f"{move}: {count}次")

# 获取第二步移动的频率统计
second_move_freq = tree.get_move_frequency(depth=2)
```

### 4.3 生成热图

对于棋盘游戏或空间决策，可以生成热图：

```python
# 为3x3棋盘游戏生成移动热图
heatmap = tree.generate_move_heatmap(board_size=3)
print("移动热图:")
for row in heatmap:
    print(" ".join(f"{val:3d}" for val in row))
```

### 4.4 树可视化

可视化树结构有助于理解决策模式：

```python
# 文本格式可视化（适合终端查看）
tree.visualize(max_depth=3)

# 生成 Graphviz DOT 格式（可转换为图像）
dot_str = tree.visualize(max_depth=3, output_format='graphviz')
with open("tree_viz.dot", "w") as f:
    f.write(dot_str)
```

## 5. 高级功能

### 5.1 树修剪

随着时间推移，树可能变得非常大。你可以修剪不常用的分支：

```python
# 修剪访问次数少于5次的路径
removed_count = tree.prune_tree(min_visits=5)
print(f"已删除 {removed_count} 个低频路径")

# 修剪深度超过10的路径
removed_count = tree.prune_tree(max_depth=10)
```

### 5.2 树合并

你可以合并两棵树的知识：

```python
# 创建两棵树
tree1 = create_tree()
tree2 = create_tree()

# 分别添加路径...

# 将 tree2 合并到 tree1
merged_count = tree1.merge(tree2, conflict_strategy='stats_sum')
print(f"合并了 {merged_count} 个路径")
```

合并策略选项：
- `stats_sum`：合并统计数据（访问、胜利次数等）
- `keep_max`：保留访问次数最多的那个
- `keep_current`：保留当前树的数据

### 5.3 路径多样性分析

分析路径的分布和多样性：

```python
# 获取路径多样性统计
diversity = tree.analyze_path_diversity()
print(f"最大深度: {diversity['max_depth']}")
print(f"平均分支因子: {diversity['avg_branching_factor']:.2f}")
print(f"叶节点数: {diversity['leaf_nodes']}")
print(f"深度分布: {diversity['depth_distribution']}")
```

### 5.4 路径模拟

模拟路径可以用于初始化或增强树的知识：

```python
# 模拟一个成功的路径，重复10次
path = [Move("X"), Move("Y"), Move("Z")]
tree.simulate_path(path, outcome='win', visits=10)
```

## 6. 最佳实践

### 6.1 存储选择

- **内存存储（默认）**：更快，但程序结束后数据会丢失
  ```python
  tree = create_tree()  # 默认使用内存存储
  ```

- **SQLite 存储**：持久化，适合长期项目和大数据集
  ```python
  tree = create_tree(storage_type='sqlite', db_path='my_database.db')
  ```

### 6.2 性能优化

- 增加缓存大小可提高频繁访问的性能
  ```python
  tree = create_tree(max_cache_size=5000)
  ```

- 定期修剪树以减少存储大小并提高查询速度
  ```python
  # 每 10,000 次添加后进行修剪
  if add_count % 10000 == 0:
      tree.prune_tree(min_visits=2)
  ```

### 6.3 移动值类型

虽然 `Move` 可以存储任意类型的值，但是同一个树中保持一致的类型很重要：

```python
# 好的做法 - 一致使用字符串
tree.add_move(Move("左转"))
tree.add_move(Move("前进"))

# 好的做法 - 一致使用数字（如棋盘坐标）
tree.add_move(Move(1))
tree.add_move(Move(5))

# 避免混合类型
# 不推荐: tree.add_move(Move("左转"))，然后 tree.add_move(Move(5))
```

### 6.4 元数据使用

元数据可以存储不直接影响路径匹配的额外信息：

```python
# 添加带有上下文的移动
tree.add_move(Move(
    "左转",
    metadata={
        "时间戳": 1623451789,
        "环境": "雨天",
        "速度": 30
    }
))
```

## 7. 案例分析

### 7.1 游戏 AI 开发

```python
from fbtree import create_tree, Move
import random

# 创建井字棋游戏 AI
tic_tac_toe_tree = create_tree()

# 模拟 1000 场游戏
for _ in range(1000):
    tic_tac_toe_tree.start_path()
    board = [None] * 9
    player = 'X'
    
    # 模拟一场游戏
    while True:
        # 找出可用位置
        available = [i for i, val in enumerate(board) if val is None]
        if not available:
            tic_tac_toe_tree.record_outcome('draw')
            break
            
        # 随机选择一个位置
        position = random.choice(available)
        tic_tac_toe_tree.add_move(Move(position))
        board[position] = player
        
        # 检查是否胜利（简化版）
        # ...实际游戏中需要检查胜利条件
        
        # 切换玩家
        player = 'O' if player == 'X' else 'X'
    
    tic_tac_toe_tree.end_path()

# 找出最佳首步
best_first_move = tic_tac_toe_tree.get_best_continuation([], top_n=1)[0]
print(f"最佳首步: {best_first_move['move'].value}, 胜率: {best_first_move['win_rate']:.2f}")

# 生成移动热图
heatmap = tic_tac_toe_tree.generate_move_heatmap(board_size=3)
```

### 7.2 用户导航分析

```python
from fbtree import create_tree, Move

# 创建用户导航分析树
navigation_tree = create_tree(storage_type='sqlite', db_path='user_paths.db')

def track_user_session(pages_visited, conversion_successful):
    """记录用户会话"""
    navigation_tree.start_path()
    for page in pages_visited:
        navigation_tree.add_move(Move(page))
    
    outcome = 'win' if conversion_successful else 'loss'
    navigation_tree.record_outcome(outcome)
    navigation_tree.end_path()

# 记录用户会话
track_user_session(['首页', '产品列表', '产品详情', '购物车', '结账'], True)
track_user_session(['首页', '搜索', '产品详情', '关闭'], False)

# 分析从首页开始的最佳路径
best_paths = navigation_tree.get_best_continuation([Move('首页')], top_n=3)
print("最高转化率的路径:")
for path_info in best_paths:
    print(f"{path_info['move']} - 转化率: {path_info['win_rate']:.2f}")
```

## 8. API 参考

### 8.1 核心函数

```python
# 创建新树
create_tree(storage_type='memory', db_path=None, max_cache_size=1000)

# 加载现有树
load_tree(file_path, storage_type='memory', db_path=None)
```

### 8.2 路径构建

```python
# 开始路径
tree.start_path()

# 添加移动
tree.add_move(Move(value, metadata=None))

# 批量添加移动
tree.add_moves(moves_list)

# 记录结果
tree.record_outcome(outcome)  # 'win', 'loss', 或 'draw'

# 结束路径
tree.end_path()
```

### 8.3 查询与分析

```python
# 获取统计信息
tree.get_statistics(fiber_id=None)

# 获取完整路径
tree.get_complete_path()

# 查找最佳后续移动
tree.get_best_continuation(current_path, top_n=3, min_visits=5)

# 获取移动频率
tree.get_move_frequency(depth=1, min_visits=0)

# 生成热图
tree.generate_move_heatmap(board_size)

# 分析路径多样性
tree.analyze_path_diversity()
```

### 8.4 管理功能

```python
# 保存树
tree.save(file_path)

# 修剪树
tree.prune_tree(min_visits=1, max_depth=None)

# 合并树
tree.merge(other_tree, conflict_strategy='stats_sum')

# 模拟路径
tree.simulate_path(path, outcome, visits=1)

# 可视化树
tree.visualize(max_depth=5, output_format='text')
```

---

这个教学文档旨在帮助您循序渐进地掌握 FiberTree 的使用。从基础概念到高级应用，您可以根据自己的需求选择适合的章节深入学习。如有任何问题或建议，请随时与我们联系。

祝您使用愉快！