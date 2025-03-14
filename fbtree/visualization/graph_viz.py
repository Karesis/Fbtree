"""
图形可视化模块: 提供树结构的图形化可视化
"""

from typing import Dict, Optional, List, Set, Any, Tuple
import json
from ..core.fiber import Fiber


def generate_graphviz(fibers: Dict[str, Fiber], 
                     root_id: str = 'root', 
                     max_depth: Optional[int] = None,
                     include_stats: bool = True,
                     theme: str = 'light') -> str:
    """
    生成Graphviz DOT格式的树表示
    
    Args:
        fibers: 包含所有Fiber的字典
        root_id: 根节点的ID
        max_depth: 最大可视化深度，None表示不限制
        include_stats: 是否包含统计信息
        theme: 可视化主题，'light'或'dark'
        
    Returns:
        str: Graphviz DOT格式表示
    """
    # 创建一个反向映射，从移动序列到fiber_id
    move_seq_to_id = {}
    for fiber_id, fiber in fibers.items():
        # 将移动转换为元组以便作为字典键
        move_tuple = tuple(str(move) for move in fiber.moves)
        move_seq_to_id[move_tuple] = fiber_id
    
    # 确定颜色主题
    if theme == 'light':
        bg_color = 'white'
        node_color = 'lightblue'
        edge_color = 'gray'
        text_color = 'black'
    else:  # theme == 'dark'
        bg_color = '#2d2d2d'
        node_color = '#3a546a'
        edge_color = '#555555'
        text_color = 'white'
    
    # 开始构建DOT字符串
    dot = [
        'digraph FiberTree {',
        f'  bgcolor="{bg_color}";',
        f'  node [style="filled", fillcolor="{node_color}", fontcolor="{text_color}"];',
        f'  edge [color="{edge_color}"];',
    ]
    
    # 节点和边的集合
    nodes = set()
    edges = set()
    
    # 递归生成节点和边
    _generate_graphviz_elements(
        fibers,
        root_id,
        [],
        nodes,
        edges,
        0,
        max_depth,
        include_stats,
        move_seq_to_id,
        set()
    )
    
    # 添加所有节点
    for node_id, label in nodes:
        dot.append(f'  "{node_id}" [label="{label}"];')
    
    # 添加所有边
    for src, dst, label in edges:
        dot.append(f'  "{src}" -> "{dst}" [label="{label}"];')
    
    # 结束DOT字符串
    dot.append('}')
    
    return '\n'.join(dot)


def _generate_graphviz_elements(
    fibers: Dict[str, Fiber],
    node_id: str,
    path: List[str],
    nodes: Set[Tuple[str, str]],
    edges: Set[Tuple[str, str, str]],
    depth: int,
    max_depth: Optional[int],
    include_stats: bool,
    move_seq_to_id: Dict[tuple, str],
    visited: Set[str]
) -> None:
    """
    递归生成Graphviz图形的节点和边
    
    Args:
        fibers: 包含所有Fiber的字典
        node_id: 当前节点ID
        path: 当前路径
        nodes: 节点集合
        edges: 边集合
        depth: 当前深度
        max_depth: 最大深度
        include_stats: 是否包含统计数据
        move_seq_to_id: 移动序列到ID的映射
        visited: 已访问节点集合
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
    
    # 创建节点标签
    node_label = "根节点" if depth == 0 else path[-1]
    
    # 添加统计信息
    if include_stats:
        visits = fiber.stats['visit_count']
        win_rate = fiber.get_win_rate()
        node_label += f"\\n访问: {visits}\\n胜率: {win_rate:.2f}"
    
    # 添加节点
    nodes.add((node_id, node_label))
    
    # 查找所有子节点
    children = _find_children(path, move_seq_to_id, fibers)
    
    # 递归处理子节点
    for child_move, child_id in children:
        # 添加边
        edges.add((node_id, child_id, child_move))
        
        # 处理子节点
        new_path = path + [child_move]
        _generate_graphviz_elements(
            fibers,
            child_id,
            new_path,
            nodes,
            edges,
            depth + 1,
            max_depth,
            include_stats,
            move_seq_to_id,
            visited
        )


def _find_children(
    path: List[str],
    move_seq_to_id: Dict[tuple, str],
    fibers: Dict[str, Fiber]
) -> List[tuple]:
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


def generate_d3_json(fibers: Dict[str, Fiber], 
                    root_id: str = 'root',
                    max_depth: Optional[int] = None) -> str:
    """
    生成用于D3.js可视化的JSON数据
    
    Args:
        fibers: 包含所有Fiber的字典
        root_id: 根节点的ID
        max_depth: 最大可视化深度，None表示不限制
        
    Returns:
        str: JSON字符串，可用于D3.js树形图
    """
    # 创建一个反向映射，从移动序列到fiber_id
    move_seq_to_id = {}
    for fiber_id, fiber in fibers.items():
        # 将移动转换为元组以便作为字典键
        move_tuple = tuple(str(move) for move in fiber.moves)
        move_seq_to_id[move_tuple] = fiber_id
    
    # 递归构建树形结构
    tree_data = _build_d3_tree(
        fibers,
        root_id,
        [],
        0,
        max_depth,
        move_seq_to_id,
        set()
    )
    
    # 转换为JSON字符串
    return json.dumps(tree_data, ensure_ascii=False, indent=2)


def _build_d3_tree(
    fibers: Dict[str, Fiber],
    node_id: str,
    path: List[str],
    depth: int,
    max_depth: Optional[int],
    move_seq_to_id: Dict[tuple, str],
    visited: Set[str]
) -> Dict[str, Any]:
    """
    递归构建D3.js树形结构
    
    Args:
        fibers: 包含所有Fiber的字典
        node_id: 当前节点ID
        path: 当前路径
        depth: 当前深度
        max_depth: 最大深度
        move_seq_to_id: 移动序列到ID的映射
        visited: 已访问节点集合
        
    Returns:
        Dict[str, Any]: D3树节点数据
    """
    # 避免循环
    if node_id in visited:
        return None
    visited.add(node_id)
    
    # 如果达到最大深度，则停止递归
    if max_depth is not None and depth > max_depth:
        return None
    
    # 获取当前fiber
    fiber = fibers.get(node_id)
    if fiber is None:
        return None
    
    # 创建节点数据
    node_data = {
        "id": node_id,
        "name": "根节点" if depth == 0 else path[-1],
        "visits": fiber.stats['visit_count'],
        "win_rate": fiber.get_win_rate(),
        "depth": depth,
        "children": []
    }
    
    # 查找所有子节点
    children = _find_children(path, move_seq_to_id, fibers)
    
    # 递归处理子节点
    for child_move, child_id in children:
        new_path = path + [child_move]
        child_data = _build_d3_tree(
            fibers,
            child_id,
            new_path,
            depth + 1,
            max_depth,
            move_seq_to_id,
            visited
        )
        
        if child_data:
            node_data["children"].append(child_data)
    
    return node_data 