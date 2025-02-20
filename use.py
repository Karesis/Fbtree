#!/usr/bin/env python
"""
FiberTree应用示例 - 五子棋AI决策路径管理
展示如何使用FiberTree管理和分析棋类AI的决策路径
"""

import os
import logging
import time
import random
import argparse
from typing import List, Tuple, Dict, Any, Optional
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

# 导入FiberTree模块
from main import FiberTree, Move, Fiber


def setup_logging(log_file: str = "fbtree_demo.log") -> logging.Logger:
    """设置日志记录"""
    logger = logging.getLogger("FiberTreeDemo")
    logger.setLevel(logging.INFO)

    # 确保日志目录存在
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 文件处理器
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 格式化器
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 添加处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def encode_move(row: int, col: int, board_size: int) -> int:
    """将棋盘坐标编码为整数值"""
    return row * board_size + col


def decode_move(value: int, board_size: int) -> Tuple[int, int]:
    """将整数值解码为棋盘坐标"""
    return value // board_size, value % board_size


def evaluate_position(board: List[List[str]], player: str) -> float:
    """简单评估棋盘位置的得分 (用于模拟AI思考)"""
    # 此函数模拟AI评估棋盘位置
    # 实际应用中应使用更复杂的评估函数
    score = random.random()  # 简单随机分数用于演示
    return score


def simulate_game(tree: FiberTree, board_size: int = 15, max_moves: int = 225) -> Tuple[List[Move], str]:
    """
    模拟一局五子棋游戏，记录决策路径
    
    Args:
        tree: FiberTree实例用于查询最佳走法
        board_size: 棋盘大小
        max_moves: 最大移动数
        
    Returns:
        Tuple[List[Move], str]: 移动序列和游戏结果
    """
    # 初始化棋盘
    board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
    moves = []
    occupancy = set()
    
    # 记录游戏开始
    tree.start_adding_mode()
    
    for move_num in range(max_moves):
        player = 'X' if move_num % 2 == 0 else 'O'
        
        # 检查当前路径是否有推荐的后续走法
        if moves:
            suggestions = tree.get_best_continuation(moves, top_n=3, min_visits=2)
        else:
            suggestions = []
            
        # 如果有推荐走法并且随机决定采纳
        if suggestions and random.random() < 0.7:
            # 90%概率选择最佳走法，10%概率选择其他推荐走法
            if len(suggestions) == 1:
                choice_idx = 0
            # 有多个建议时随机选择
            else:
                choice_idx = 0 if random.random() < 0.9 else random.randint(1, len(suggestions)-1)

            move_value = suggestions[choice_idx]['move'].value
            row, col = decode_move(move_value, board_size)
        else:
            # 没有推荐走法时随机选择
            available_moves = [(r, c) for r in range(board_size) for c in range(board_size) 
                              if (r*board_size + c) not in occupancy]
            if not available_moves:
                # 棋盘已满，平局
                tree.update_statistics('draw')
                tree.end_adding_mode()
                return moves, 'draw'
                
            row, col = random.choice(available_moves)
            move_value = encode_move(row, col, board_size)
            
        # 记录移动
        move = Move(value=move_value)
        moves.append(move)
        tree.add_move(move)
        
        # 更新棋盘
        board[row][col] = player
        occupancy.add(move_value)
        
        # 检查胜负 (简化版)
        if check_win(board, row, col, player, board_size):
            outcome = 'win' if player == 'X' else 'loss'
            tree.update_statistics(outcome)
            tree.end_adding_mode()
            return moves, outcome
            
    # 如果达到最大移动数，视为平局
    tree.update_statistics('draw')
    tree.end_adding_mode()
    return moves, 'draw'


def check_win(board: List[List[str]], row: int, col: int, player: str, board_size: int, n: int = 5) -> bool:
    """检查是否获胜 (五子连珠)"""
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dr, dc in directions:
        count = 1  # 当前位置已经算一个
        
        # 向一个方向查找
        r, c = row + dr, col + dc
        while 0 <= r < board_size and 0 <= c < board_size and board[r][c] == player:
            count += 1
            r += dr
            c += dc
            
        # 向相反方向查找
        r, c = row - dr, col - dc
        while 0 <= r < board_size and 0 <= c < board_size and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
            
        if count >= n:
            return True
            
    return False


