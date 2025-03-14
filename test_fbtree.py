"""
FiberTree 功能测试脚本
"""

import os
from fbtree import create_tree, Move, FiberTree

def test_basic_functionality():
    """测试基本功能"""
    print("测试1: 基本功能测试")
    print("-" * 50)
    
    # 创建树
    tree = create_tree()
    print("✓ 创建树成功")
    
    # 添加路径
    tree.start_path()
    tree.add_move(Move("左"))
    tree.add_move(Move("右"))
    tree.add_move(Move("前"))
    tree.record_outcome('win')
    print("✓ 添加并记录第一条路径成功")
    
    # 添加第二条路径
    tree.start_path()
    tree.add_move(Move("左"))
    tree.add_move(Move("右"))
    tree.add_move(Move("后"))
    tree.record_outcome('loss')
    print("✓ 添加并记录第二条路径成功")
    
    # 检查当前路径
    path = tree.get_complete_path()
    path_str = [str(move) for move in path]
    print(f"当前完整路径: {path_str}")
    
    # 检查统计信息
    stats = tree.get_statistics()
    print(f"当前路径统计: {stats}")
    
    return tree

def test_analysis(tree):
    """测试分析功能"""
    print("\n测试2: 分析功能测试")
    print("-" * 50)
    
    # 测试最佳后续移动
    starting_path = [Move("左"), Move("右")]
    best_moves = tree.get_best_continuation(starting_path)
    print("从 '左,右' 开始的最佳后续移动:")
    for move_info in best_moves:
        print(f"  {move_info['move']} - 胜率: {move_info['win_rate']:.2f}, 访问次数: {move_info['visits']}")
    
    # 测试移动频率
    freq = tree.get_move_frequency(depth=1)
    print(f"第一层移动频率: {freq}")
    
    freq = tree.get_move_frequency(depth=2)
    print(f"第二层移动频率: {freq}")

def test_persistence(tree):
    """测试持久化功能"""
    print("\n测试3: 持久化功能测试")
    print("-" * 50)
    
    # 保存到文件
    filename = "test_tree.json"
    tree.save(filename)
    print(f"✓ 树已保存到 {filename}")
    
    # 验证文件存在
    if os.path.exists(filename):
        print(f"✓ 文件 {filename} 已创建")
    
    # 加载树
    try:
        loaded_tree = FiberTree.import_from_json(filename)
        print(f"✓ 从文件加载树成功")
        
        # 验证加载的树
        loaded_tree.start_path()
        loaded_tree.add_move(Move("左"))
        loaded_tree.add_move(Move("右"))
        stats = loaded_tree.get_statistics()
        print(f"加载的树统计信息: {stats}")
    except Exception as e:
        print(f"加载树失败: {e}")
    
    # 清理文件
    try:
        os.remove(filename)
        print(f"✓ 测试文件已删除")
    except:
        pass

def test_visualization(tree):
    """测试可视化功能"""
    print("\n测试4: 可视化功能测试")
    print("-" * 50)
    
    # 文本可视化
    text_viz = tree.visualize(max_depth=3, output_format='text')
    print("树的文本可视化:")
    print(text_viz)

def main():
    """运行所有测试"""
    print("FiberTree 功能测试\n")
    
    # 测试基本功能
    tree = test_basic_functionality()
    
    # 测试分析功能
    test_analysis(tree)
    
    # 测试可视化功能
    test_visualization(tree)
    
    # 测试持久化功能
    test_persistence(tree)
    
    print("\n测试完成!")

if __name__ == "__main__":
    main() 