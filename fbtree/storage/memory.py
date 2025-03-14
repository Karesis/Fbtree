"""
内存存储: 使用内存字典实现的存储后端
"""

import json
from typing import List, Dict, Optional, Any
import logging
import copy

from .base import StorageInterface
from ..core.fiber import Fiber

class MemoryStorage(StorageInterface):
    """基于内存的存储实现
    
    使用Python字典在内存中存储Fiber对象。
    快速但非持久化，适合临时分析和小型数据集。
    """
    
    def __init__(self, logger: logging.Logger = None):
        """初始化内存存储
        
        Args:
            logger: 可选的日志记录器
        """
        super().__init__(logger)
        self._store: Dict[str, Fiber] = {}
        self._children_map: Dict[str, List[str]] = {}
        
    def get_fiber(self, fiber_id: str) -> Optional[Fiber]:
        """获取指定ID的Fiber
        
        Args:
            fiber_id: 要获取的Fiber ID
            
        Returns:
            Optional[Fiber]: 找到的Fiber对象，如果不存在则返回None
        """
        return self._store.get(fiber_id)
    
    def save_fiber(self, fiber: Fiber):
        """保存Fiber到存储
        
        Args:
            fiber: 要保存的Fiber对象
        """
        self._store[fiber.fiber_id] = fiber
        
        # 更新父子关系映射
        if fiber.parent_id:
            if fiber.parent_id not in self._children_map:
                self._children_map[fiber.parent_id] = []
            if fiber.fiber_id not in self._children_map[fiber.parent_id]:
                self._children_map[fiber.parent_id].append(fiber.fiber_id)
    
    def get_children(self, fiber_id: str) -> List[str]:
        """获取指定Fiber的所有子Fiber ID
        
        Args:
            fiber_id: 父Fiber ID
            
        Returns:
            List[str]: 子Fiber ID列表
        """
        return self._children_map.get(fiber_id, [])
    
    def remove_fiber(self, fiber_id: str) -> bool:
        """从存储中删除Fiber
        
        Args:
            fiber_id: 要删除的Fiber ID
            
        Returns:
            bool: 操作是否成功
        """
        if fiber_id not in self._store:
            return False
        
        # 从存储中删除
        fiber = self._store.pop(fiber_id)
        
        # 更新父子关系映射
        if fiber.parent_id and fiber.parent_id in self._children_map:
            if fiber_id in self._children_map[fiber.parent_id]:
                self._children_map[fiber.parent_id].remove(fiber_id)
        
        # 删除子映射记录
        if fiber_id in self._children_map:
            del self._children_map[fiber_id]
            
        return True
    
    def get_all_fibers(self) -> Dict[str, Fiber]:
        """获取所有存储的Fiber
        
        Returns:
            Dict[str, Fiber]: Fiber ID到Fiber对象的映射
        """
        return copy.copy(self._store)
    
    def clear(self):
        """清空存储"""
        self._store.clear()
        self._children_map.clear()
    
    def persist(self, path: str):
        """将存储内容持久化到文件
        
        Args:
            path: 输出文件路径
        """
        data = {
            'fibers': {fid: fiber.to_dict() for fid, fiber in self._store.items()},
            'children_map': self._children_map
        }
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        self.logger.info(f"已将{len(self._store)}个Fiber保存到文件：{path}")
    
    def load(self, path: str):
        """从文件加载存储内容
        
        Args:
            path: 输入文件路径
        """
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.clear()
        
        # 加载Fiber
        if 'fibers' in data:
            for fid, fiber_data in data['fibers'].items():
                self._store[fid] = Fiber.from_dict(fiber_data)
        
        # 加载子映射
        if 'children_map' in data:
            self._children_map = data['children_map']
            
        self.logger.info(f"从文件加载了{len(self._store)}个Fiber：{path}") 