"""
FiberTree 基本用法示例
"""

from fbtree import create_tree, Move

def main():
    # 创建一个内存存储的树
    tree = create_tree()
    
    # 创建并记录一些路径
    
    # 路径1: 一个胜利序列
    tree.start_path()
    tree.add_move(Move("A"))
    tree.add_move(Move("B"))
    tree.add_move(Move("C"))
    tree.record_outcome('win')
    
    # 路径2: 另一个胜利序列
    tree.start_path()
    tree.add_move(Move("A"))
    tree.add_move(Move("B"))
    tree.add_move(Move("D"))
    tree.record_outcome('win')
    
    # 路径3: 一个失败序列
    tree.start_path()
    tree.add_move(Move("A"))
    tree.add_move(Move("E"))
    tree.record_outcome('loss')
    
    # 获取当前完整路径
    current_path = tree.get_complete_path()
    print(f"当前路径: {[str(move) for move in current_path]}")
    
    # 获取当前路径的统计信息
    stats = tree.get_statistics()
    print(f"当前路径统计: {stats}")
    
    # 从特定位置查找最佳后续移动
    starting_path = [Move("A")]
    best_moves = tree.get_best_continuation(starting_path, top_n=2)
    print(f"从'A'开始的最佳后续移动:")
    for move_info in best_moves:
        print(f"  {move_info['move']} - 胜率: {move_info['win_rate']:.2f}, 访问次数: {move_info['visits']}")
    
    # 获取第一个位置的移动频率
    first_move_freq = tree.get_move_frequency(depth=1)
    print(f"第一个位置的移动频率: {first_move_freq}")
    
    # 可视化树
    print("\n树形可视化:")
    print(tree.visualize(max_depth=3))
    
    # 保存树到文件
    tree.save("my_first_tree.json")
    print("树已保存到my_first_tree.json")
    
if __name__ == "__main__":
    main() 