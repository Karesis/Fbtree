"""
存储接口: 定义FiberTree存储后端的抽象基类
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
import logging

from ..core.fiber import Fiber

class StorageInterface(ABC):
    """FiberTree存储后端的抽象基类
    
    定义了所有存储实现必须提供的方法。
    """
    
    def __init__(self, logger: logging.Logger = None):
        """初始化存储接口
        
        Args:
            logger: 可选的日志记录器
        """
        self.logger = logger or logging.getLogger(f'{self.__class__.__name__}')
    
    @abstractmethod
    def get_fiber(self, fiber_id: str) -> Optional[Fiber]:
        """获取指定ID的Fiber
        
        Args:
            fiber_id: 要获取的Fiber ID
            
        Returns:
            Optional[Fiber]: 找到的Fiber对象，如果不存在则返回None
        """
        pass
    
    @abstractmethod
    def save_fiber(self, fiber: Fiber):
        """保存Fiber到存储
        
        Args:
            fiber: 要保存的Fiber对象
        """
        pass
    
    @abstractmethod
    def get_children(self, fiber_id: str) -> List[str]:
        """获取指定Fiber的所有子Fiber ID
        
        Args:
            fiber_id: 父Fiber ID
            
        Returns:
            List[str]: 子Fiber ID列表
        """
        pass
    
    @abstractmethod
    def remove_fiber(self, fiber_id: str) -> bool:
        """从存储中删除Fiber
        
        Args:
            fiber_id: 要删除的Fiber ID
            
        Returns:
            bool: 操作是否成功
        """
        pass
    
    @abstractmethod
    def get_all_fibers(self) -> Dict[str, Fiber]:
        """获取所有存储的Fiber
        
        Returns:
            Dict[str, Fiber]: Fiber ID到Fiber对象的映射
        """
        pass
    
    @abstractmethod
    def clear(self):
        """清空存储"""
        pass
    
    @abstractmethod
    def persist(self, path: str):
        """将存储内容持久化到文件
        
        Args:
            path: 输出文件路径
        """
        pass
    
    @abstractmethod
    def load(self, path: str):
        """从文件加载存储内容
        
        Args:
            path: 输入文件路径
        """
        pass 