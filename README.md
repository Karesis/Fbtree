﻿# FiberTree 决策路径存储与分析库

FiberTree 是一个专注于存储和分析顺序决策路径的数据库系统。它能高效地记录、存储和分析决策路径，并提供丰富的统计功能和可视化工具，帮助您优化决策过程。

## 特点

- **灵活的路径存储** - 支持任何序列化决策路径的存储和检索
- **统计分析** - 自动计算节点访问频率、胜率等统计数据
- **路径学习** - 基于现有数据优化决策路径
- **可视化功能** - 提供多种方式可视化决策树（文本、图形）
- **高性能** - 优化的存储引擎，支持内存和SQLite后端
- **易扩展** - 清晰的API设计，便于集成和扩展功能
- **路径分析** - 提供对决策路径的深度分析功能
- **多种可视化方案** - 支持文本、Graphviz和D3.js等多种可视化格式

## 应用场景

- 棋类游戏的走法分析和学习
- 推荐系统决策路径优化
- 用户行为路径分析
- 自动化测试场景覆盖分析
- 决策支持系统
- 强化学习的路径记录与分析

## 安装

### 使用pip安装

```bash
pip install fbtree
```

### 从源码安装

```bash
git clone https://github.com/yourusername/fbtree.git
cd fbtree
pip install -e .
```

## 基本用法

```python
from fbtree import create_tree, Move

# 创建一个树
tree = create_tree()

# 开始构建路径
tree.start_path()

# 添加移动到路径
tree.add_move(Move("A1"))
tree.add_move(Move("B2"))
tree.add_move(Move("C3"))

# 记录结果
tree.record_outcome(win=1, score=10)

# 获取统计信息
stats = tree.get_statistics()
print(stats)
```

## 分析功能

```python
from fbtree import create_tree, Move, analyze_path_frequency, find_winning_paths, calculate_move_impact

# 创建并填充决策树
tree = create_tree()
# ... 添加一些路径和结果 ...

# 分析不同深度的移动频率
freq_data = analyze_path_frequency(tree.get_all_fibers())
print("移动频率分析:", freq_data)

# 查找高胜率路径
winning_paths = find_winning_paths(tree.get_all_fibers(), min_visits=5, min_win_rate=0.6)
print("高胜率路径:", winning_paths)

# 计算各移动对胜率的影响
impact_data = calculate_move_impact(tree.get_all_fibers())
print("移动影响分析:", impact_data)
```

## 可视化功能

```python
from fbtree import create_tree, Move, visualize_tree_text, generate_path_summary
from fbtree import generate_graphviz, generate_d3_json

# 创建并填充决策树
tree = create_tree()
# ... 添加一些路径和结果 ...

# 文本可视化
text_tree = visualize_tree_text(tree.get_all_fibers())
print(text_tree)

# 路径摘要
path_summary = generate_path_summary(tree.get_all_fibers(), min_visits=3)
print(path_summary)

# Graphviz可视化
dot_graph = generate_graphviz(tree.get_all_fibers(), max_depth=3, theme='light')
with open('tree_visualization.dot', 'w') as f:
    f.write(dot_graph)
    
# D3.js数据生成
d3_data = generate_d3_json(tree.get_all_fibers())
with open('tree_data.json', 'w') as f:
    f.write(d3_data)
```

## 核心概念

- **Fiber (纤维)** - 表示一条完整的决策路径，由一系列的Move组成
- **Move (移动)** - 决策路径中的单一步骤或决策
- **Tree (树)** - 所有相关决策路径的集合
- **Storage (存储)** - 负责持久化存储决策路径数据

## 文档

详细的API参考和使用指南请查看[文档](docs/api_reference.md)

## 贡献

欢迎贡献代码、报告问题或提出新的功能建议。请参阅[贡献指南](CONTRIBUTING.md)。

## 许可

本项目基于MIT许可证 - 详情请参阅 [LICENSE](LICENSE) 文件 
