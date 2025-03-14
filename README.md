# FiberTree (纤维树)

FiberTree 是一个灵活、可扩展的决策路径管理和分析库，专为序列决策问题设计。它不仅仅是一个蒙特卡罗树搜索(MCTS)实现，更是一个完整的决策分析框架，能够帮助您存储、管理、分析和可视化决策路径。

## 主要特点

- **灵活的路径存储**：支持内存和SQLite存储后端，满足不同的应用场景
- **统计分析**：跟踪访问次数、胜率和其他关键指标
- **路径学习**：根据历史数据识别最佳决策路径
- **可视化**：支持文本和图形化可视化决策树
- **轻量级**：核心设计简洁高效，易于集成
- **可扩展**：模块化设计，易于定制和扩展

## 应用场景

FiberTree 适用于各种需要序列决策分析的场景：

- **游戏AI**：棋类游戏、策略游戏的决策分析
- **用户行为分析**：跟踪用户决策路径，发现行为模式
- **业务流程优化**：分析不同决策路径的效果
- **风险评估**：评估不同决策序列的风险和回报
- **推荐系统**：基于历史路径推荐最佳下一步

## 安装

```bash
pip install fbtree
```

或者从源码安装:

```bash
git clone https://github.com/yourusername/fbtree.git
cd fbtree
pip install -e .
```

## 快速开始

### 基本用法

```python
from fbtree import create_tree, Move

# 创建一个新的决策树
tree = create_tree()

# 开始一个新路径
tree.start_path()

# 添加一系列决策
tree.add_move(Move("左转"))
tree.add_move(Move("直行"))
tree.add_move(Move("右转"))

# 记录这个路径的结果
tree.record_outcome('success')

# 获取当前路径的统计信息
stats = tree.get_statistics()
print(stats)
```

### 分析最佳后续动作

```python
# 从特定路径开始，分析最佳后续动作
starting_path = [Move("左转"), Move("直行")]
best_moves = tree.get_best_continuation(starting_path)

for move in best_moves:
    print(f"动作: {move['move']}, 胜率: {move['win_rate']}, 访问次数: {move['visits']}")
```

### 可视化决策树

```python
# 以文本形式可视化树
visualization = tree.visualize(max_depth=3, output_format='text')
print(visualization)

# 保存图形化可视化 (需要安装graphviz)
tree.visualize(max_depth=3, output_format='graphviz', output_file='my_tree.png')
```

## 核心概念

- **Move**：表示在决策序列中的一个单一决策或动作
- **Fiber**：代表决策树中的一个节点，包含统计信息和状态
- **FiberTree**：管理整个决策树的核心类，提供路径添加、查询和分析功能

## 文档

更详细的文档请参考 [docs/](docs/) 目录或访问我们的在线文档。

## 示例

查看 [examples/](examples/) 目录获取更多使用示例。

## 贡献指南

我们欢迎所有形式的贡献。请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何参与项目。

## 许可证

本项目采用 [MIT 许可证](LICENSE)。 
