"""
测试FiberTree 1.2.0版本的所有新功能
包括路径分析和可视化功能
"""

import os
import json
from pprint import pprint
import fbtree
from fbtree import create_tree, Move
from fbtree import analyze_path_frequency, find_winning_paths, calculate_move_impact
from fbtree import visualize_tree_text, generate_path_summary

print(f"FiberTree 版本: {fbtree.__version__}")
print("开始全面功能测试...\n")

# 1. 创建树和添加路径
print("=== 1. 创建树和添加路径 ===")
tree = create_tree()

# 添加第一条路径 (获胜路径)
print("添加路径1 (获胜)...")
tree.start_path()
tree.add_move(Move("行动A"))
tree.add_move(Move("结果1"))
tree.record_outcome("win")

# 添加第二条路径 (获胜路径)
print("添加路径2 (获胜)...")
tree.start_path()
tree.add_move(Move("行动B"))
tree.add_move(Move("结果2"))
tree.record_outcome("win")

# 添加第三条路径 (失败路径)
print("添加路径3 (失败)...")
tree.start_path()
tree.add_move(Move("行动C"))
tree.add_move(Move("结果3"))
tree.record_outcome("loss")

# 添加第四条路径 (获胜路径)
print("添加路径4 (获胜)...")
tree.start_path()
tree.add_move(Move("行动A"))  # 再次使用行动A
tree.add_move(Move("结果4"))  # 但到达不同结果
tree.record_outcome("win")

print("路径添加完成\n")

# 2. 保存树
print("=== 2. 保存树 ===")
json_file = "full_test_tree.json"
print(f"保存树到 {json_file}...")
tree.save(json_file)
print("树保存成功\n")

# 3. 获取fibers用于分析
print("=== 3. 准备分析数据 ===")
fibers = tree.get_all_fibers()
print(f"获取到 {len(fibers)} 个fiber节点\n")

# 4. 路径频率分析
print("=== 4. 路径频率分析 ===")
freq_results = analyze_path_frequency(fibers)
print("路径频率分析结果:")
pprint(freq_results)
print()

# 5. 寻找获胜路径
print("=== 5. 寻找获胜路径 ===")
winning_paths = find_winning_paths(fibers, min_visits=1, min_win_rate=0.5)
print("获胜路径:")
for path, win_rate in winning_paths:
    path_str = " -> ".join([str(move) for move in path])
    print(f"  {path_str}: {win_rate:.2f}")
print()

# 6. 计算动作影响
print("=== 6. 计算动作影响 ===")
impact_results = calculate_move_impact(fibers)
print("动作影响结果:")
for move, stats in impact_results.items():
    print(f"  {move}: 胜率={stats['win_rate']:.2f}, 次数={stats['count']}")
print()

# 7. 文本可视化
print("=== 7. 文本可视化 ===")
text_viz = visualize_tree_text(fibers)
print("树的文本可视化:")
print(text_viz)
print()

# 8. 路径摘要生成
print("=== 8. 路径摘要生成 ===")
path_summary = generate_path_summary(fibers)
print("路径摘要:")
print(path_summary)
print()

# 9. 检查 GraphViz 和 D3 功能是否可用
print("=== 9. 检查高级可视化功能 ===")
try:
    from fbtree.visualization import generate_graphviz
    print("GraphViz 功能可用 ✓")
except ImportError:
    print("GraphViz 功能不可用 ✗")

try:
    from fbtree.visualization import generate_d3_json
    print("D3 JSON 功能可用 ✓")
except ImportError:
    print("D3 JSON 功能不可用 ✗")
print()

# 10. 清理
print("=== 10. 清理 ===")
if os.path.exists(json_file):
    os.remove(json_file)
    print(f"已删除测试文件 {json_file}")

print("\n全部测试完成！") 