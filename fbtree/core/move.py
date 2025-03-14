"""
Move类: 表示决策树中单个决策/移动的通用类
"""

from typing import Dict, Any, TypeVar, Generic
from dataclasses import dataclass

T = TypeVar('T')

@dataclass
class Move(Generic[T]):
    """表示一个移动/决策的通用类
    
    一个Move实例表示决策序列中的单个决择或行动。它可以存储任意类型的值，
    同时每个移动还可以关联额外的元数据。
    
    属性:
        value: 任意类型的值，表示此移动的内容
        metadata: 与此移动相关的任意元数据字典
    """
    value: T
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """初始化后处理，确保metadata不为None"""
        if self.metadata is None:
            self.metadata = {}
    
    def __eq__(self, other):
        """比较两个Move是否相等"""
        if not isinstance(other, Move):
            return False
        return self.value == other.value
    
    def __hash__(self):
        """计算Move的哈希值"""
        return hash(self.value)
    
    def __str__(self):
        """返回Move的字符串表示"""
        return str(self.value)
    
    def to_dict(self) -> Dict[str, Any]:
        """将Move转换为字典表示
        
        Returns:
            Dict[str, Any]: 包含Move数据的字典
        """
        return {
            'value': self.value,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Move':
        """从字典创建Move对象
        
        Args:
            data: 包含Move数据的字典
            
        Returns:
            Move: 新创建的Move实例
        """
        return cls(
            value=data['value'],
            metadata=data.get('metadata', {})
        ) 