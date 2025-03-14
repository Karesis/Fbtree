"""
存储模块: 提供多种存储后端实现
"""

from .base import StorageInterface
from .memory import MemoryStorage
from .sqlite import SQLiteStorage

__all__ = ['StorageInterface', 'MemoryStorage', 'SQLiteStorage'] 