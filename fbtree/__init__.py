"""
FiberTree: 专注于存储和分析顺序决策路径的数据库系统

FiberTree 帮助您跟踪、分析和优化决策过程，
通过记录决策路径（fiber）及其结果，为您提供深入的数据分析和决策支持。

基本用法:
    from fbtree import create_tree, Move
    
    # 创建一个树
    tree = create_tree()
    
    # 开始构建路径
    tree.start_path()
    
    # 添加移动到路径
    tree.add_move(Move(1))
    tree.add_move(Move(2))
    tree.add_move(Move(3))
    
    # 记录结果
    tree.record_outcome('win')
    
    # 获取统计信息
    stats = tree.get_statistics()
"""

from .core.move import Move
from .core.fiber import Fiber
from .core.tree import FiberTree

# 简化的接口函数
def create_tree(storage_type='memory', db_path=None, max_cache_size=1000):
    """
    创建一个新的FiberTree，使用简化的参数。
    
    Args:
        storage_type: 'memory' (更快，非持久化) 或 'sqlite' (持久化)
        db_path: SQLite数据库文件路径（当storage_type='sqlite'时需要）
        max_cache_size: 内存缓存的最大项数
        
    Returns:
        FiberTree: 新创建的树实例
    """
    return FiberTree(storage_type=storage_type, db_path=db_path, max_cache_size=max_cache_size)

def load_tree(file_path, storage_type='memory', db_path=None):
    """
    从JSON文件加载FiberTree。
    
    Args:
        file_path: 要加载的JSON文件路径
        storage_type: 'memory' 或 'sqlite'
        db_path: SQLite数据库路径（当storage_type='sqlite'时需要）
        
    Returns:
        FiberTree: 加载的树实例
    """
    return FiberTree.import_from_json(file_path, storage_type, db_path)

__all__ = [
    'Move',
    'Fiber',
    'FiberTree',
    'create_tree',
    'load_tree'
]

# 版本信息
__version__ = "1.1.1"