def visualize_heatmap(heatmap: List[List[int]], board_size: int, title: str = "移动热图"):
    """可视化移动热图"""
    plt.figure(figsize=(10, 10))
    
    # 创建热图
    plt.imshow(heatmap, cmap='viridis')
    plt.colorbar(label='移动频率')
    
    # 设置标题和标签
    plt.title(title, fontsize=16)
    plt.xlabel('列', fontsize=12)
    plt.ylabel('行', fontsize=12)
    
    # 设置刻度
    plt.xticks(range(board_size), range(1, board_size+1))
    plt.yticks(range(board_size), range(1, board_size+1))
    
    # 添加网格
    plt.grid(color='black', linestyle='-', linewidth=0.5, alpha=0.3)
    
    # 突出显示天元和星位
    center = board_size // 2
    star_points = []
    if board_size >= 15:  # 19路或15路棋盘
        corner_dist = 3 if board_size == 15 else 4
        star_points = [
            (corner_dist, corner_dist), (corner_dist, center), (corner_dist, board_size-corner_dist-1),
            (center, corner_dist), (center, center), (center, board_size-corner_dist-1),
            (board_size-corner_dist-1, corner_dist), (board_size-corner_dist-1, center), 
            (board_size-corner_dist-1, board_size-corner_dist-1)
        ]
    
    for y, x in star_points:
        plt.plot(x, y, 'o', color='red', markersize=8, alpha=0.6)
    
    plt.tight_layout()
    
    # 保存图片
    os.makedirs('output', exist_ok=True)
    plt.savefig(f'output/{title.replace(" ", "_")}.png', dpi=150)
    plt.close()


def visualize_win_rates(tree: FiberTree, board_size: int):
    """可视化不同位置的胜率"""
    # 获取第一步移动的数据
    first_moves = tree.get_move_frequency(depth=1, min_visits=5)
    
    win_rates = np.zeros((board_size, board_size))
    visit_counts = np.zeros((board_size, board_size))
    
    # 分析每个首步移动的胜率
    for move_str, _ in first_moves.items():
        try:
            move_value = int(move_str)
            row, col = decode_move(move_value, board_size)
            
            # 查找这个移动的fiber
            path = [Move(value=move_value)]
            fiber_id = tree.find_path(path)
            
            if fiber_id:
                stats = tree.get_statistics(fiber_id)
                if stats['visit_count'] > 0:
                    win_rates[row][col] = stats['win_rate']
                    visit_counts[row][col] = stats['visit_count']
        except (ValueError, TypeError):
            continue
    
    # 可视化胜率
    plt.figure(figsize=(12, 10))
    
    # 创建胜率热图
    win_rate_masked = np.ma.masked_where(visit_counts < 5, win_rates)
    plt.imshow(win_rate_masked, cmap='RdYlGn', vmin=0, vmax=1, alpha=0.8)
    plt.colorbar(label='胜率')
    
    # 设置标题和标签
    plt.title("首步落子位置胜率分析", fontsize=16)
    plt.xlabel('列', fontsize=12)
    plt.ylabel('行', fontsize=12)
    
    # 设置刻度
    plt.xticks(range(board_size), range(1, board_size+1))
    plt.yticks(range(board_size), range(1, board_size+1))
    
    # 添加网格和星位标记
    plt.grid(color='black', linestyle='-', linewidth=0.5, alpha=0.3)
    center = board_size // 2
    corner_dist = 3 if board_size == 15 else 4
    star_points = [
        (corner_dist, corner_dist), (corner_dist, center), (corner_dist, board_size-corner_dist-1),
        (center, corner_dist), (center, center), (center, board_size-corner_dist-1),
        (board_size-corner_dist-1, corner_dist), (board_size-corner_dist-1, center), 
        (board_size-corner_dist-1, board_size-corner_dist-1)
    ]
    
    for y, x in star_points:
        plt.plot(x, y, 'o', color='black', markersize=8, alpha=0.5)
    
    # 添加访问次数标签
    for i in range(board_size):
        for j in range(board_size):
            if visit_counts[i, j] >= 20:
                plt.text(j, i, f"{int(visit_counts[i, j])}", 
                        ha="center", va="center", color="black", fontsize=8, fontweight="bold")
    
    plt.tight_layout()
    plt.savefig('output/first_move_win_rates.png', dpi=150)
    plt.close()


def analyze_opening_sequences(tree: FiberTree, board_size: int):
    """分析开局序列及其表现"""
    common_paths = tree.get_common_path_statistics(min_visits=10)
    
    # 过滤出长度大于等于4的序列（两回合及以上）
    openings = [path for path in common_paths if path['depth'] >= 4]
    
    if not openings:
        print("没有足够数据的开局序列")
        return
    
    print(f"\n发现 {len(openings)} 种常用开局序列（至少两回合）:")
    
    for i, opening in enumerate(openings[:10]):  # 展示前10个
        path = opening['path']
        
        print(f"\n开局 {i+1} (访问次数: {opening['visits']}, 胜率: {opening['win_rate']:.2f}):")
        print("  移动序列:")
        
        # 转换并展示每步移动
        for j, move in enumerate(path):
            row, col = decode_move(move.value, board_size)
            player = 'X' if j % 2 == 0 else 'O'
            print(f"    {j+1}. {player}: ({row+1}, {col+1})")
            
        # 获取后续常用走法
        continuations = tree.get_best_continuation(path, top_n=3, min_visits=3)
        
        if continuations:
            next_player = 'X' if len(path) % 2 == 0 else 'O'
            print(f"  {next_player}的常见后续走法:")
            
            for j, cont in enumerate(continuations):
                row, col = decode_move(cont['move'].value, board_size)
                print(f"    选项 {j+1}: ({row+1}, {col+1}) - "
                     f"胜率: {cont['win_rate']:.2f}, 访问: {cont['visits']}")


