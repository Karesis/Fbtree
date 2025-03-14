"""
FiberTree 高级分析和可视化示例

此示例展示如何使用FiberTree的分析和可视化模块进行决策路径分析和可视化。
"""

from fbtree import create_tree, Move
from fbtree import analyze_path_frequency, find_winning_paths, calculate_move_impact
from fbtree import visualize_tree_text, generate_path_summary, generate_graphviz, generate_d3_json
import json
import os

def create_sample_tree():
    """创建一个包含示例数据的决策树"""
    tree = create_tree()
    
    # 添加多个决策路径
    paths_and_outcomes = [
        # 路径, 结果, 访问次数
        ([("A1", 0.8), ("B2", 0.6), ("C3", 0.9)], 'win', 10),
        ([("A1", 0.8), ("B2", 0.6), ("D4", 0.4)], 'loss', 5),
        ([("A1", 0.8), ("B3", 0.3), ("E5", 0.7)], 'win', 8),
        ([("A1", 0.8), ("B3", 0.3), ("F6", 0.2)], 'loss', 3),
        ([("G7", 0.5), ("H8", 0.8), ("I9", 0.9)], 'win', 12),
        ([("G7", 0.5), ("H8", 0.8), ("J0", 0.1)], 'loss', 4),
        ([("G7", 0.5), ("K1", 0.4), ("L2", 0.6)], 'win', 7),
        ([("M3", 0.2), ("N4", 0.3), ("O5", 0.4)], 'loss', 6),
    ]
    
    for path, outcome, visits in paths_and_outcomes:
        # 为每条路径重复添加记录（模拟多次访问）
        for _ in range(visits):
            tree.start_path()
            for move_val, score in path:
                tree.add_move(Move(move_val))
            tree.record_outcome(outcome, score=score)
    
    return tree

def analyze_tree(tree):
    """对树进行分析"""
    print("\n=== 树分析 ===\n")
    
    # 获取所有fiber数据
    fibers = tree.get_all_fibers()
    
    # 1. 分析不同深度的移动频率
    print("1. 移动频率分析:")
    freq_data = analyze_path_frequency(fibers)
    for depth, moves in freq_data.items():
        print(f"深度 {depth}:")
        # 按频率排序
        sorted_moves = sorted(moves.items(), key=lambda x: x[1], reverse=True)
        for move, freq in sorted_moves:
            print(f"  {move}: {freq}次")
    
    # 2. 寻找高胜率路径
    print("\n2. 高胜率路径:")
    winning_paths = find_winning_paths(fibers, min_visits=5, min_win_rate=0.6)
    for i, (moves, win_rate) in enumerate(winning_paths, 1):
        path_str = " → ".join([str(move) for move in moves])
        print(f"路径 {i}: {path_str} (胜率: {win_rate:.2f})")
    
    # 3. 分析每个移动对胜率的影响
    print("\n3. 移动影响分析:")
    impact_data = calculate_move_impact(fibers)
    # 按平均胜率排序
    sorted_impact = sorted(impact_data.items(), 
                         key=lambda x: x[1]['win_rate'], 
                         reverse=True)
    for move, stats in sorted_impact:
        print(f"移动 {move}: 平均胜率 {stats['win_rate']:.2f}, 出现 {stats['count']} 次")

def visualize_tree(tree):
    """展示树的不同可视化方式"""
    print("\n=== 树可视化 ===\n")
    
    # 获取所有fiber数据
    fibers = tree.get_all_fibers()
    
    # 确保输出目录存在
    os.makedirs("output", exist_ok=True)
    
    # 1. 文本可视化
    print("1. 文本可视化输出:")
    text_tree = visualize_tree_text(fibers, max_depth=2)
    print(text_tree)
    
    # 2. 路径摘要
    print("\n2. 路径摘要:")
    path_summary = generate_path_summary(fibers, min_visits=3, sort_by='win_rate')
    print(path_summary)
    
    # 3. 生成Graphviz DOT文件
    print("\n3. 生成Graphviz图形:")
    dot_graph = generate_graphviz(fibers, max_depth=3, theme='light')
    dot_file_path = "output/tree_visualization.dot"
    with open(dot_file_path, 'w') as f:
        f.write(dot_graph)
    print(f"Graphviz DOT文件已保存到: {dot_file_path}")
    print("可以使用以下命令生成图像:")
    print(f"  dot -Tpng {dot_file_path} -o output/tree_visualization.png")
    
    # 4. 生成D3.js JSON数据
    print("\n4. 生成D3.js数据:")
    d3_data = generate_d3_json(fibers)
    json_file_path = "output/tree_data.json"
    with open(json_file_path, 'w') as f:
        f.write(d3_data)
    print(f"D3.js JSON数据已保存到: {json_file_path}")

def main():
    # 创建示例树
    tree = create_sample_tree()
    print(f"创建了一个包含 {len(tree.get_all_fibers())} 个路径节点的决策树")
    
    # 分析树
    analyze_tree(tree)
    
    # 可视化树
    visualize_tree(tree)
    
    print("\n示例完成。可视化文件已保存到output目录。")

if __name__ == "__main__":
    main() 