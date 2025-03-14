"""
FiberTree 1.2.0 正确用法示例
展示包括基本功能、分析和可视化的完整使用方法
"""

import os
import json
from pprint import pprint
import fbtree
from fbtree import create_tree, Move
from fbtree import analyze_path_frequency, find_winning_paths, calculate_move_impact
from fbtree import visualize_tree_text, generate_path_summary, generate_graphviz, generate_d3_json

print(f"FiberTree 版本: {fbtree.__version__}")

# 1. 创建树和添加路径
print("\n=== 1. 创建树和添加路径 ===")
tree = create_tree()  # 使用内存存储后端
print("* 树已创建")

# 添加第一条路径 (获胜)
print("* 添加路径1 (获胜)")
tree.start_path()
tree.add_move(Move("行动A"))
tree.add_move(Move("结果1"))
tree.record_outcome("win")  # 正确的记录结果方法

# 添加第二条路径 (获胜)
print("* 添加路径2 (获胜)")
tree.start_path()
tree.add_move(Move("行动B"))
tree.add_move(Move("结果2"))
tree.record_outcome("win")

# 添加第三条路径 (失败)
print("* 添加路径3 (失败)")
tree.start_path()
tree.add_move(Move("行动C"))
tree.add_move(Move("结果3"))
tree.record_outcome("loss")

# 添加第四条路径 (获胜) - 复用之前的行动
print("* 添加路径4 (获胜 - 复用行动A)")
tree.start_path()
tree.add_move(Move("行动A"))
tree.add_move(Move("结果4"))
tree.record_outcome("win")

# 2. 获取基本统计信息
print("\n=== 2. 基本统计信息 ===")
stats = tree.get_statistics()
print("* 树统计信息:")
pprint(stats)

# 3. 保存和加载
print("\n=== 3. 保存和加载树 ===")
json_file = "example_tree.json"
tree.save(json_file)
print(f"* 已保存树到 {json_file}")

# 可以使用以下方法加载树
# loaded_tree = fbtree.load_tree(json_file)
# print("* 成功加载树")

# 4. 使用分析功能
print("\n=== 4. 使用分析功能 ===")
# 获取所有fibers用于分析
fibers = tree.get_all_fibers()

# 分析路径频率
print("\n* 路径频率分析:")
freq_results = analyze_path_frequency(fibers)
pprint(freq_results)

# 查找获胜路径
print("\n* 获胜路径分析:")
winning_paths = find_winning_paths(fibers, min_visits=1, min_win_rate=0.5)
for path, win_rate in winning_paths:
    path_str = " -> ".join([str(move) for move in path])
    print(f"  路径: {path_str}, 胜率: {win_rate:.2f}")

# 计算移动影响
print("\n* 移动影响分析:")
impact_results = calculate_move_impact(fibers)
for move, stats in impact_results.items():
    print(f"  移动 {move}: 胜率={stats['win_rate']:.2f}, 次数={stats['count']}")

# 5. 使用可视化功能
print("\n=== 5. 使用可视化功能 ===")

# 文本可视化
print("\n* 树的文本可视化:")
text_viz = visualize_tree_text(fibers, max_depth=3)
print(text_viz)

# 路径摘要
print("\n* 路径摘要:")
path_summary = generate_path_summary(fibers, min_visits=1)
print(path_summary)

# Graphviz可视化 (可选)
dot_file = "example_tree.dot"
dot_string = generate_graphviz(fibers, max_depth=3)
with open(dot_file, "w") as f:
    f.write(dot_string)
print(f"\n* 已生成Graphviz DOT文件: {dot_file}")

# D3.js JSON数据 (可选)
d3_file = "example_tree_d3.json"
d3_json = generate_d3_json(fibers)
with open(d3_file, "w") as f:
    f.write(d3_json)
print(f"* 已生成D3.js JSON文件: {d3_file}")

# 6. 清理
print("\n=== 6. 清理 ===")
# 仅在示例运行结束时删除生成的文件
for file in [json_file, dot_file, d3_file]:
    if os.path.exists(file):
        os.remove(file)
        print(f"* 已删除临时文件: {file}")

print("\n示例运行完成!") 