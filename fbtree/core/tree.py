"""
FiberTree: 管理决策路径集合的树形数据库
"""

from typing import List, Dict, Optional, Any, Tuple, Union
import logging
import json
import copy
from collections import Counter

from .move import Move
from .fiber import Fiber
from ..storage import StorageInterface, MemoryStorage, SQLiteStorage

class FiberTree:
    """管理决策路径集合的树形数据库
    
    提供添加、查询、分析和可视化决策路径的功能。
    
    属性:
        storage: 存储后端接口
        logger: 日志记录器
        current_path: 当前正在构建的路径
        current_fiber: 当前Fiber对象
        adding_mode: 是否处于添加模式
    """
    
    def __init__(self, 
                 storage_type: str = 'memory',
                 db_path: str = None,
                 max_cache_size: int = 1000,
                 logger: logging.Logger = None):
        """初始化FiberTree
        
        Args:
            storage_type: 'memory' 或 'sqlite'
            db_path: SQLite数据库路径（当storage_type='sqlite'时需要）
            max_cache_size: 内存缓存的最大项数
            logger: 可选的日志记录器
        """
        self.logger = logger or logging.getLogger('FiberTree')
        
        # 初始化存储后端
        if storage_type == 'memory':
            self.storage = MemoryStorage(logger=self.logger)
        elif storage_type == 'sqlite':
            if not db_path:
                raise ValueError("使用SQLite存储时必须提供db_path")
            self.storage = SQLiteStorage(db_path=db_path, logger=self.logger)
        else:
            raise ValueError(f"不支持的存储类型: {storage_type}")
        
        # 当前正在构建的路径
        self.current_path: List[Move] = []
        self.current_fiber: Optional[Fiber] = None
        self.adding_mode = False
        
        # 创建根Fiber（如果不存在）
        root = self.storage.get_fiber('root')
        if not root:
            root = Fiber(moves=[], fiber_id='root')
            self.storage.save_fiber(root)
    
    def start_path(self):
        """开始添加模式以构建新路径
        
        等同于start_adding_mode方法，提供更直观的命名。
        """
        self.start_adding_mode()
    
    def start_adding_mode(self):
        """开始添加模式以构建新路径"""
        self.adding_mode = True
        self.current_fiber = self.storage.get_fiber('root')
        self.current_path = []
    
    def end_path(self):
        """结束添加模式
        
        等同于end_adding_mode方法，提供更直观的命名。
        """
        self.end_adding_mode()
    
    def end_adding_mode(self):
        """结束添加模式"""
        self.adding_mode = False
    
    def add_move(self, move: Move) -> bool:
        """添加一个移动到当前路径
        
        Args:
            move: 要添加的移动
            
        Returns:
            bool: 操作是否成功
        """
        if not self.adding_mode:
            self.logger.warning("在添加模式外调用add_move")
            self.start_adding_mode()
        
        self.current_path.append(move)
        
        # 获取当前Fiber的子节点
        children_ids = self.storage.get_children(self.current_fiber.fiber_id)
        matching_child_id = None
        
        # 检查是否有匹配的子节点
        for child_id in children_ids:
            child = self.storage.get_fiber(child_id)
            if not child or not child.moves:
                continue
                
            if child.moves[0] == move:
                matching_child_id = child_id
                break
        
        if matching_child_id:
            # 找到匹配的子节点，使用它
            self.current_fiber = self.storage.get_fiber(matching_child_id)
        else:
            # 创建新的子Fiber
            new_fiber = Fiber(
                moves=[move],
                parent_id=self.current_fiber.fiber_id
            )
            self.storage.save_fiber(new_fiber)
            self.current_fiber = new_fiber
        
        return True
    
    def add_moves(self, moves: List[Move]) -> bool:
        """批量添加多个移动
        
        Args:
            moves: 要添加的移动列表
            
        Returns:
            bool: 操作是否成功
        """
        if not self.adding_mode:
            self.start_adding_mode()
            
        success = True
        for move in moves:
            if not self.add_move(move):
                success = False
                
        return success
    
    def record_outcome(self, outcome: str):
        """记录当前路径的结果
        
        等同于update_statistics方法，提供更直观的命名。
        
        Args:
            outcome: 'win', 'loss', 或 'draw'
        """
        self.update_statistics(outcome)
    
    def update_statistics(self, outcome: str):
        """更新当前路径的统计信息
        
        Args:
            outcome: 'win', 'loss', 或 'draw'
        """
        if not self.current_fiber:
            self.logger.warning("尝试更新统计信息，但没有当前Fiber")
            return
            
        # 从当前Fiber开始，向上更新所有父Fiber
        fiber = self.current_fiber
        updated_ids = set()
        
        while fiber and fiber.fiber_id not in updated_ids:
            fiber.update_stats(outcome)
            self.storage.save_fiber(fiber)
            updated_ids.add(fiber.fiber_id)
            
            if fiber.parent_id and fiber.parent_id != 'root':
                fiber = self.storage.get_fiber(fiber.parent_id)
            else:
                # 更新根节点
                if fiber.fiber_id != 'root':
                    root = self.storage.get_fiber('root')
                    if root:
                        root.update_stats(outcome)
                        self.storage.save_fiber(root)
                break
    
    def get_complete_path(self) -> List[Move]:
        """获取从根节点到当前节点的完整移动序列
        
        Returns:
            List[Move]: 完整的移动序列
        """
        if not self.current_fiber:
            return []
            
        # 向上追踪路径
        complete_moves = []
        fiber = self.current_fiber
        fiber_chain = []
        
        while fiber and fiber.fiber_id != 'root':
            fiber_chain.append(fiber)
            fiber = self.storage.get_fiber(fiber.parent_id)
        
        # 从上到下构建路径
        for fiber in reversed(fiber_chain):
            complete_moves.extend(fiber.moves)
            
        return complete_moves
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取当前路径的统计信息
        
        Returns:
            Dict[str, Any]: 包含访问次数、胜率等统计数据的字典
        """
        if not self.current_fiber:
            return {
                'visit_count': 0,
                'win_count': 0,
                'loss_count': 0,
                'draw_count': 0,
                'win_rate': 0.0
            }
        
        stats = copy.copy(self.current_fiber.stats)
        stats['win_rate'] = self.current_fiber.get_win_rate()
        return stats
    
    def find_path(self, moves: List[Move]) -> Optional[str]:
        """查找匹配给定移动序列的路径
        
        Args:
            moves: 要查找的移动序列
            
        Returns:
            Optional[str]: 匹配的Fiber ID，如果未找到则为None
        """
        current_fiber_id = 'root'
        remaining_idx = 0
        
        while remaining_idx < len(moves):
            best_match_id, match_len = self._find_matching_fiber(
                current_fiber_id, moves, remaining_idx)
            
            if not best_match_id or match_len == 0:
                return None
                
            current_fiber_id = best_match_id
            remaining_idx += match_len
            
        return current_fiber_id
    
    def _find_matching_fiber(self, current_fiber_id: str, path: List[Move], 
                             start_idx: int) -> Tuple[Optional[str], int]:
        """查找匹配给定路径的下一个fiber
        
        Args:
            current_fiber_id: 当前Fiber ID
            path: 要匹配的完整路径
            start_idx: 路径中的起始索引
            
        Returns:
            Tuple[Optional[str], int]: 匹配的Fiber ID和匹配的移动数量
        """
        if start_idx >= len(path):
            return None, 0
            
        remaining_moves = path[start_idx:]
        child_ids = self.storage.get_children(current_fiber_id)
        
        best_match_id = None
        best_match_len = 0
        
        for child_id in child_ids:
            child = self.storage.get_fiber(child_id)
            if not child:
                continue
                
            # 计算最长匹配前缀
            match_len = 0
            for i in range(min(len(child.moves), len(remaining_moves))):
                if child.moves[i] == remaining_moves[i]:
                    match_len += 1
                else:
                    break
            
            if match_len > 0 and match_len > best_match_len:
                best_match_id = child_id
                best_match_len = match_len
        
        return best_match_id, best_match_len
    
    def get_move_frequency(self, depth: int = 1) -> Dict[str, int]:
        """获取特定深度的移动频率
        
        Args:
            depth: 要分析的深度（从1开始）
            
        Returns:
            Dict[str, int]: 移动值到出现次数的映射
        """
        if depth < 1:
            raise ValueError("深度必须大于0")
            
        counter = Counter()
        all_fibers = self.storage.get_all_fibers()
        
        for fiber_id, fiber in all_fibers.items():
            if fiber_id == 'root' or fiber.is_empty():
                continue
                
            # 跟踪当前深度
            current_depth = 1
            current_fiber = fiber
            
            # 向上查找父节点，直到到达根节点或达到所需深度
            while current_fiber.parent_id and current_fiber.parent_id != 'root':
                parent = all_fibers.get(current_fiber.parent_id)
                if not parent:
                    break
                current_depth += 1
                current_fiber = parent
                
            # 如果找到匹配深度的路径
            if current_depth == depth and not current_fiber.is_empty():
                # 使用第一个移动的值作为键
                move_val = str(current_fiber.moves[0])
                counter[move_val] += 1
        
        return dict(counter)
    
    def get_best_continuation(self, starting_path: List[Move], top_n: int = 3) -> List[Dict[str, Any]]:
        """从给定起始路径找出最佳后续移动
        
        Args:
            starting_path: 起始路径的移动列表
            top_n: 返回的最佳移动数量
            
        Returns:
            List[Dict[str, Any]]: 包含后续移动及其统计信息的列表
        """
        if not starting_path:
            # 如果起始路径为空，返回根节点的所有子节点
            child_ids = self.storage.get_children('root')
            results = []
            
            for child_id in child_ids:
                child = self.storage.get_fiber(child_id)
                if not child or child.is_empty():
                    continue
                    
                move = child.moves[0]
                results.append({
                    'move': str(move),
                    'win_rate': child.get_win_rate(),
                    'visits': child.stats['visit_count']
                })
            
            # 按胜率排序
            results.sort(key=lambda x: x['win_rate'], reverse=True)
            return results[:top_n]
        
        # 查找起始路径的Fiber
        current_fiber_id = self.find_path(starting_path)
        if not current_fiber_id:
            return []
            
        # 获取子节点
        child_ids = self.storage.get_children(current_fiber_id)
        results = []
        
        for child_id in child_ids:
            child = self.storage.get_fiber(child_id)
            if not child or child.is_empty():
                continue
                
            move = child.moves[0]
            results.append({
                'move': str(move),
                'win_rate': child.get_win_rate(),
                'visits': child.stats['visit_count']
            })
        
        # 按胜率排序
        results.sort(key=lambda x: x['win_rate'], reverse=True)
        return results[:top_n]
    
    def prune_tree(self, min_visits: int = None, max_depth: int = None) -> int:
        """修剪树中的低频或深度过大的路径
        
        Args:
            min_visits: 最小访问次数，低于此值的路径将被删除
            max_depth: 最大深度，超过此深度的路径将被删除
            
        Returns:
            int: 删除的路径数量
        """
        if min_visits is None and max_depth is None:
            return 0
            
        removed_count = 0
        all_fibers = self.storage.get_all_fibers()
        
        # 计算每个Fiber的深度
        depth_map = {}
        for fid, fiber in all_fibers.items():
            if fid == 'root':
                depth_map[fid] = 0
                continue
                
            # 计算深度
            depth = 1
            current_id = fiber.parent_id
            while current_id and current_id != 'root':
                depth += 1
                parent = all_fibers.get(current_id)
                if not parent:
                    break
                current_id = parent.parent_id
                
            depth_map[fid] = depth
        
        # 执行修剪
        for fid, fiber in all_fibers.items():
            if fid == 'root':
                continue
                
            should_remove = False
            
            # 检查访问次数
            if min_visits is not None and fiber.stats['visit_count'] < min_visits:
                should_remove = True
                
            # 检查深度
            if max_depth is not None and depth_map.get(fid, 0) > max_depth:
                should_remove = True
                
            if should_remove:
                # 递归删除此Fiber及其所有子节点
                removed_count += self._remove_fiber_recursive(fid)
        
        return removed_count
    
    def _remove_fiber_recursive(self, fiber_id: str) -> int:
        """递归删除Fiber及其所有子节点
        
        Args:
            fiber_id: 要删除的Fiber ID
            
        Returns:
            int: 删除的节点数量
        """
        if fiber_id == 'root':
            return 0
            
        count = 0
        
        # 首先递归删除所有子节点
        children = self.storage.get_children(fiber_id)
        for child_id in children:
            count += self._remove_fiber_recursive(child_id)
            
        # 然后删除此节点
        if self.storage.remove_fiber(fiber_id):
            count += 1
            
        return count
    
    def export_to_json(self, file_path: str):
        """将树导出为JSON文件
        
        Args:
            file_path: 输出文件路径
        """
        self.storage.persist(file_path)
    
    def save(self, file_path: str):
        """保存树到文件（为保持向后兼容）
        
        Args:
            file_path: 输出文件路径
        """
        self.export_to_json(file_path)
    
    @classmethod
    def import_from_json(cls, file_path: str, storage_type: str = 'memory', db_path: str = None) -> 'FiberTree':
        """从JSON文件导入树
        
        Args:
            file_path: JSON文件路径
            storage_type: 新树的存储类型
            db_path: SQLite数据库路径（当storage_type='sqlite'时需要）
            
        Returns:
            FiberTree: 新导入的树实例
        """
        tree = cls(storage_type=storage_type, db_path=db_path)
        tree.storage.load(file_path)
        return tree
    
    def visualize(self, max_depth: int = 5, output_format: str = 'text') -> str:
        """可视化决策树
        
        Args:
            max_depth: 最大显示深度
            output_format: 输出格式，'text'或'graphviz'
            
        Returns:
            str: 可视化结果字符串
        """
        if output_format == 'text':
            return self._visualize_text(max_depth)
        elif output_format == 'graphviz':
            return self._visualize_graphviz(max_depth)
        else:
            raise ValueError(f"不支持的输出格式: {output_format}")
    
    def _visualize_text(self, max_depth: int) -> str:
        """以文本形式可视化树
        
        Args:
            max_depth: 最大显示深度
            
        Returns:
            str: 文本可视化结果
        """
        lines = ["FiberTree 可视化:"]
        
        def _visualize_node(node_id: str, prefix: str, depth: int):
            if depth > max_depth:
                return
                
            node = self.storage.get_fiber(node_id)
            if not node:
                return
                
            # 获取节点显示信息
            if node_id == 'root':
                node_str = "ROOT"
            else:
                moves_str = ', '.join(str(m) for m in node.moves)
                visits = node.stats['visit_count']
                win_rate = node.get_win_rate() * 100
                node_str = f"{moves_str} [访问：{visits}, 胜率：{win_rate:.1f}%]"
                
            lines.append(f"{prefix}{node_str}")
            
            # 递归处理子节点
            children = self.storage.get_children(node_id)
            for i, child_id in enumerate(children):
                if i == len(children) - 1:
                    # 最后一个子节点
                    _visualize_node(child_id, prefix + "└── ", depth + 1)
                else:
                    _visualize_node(child_id, prefix + "├── ", depth + 1)
        
        _visualize_node('root', "", 0)
        return '\n'.join(lines)
    
    def _visualize_graphviz(self, max_depth: int) -> str:
        """以Graphviz DOT格式可视化树
        
        Args:
            max_depth: 最大显示深度
            
        Returns:
            str: Graphviz DOT格式字符串
        """
        lines = ["digraph G {", "  node [shape=box];"]
        
        def _visualize_node(node_id: str, depth: int):
            if depth > max_depth:
                return
                
            node = self.storage.get_fiber(node_id)
            if not node:
                return
                
            # 获取节点显示信息
            if node_id == 'root':
                node_label = "ROOT"
            else:
                moves_str = ', '.join(str(m) for m in node.moves)
                visits = node.stats['visit_count']
                win_rate = node.get_win_rate() * 100
                node_label = f"{moves_str}\\nVisits: {visits}, Win: {win_rate:.1f}%"
                
            # 添加节点
            lines.append(f'  "{node_id}" [label="{node_label}"];')
            
            # 递归处理子节点
            children = self.storage.get_children(node_id)
            for child_id in children:
                child = self.storage.get_fiber(child_id)
                if not child:
                    continue
                    
                lines.append(f'  "{node_id}" -> "{child_id}";')
                _visualize_node(child_id, depth + 1)
        
        _visualize_node('root', 0)
        lines.append("}")
        return '\n'.join(lines) 