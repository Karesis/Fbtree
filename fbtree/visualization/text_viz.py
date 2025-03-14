"""
文本可视化模块: 提供树结构的文本形式可视化
"""

from typing import Dict, Optional, List, Set
from ..core.fiber import Fiber
from ..core.move import Move

def visualize_tree_text(fibers: Dict[str, Fiber], 
                        root_id: str = 'root', 
                        max_depth: Optional[int] = None,
                        include_stats: bool = True) -> str:
    """
    生成树的文本可视化表示
    
    Args:
        fibers: 包含所有Fiber的字典
        root_id: 根节点的ID
        max_depth: 最大可视化深度，None表示不限制
        include_stats: 是否包含统计信息
        
    Returns:
        str: 树的文本表示
    """
    # 创建一个反向映射，从移动序列到fiber_id
    move_seq_to_id = {}
    for fiber_id, fiber in fibers.items():
        # 将移动转换为元组以便作为字典键
        move_tuple = tuple(str(move) for move in fiber.moves)
        move_seq_to_id[move_tuple] = fiber_id
    
    # 生成文本表示
    lines = ["树的文本可视化:"]
    _visualize_node(fibers, 
                   root_id, 
                   [], 
                   lines, 
                   0, 
                   max_depth, 
                   include_stats, 
                   move_seq_to_id,
                   set())
    
    return "\n".join(lines)

def _visualize_node(fibers: Dict[str, Fiber], 
                   node_id: str, 
                   path: List[str], 
                   lines: List[str], 
                   depth: int, 
                   max_depth: Optional[int], 
                   include_stats: bool, 
                   move_seq_to_id: Dict[tuple, str],
                   visited: Set[str]) -> None:
    """
    递归辅助函数，用于生成单个节点及其子节点的文本表示
    
    Args:
        fibers: 包含所有Fiber的字典
        node_id: 当前节点的ID
        path: 当前路径（移动字符串列表）
        lines: 输出行列表
        depth: 当前深度
        max_depth: 最大深度
        include_stats: 是否包含统计信息
        move_seq_to_id: 从移动序列到fiber_id的映射
        visited: 已访问节点的集合
    """
    # 避免循环
    if node_id in visited:
        return
    visited.add(node_id)
    
    # 如果达到最大深度，则停止递归
    if max_depth is not None and depth > max_depth:
        return
    
    # 获取当前fiber
    fiber = fibers.get(node_id)
    if fiber is None:
        return
    
    # 生成当前节点的文本表示
    indent = "  " * depth
    node_text = f"{indent}{'→ ' if depth > 0 else ''}"
    
    # 添加移动名称
    if depth > 0 and path:
        node_text += f"{path[-1]}"
    else:
        node_text += "根节点"
    
    # 添加统计信息
    if include_stats:
        visits = fiber.stats['visit_count']
        win_rate = fiber.get_win_rate()
        node_text += f" (访问: {visits}, 胜率: {win_rate:.2f})"
    
    lines.append(node_text)
    
    # 查找所有子节点
    children = _find_children(path, move_seq_to_id, fibers)
    
    # 递归处理子节点
    for child_move, child_id in children:
        new_path = path + [child_move]
        _visualize_node(fibers, 
                        child_id, 
                        new_path, 
                        lines, 
                        depth + 1, 
                        max_depth, 
                        include_stats, 
                        move_seq_to_id,
                        visited)

def _find_children(path: List[str], 
                  move_seq_to_id: Dict[tuple, str], 
                  fibers: Dict[str, Fiber]) -> List[tuple]:
    """
    查找给定路径的所有子节点
    
    Args:
        path: 当前路径（移动字符串列表）
        move_seq_to_id: 从移动序列到fiber_id的映射
        fibers: 包含所有Fiber的字典
        
    Returns:
        List[tuple]: 子节点列表，每项包含 (移动字符串, fiber_id)
    """
    # 保存所有可能的子节点
    children = []
    path_tuple = tuple(path)
    
    # 遍历所有fiber
    for seq, fiber_id in move_seq_to_id.items():
        # 如果序列长度比当前路径长1，且前缀匹配，则为子节点
        if len(seq) == len(path) + 1 and seq[:len(path)] == path_tuple:
            # 提取子节点的移动
            child_move = seq[-1]
            children.append((child_move, fiber_id))
    
    return children

def generate_path_summary(fibers: Dict[str, Fiber], 
                         min_visits: int = 1, 
                         sort_by: str = 'win_rate') -> str:
    """
    生成路径摘要信息
    
    Args:
        fibers: 包含所有Fiber的字典
        min_visits: 最小访问次数阈值
        sort_by: 排序依据，'win_rate'或'visits'
        
    Returns:
        str: 路径摘要文本
    """
    # 收集所有有效路径
    paths = []
    for fiber_id, fiber in fibers.items():
        # 跳过访问次数低于阈值的fiber
        if fiber.stats['visit_count'] < min_visits:
            continue
        
        # 构建路径字符串
        path_str = " → ".join([str(m) for m in fiber.moves]) or "根节点"
        win_rate = fiber.get_win_rate()
        visits = fiber.stats['visit_count']
        
        paths.append((path_str, win_rate, visits))
    
    # 排序
    if sort_by == 'win_rate':
        paths.sort(key=lambda x: (x[1], x[2]), reverse=True)
    else:  # sort_by == 'visits'
        paths.sort(key=lambda x: (x[2], x[1]), reverse=True)
    
    # 生成摘要文本
    lines = ["路径摘要:"]
    for i, (path, win_rate, visits) in enumerate(paths, 1):
        lines.append(f"{i}. {path} - 胜率: {win_rate:.2f}, 访问: {visits}")
    
    return "\n".join(lines) 