def run_simulation(games: int, board_size: int, tree_path: Optional[str] = None, 
                  prune_threshold: int = 1) -> FiberTree:
    """运行模拟并构建决策树"""
    logger = setup_logging()
    logger.info(f"开始模拟 {games} 局五子棋游戏...")
    
    # 创建或加载FiberTree
    db_path = os.path.join("data", "gomoku_knowledge.db")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    if tree_path and os.path.exists(tree_path):
        logger.info(f"从 {tree_path} 加载现有决策树...")
        tree = FiberTree.import_from_json(tree_path, storage_type='sqlite', db_path=db_path)
        logger.info(f"成功加载决策树，包含 {len(tree)} 个节点")
    else:
        logger.info("创建新的决策树...")
        tree = FiberTree(storage_type='sqlite', db_path=db_path)
    
    # 记录游戏统计
    results = {'win': 0, 'loss': 0, 'draw': 0}
    start_time = time.time()
    
    # 模拟游戏
    for i in tqdm(range(games), desc="模拟游戏进度"):
        moves, outcome = simulate_game(tree, board_size)
        results[outcome] += 1
        
        # 每100局打印进度
        if (i + 1) % 100 == 0:
            elapsed = time.time() - start_time
            games_per_sec = (i + 1) / elapsed
            logger.info(f"已完成 {i + 1} 局游戏, "
                      f"速度: {games_per_sec:.2f} 游戏/秒, "
                      f"树大小: {len(tree)} 节点")
    
    # 打印结果
    total_time = time.time() - start_time
    logger.info(f"\n模拟完成! 总用时: {total_time:.1f} 秒")
    logger.info(f"游戏结果: 黑胜: {results['win']}, 白胜: {results['loss']}, 平局: {results['draw']}")
    logger.info(f"树大小: {len(tree)} 节点")
    
    # 修剪低访问度的节点
    if prune_threshold > 0:
        initial_size = len(tree)
        logger.info(f"修剪访问次数少于 {prune_threshold} 的节点...")
        removed = tree.prune_tree(min_visits=prune_threshold)
        logger.info(f"修剪完成: 移除了 {removed} 个节点, 当前树大小: {len(tree)}")
        
        if initial_size - removed != len(tree):
            logger.warning(f"修剪后节点计数不一致: {initial_size} - {removed} != {len(tree)}")
    
    # 导出决策树
    if not tree_path:
        tree_path = os.path.join("data", f"gomoku_tree_{games}games.json")
    
    tree.export_to_json(tree_path)
    logger.info(f"决策树已导出到 {tree_path}")
    
    return tree


def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="五子棋AI决策树模拟器")
    parser.add_argument("--games", type=int, default=1000, help="要模拟的游戏数量")
    parser.add_argument("--board-size", type=int, default=15, help="棋盘大小")
    parser.add_argument("--load", type=str, default="", help="要加载的决策树JSON文件路径")
    parser.add_argument("--prune", type=int, default=2, help="修剪阈值，0表示不修剪")
    parser.add_argument("--analysis-only", action="store_true", help="仅分析现有树，不模拟新游戏")
    
    args = parser.parse_args()
    
    # 如果仅分析模式
    if args.analysis_only:
        if not args.load or not os.path.exists(args.load):
            print(f"错误: 在分析模式下必须提供有效的决策树文件 (--load)")
            return
            
        print(f"加载决策树 {args.load} 进行分析...")
        db_path = os.path.join("data", "analysis_tree.db")
        tree = FiberTree.import_from_json(args.load, storage_type='sqlite', db_path=db_path)
        print(f"成功加载决策树，包含 {len(tree)} 个节点")
    else:
        # 运行模拟
        tree = run_simulation(args.games, args.board_size, args.load, args.prune)
    
    # 分析树结构
    print("\n分析决策树...")
    stats = tree.analyze_path_diversity()
    print(f"总节点数: {stats['total_fibers']}")
    print(f"最大深度: {stats['max_depth']}")
    print(f"平均分支因子: {stats['avg_branching_factor']:.2f}")
    print(f"叶节点数: {stats['leaf_nodes']}")
    
    # 生成热图
    print("\n生成移动热图...")
    os.makedirs('output', exist_ok=True)
    
    heatmap = tree.generate_move_heatmap(args.board_size)
    visualize_heatmap(heatmap, args.board_size, "全局移动频率热图")
    
    # 分析开局走法
    print("\n生成胜率分析...")
    visualize_win_rates(tree, args.board_size)
    
    # 分析开局序列
    analyze_opening_sequences(tree, args.board_size)
    
    print("\n分析完成! 结果已保存到 output/ 目录")


if __name__ == "__main__":
    main()