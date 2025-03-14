"""
Fiber类: 表示决策路径的容器类
"""

from typing import List, Dict, Any, Optional
import uuid
from .move import Move

class Fiber:
    """表示决策路径的容器类
    
    Fiber表示一系列移动的容器，形成一个决策路径。
    每个Fiber包含移动序列和相关统计数据（如访问次数、胜率等）。
    
    属性:
        moves: 此Fiber包含的移动列表
        fiber_id: 唯一标识符
        parent_id: 父Fiber的ID（如果有）
        metadata: 与此Fiber相关的任意元数据
        stats: 统计信息字典，包含访问次数和不同结果的计数
    """
    
    def __init__(self, 
                 moves: List[Move],
                 fiber_id: str = None,
                 parent_id: str = None,
                 metadata: Dict[str, Any] = None):
        """初始化一个Fiber
        
        Args:
            moves: 此Fiber包含的移动列表
            fiber_id: 唯一标识符（如果为None则自动生成）
            parent_id: 父Fiber的ID（如果有）
            metadata: 与此Fiber相关的任意元数据
        """
        self.moves = moves.copy()
        self.fiber_id = fiber_id if fiber_id else str(uuid.uuid4())
        self.parent_id = parent_id
        self.metadata = metadata if metadata else {}
        self.stats = {
            'visit_count': 0,
            'win_count': 0,
            'loss_count': 0,
            'draw_count': 0
        }
    
    def is_empty(self) -> bool:
        """检查是否为空Fiber
        
        Returns:
            bool: 如果Fiber不包含任何移动则返回True
        """
        return len(self.moves) == 0
    
    def __len__(self) -> int:
        """获取Fiber长度（移动数量）
        
        Returns:
            int: Fiber中包含的移动数量
        """
        return len(self.moves)
    
    def __getitem__(self, index) -> Move:
        """通过索引访问移动
        
        Args:
            index: 要访问的移动索引
            
        Returns:
            Move: 指定索引处的Move对象
        """
        return self.moves[index]
    
    def get_win_rate(self) -> float:
        """计算胜率
        
        Returns:
            float: 胜率（0.0到1.0之间的值）
        """
        if self.stats['visit_count'] == 0:
            return 0.0
        return self.stats['win_count'] / self.stats['visit_count']
    
    def update_stats(self, outcome: str):
        """更新统计信息
        
        Args:
            outcome: 'win', 'loss', 'draw' 之一
        """
        self.stats['visit_count'] += 1
        if outcome == 'win':
            self.stats['win_count'] += 1
        elif outcome == 'loss':
            self.stats['loss_count'] += 1
        elif outcome == 'draw':
            self.stats['draw_count'] += 1
    
    def add_metadata(self, key: str, value: Any):
        """添加或更新元数据
        
        Args:
            key: 元数据键
            value: 元数据值
        """
        self.metadata[key] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """将Fiber转换为字典表示
        
        Returns:
            Dict[str, Any]: 包含Fiber数据的字典
        """
        return {
            'fiber_id': self.fiber_id,
            'parent_id': self.parent_id,
            'moves': [move.to_dict() for move in self.moves],
            'metadata': self.metadata,
            'stats': self.stats
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Fiber':
        """从字典创建Fiber对象
        
        Args:
            data: 包含Fiber数据的字典
            
        Returns:
            Fiber: 新创建的Fiber实例
        """
        fiber = cls(
            moves=[Move.from_dict(m) for m in data['moves']],
            fiber_id=data['fiber_id'],
            parent_id=data['parent_id'],
            metadata=data.get('metadata', {})
        )
        fiber.stats = data.get('stats', {
            'visit_count': 0,
            'win_count': 0,
            'loss_count': 0,
            'draw_count': 0
        })
        return fiber 