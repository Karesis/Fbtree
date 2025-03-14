"""
缓存管理: 提供高效的LRU缓存实现
"""

from typing import Dict, Any, Optional, TypeVar, Generic
from collections import OrderedDict

T = TypeVar('T')

class LRUCache(Generic[T]):
    """基于LRU（最近最少使用）策略的缓存实现
    
    当缓存达到最大容量时，会自动删除最长时间未使用的项。
    
    属性:
        capacity: 缓存的最大容量
        cache: 有序字典，保存缓存的键值对
    """
    
    def __init__(self, capacity: int = 1000):
        """初始化LRU缓存
        
        Args:
            capacity: 缓存的最大容量
        """
        self.capacity = max(1, capacity)
        self.cache: OrderedDict[str, T] = OrderedDict()
    
    def get(self, key: str) -> Optional[T]:
        """获取缓存项
        
        如果项存在，会将其移动到最近使用的位置。
        
        Args:
            key: 缓存项的键
            
        Returns:
            Optional[T]: 缓存的值，如果不存在则返回None
        """
        if key not in self.cache:
            return None
            
        # 将访问的项移到末尾（最近使用）
        value = self.cache.pop(key)
        self.cache[key] = value
        return value
    
    def put(self, key: str, value: T):
        """添加或更新缓存项
        
        如果键已存在，会更新值并将其移动到最近使用的位置。
        如果缓存已满，会移除最久未使用的项。
        
        Args:
            key: 缓存项的键
            value: 要缓存的值
        """
        # 如果键已存在，先移除它
        if key in self.cache:
            self.cache.pop(key)
        # 如果缓存已满，移除最久未使用的项（第一个）
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
            
        # 添加到末尾（最近使用）
        self.cache[key] = value
    
    def remove(self, key: str) -> bool:
        """从缓存中移除项
        
        Args:
            key: 要移除的缓存项的键
            
        Returns:
            bool: 如果项存在并被移除则返回True，否则返回False
        """
        if key in self.cache:
            self.cache.pop(key)
            return True
        return False
    
    def clear(self):
        """清空缓存"""
        self.cache.clear()
    
    def __len__(self) -> int:
        """返回缓存中的项数"""
        return len(self.cache)
    
    def __contains__(self, key: str) -> bool:
        """检查键是否在缓存中"""
        return key in self.cache 