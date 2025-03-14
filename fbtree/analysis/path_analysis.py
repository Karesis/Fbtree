"""
路径分析模块: 提供对决策路径的分析功能
"""

from typing import List, Dict, Any, Optional, Tuple
from ..core.move import Move
from ..core.fiber import Fiber

def analyze_path_frequency(fibers: Dict[str, Fiber], depth: Optional[int] = None) -> Dict[int, Dict[str, int]]:
    """
    分析不同深度上移动的频率分布
    
    Args:
        fibers: 包含所有Fiber的字典
        depth: 要分析的最大深度，None表示分析所有深度
        
    Returns:
        Dict[int, Dict[str, int]]: 每个深度的移动频率，格式为 {深度: {移动: 频率}}
    """
    # 结果字典
    depth_frequency = {}
    
    # 遍历所有fiber
    for fiber_id, fiber in fibers.items():
        # 跳过空fiber
        if fiber.is_empty():
            continue
            
        # 遍历fiber中的每个移动
        for i, move in enumerate(fiber.moves):
            # 如果指定了深度且当前深度大于指定深度，则跳过
            if depth is not None and i >= depth:
                break
                
            # 确保深度键存在于结果字典中
            if i not in depth_frequency:
                depth_frequency[i] = {}
                
            # 增加移动频率计数
            move_str = str(move)
            if move_str in depth_frequency[i]:
                depth_frequency[i][move_str] += 1
            else:
                depth_frequency[i][move_str] = 1
    
    return depth_frequency

def find_winning_paths(fibers: Dict[str, Fiber], min_visits: int = 1, min_win_rate: float = 0.5) -> List[Tuple[List[Move], float]]:
    """
    寻找胜率高的路径
    
    Args:
        fibers: 包含所有Fiber的字典
        min_visits: 最小访问次数，用于过滤低置信度的路径
        min_win_rate: 最小胜率阈值
        
    Returns:
        List[Tuple[List[Move], float]]: 符合条件的路径列表，每项包含移动序列和胜率
    """
    winning_paths = []
    
    # 遍历所有fiber
    for fiber_id, fiber in fibers.items():
        # 跳过访问次数低于阈值的fiber
        if fiber.stats['visit_count'] < min_visits:
            continue
            
        # 计算胜率
        win_rate = fiber.get_win_rate()
        
        # 如果胜率高于阈值，则添加到结果列表
        if win_rate >= min_win_rate:
            winning_paths.append((fiber.moves, win_rate))
    
    # 按胜率降序排序
    winning_paths.sort(key=lambda x: x[1], reverse=True)
    
    return winning_paths

def calculate_move_impact(fibers: Dict[str, Fiber]) -> Dict[str, Dict[str, float]]:
    """
    计算每个移动对胜率的影响
    
    Args:
        fibers: 包含所有Fiber的字典
        
    Returns:
        Dict[str, Dict[str, float]]: 每个移动的影响统计，格式为 {移动: {'win_rate': 平均胜率, 'count': 出现次数}}
    """
    move_stats = {}
    
    # 遍历所有fiber
    for fiber_id, fiber in fibers.items():
        # 跳过空fiber
        if fiber.is_empty() or fiber.stats['visit_count'] == 0:
            continue
            
        # 遍历fiber中的每个移动
        for move in fiber.moves:
            move_str = str(move)
            
            # 初始化移动统计
            if move_str not in move_stats:
                move_stats[move_str] = {'win_rate_sum': 0.0, 'count': 0}
                
            # 累加胜率和计数
            move_stats[move_str]['win_rate_sum'] += fiber.get_win_rate()
            move_stats[move_str]['count'] += 1
    
    # 计算每个移动的平均胜率
    result = {}
    for move_str, stats in move_stats.items():
        if stats['count'] > 0:
            result[move_str] = {
                'win_rate': stats['win_rate_sum'] / stats['count'],
                'count': stats['count']
            }
    
    return result 