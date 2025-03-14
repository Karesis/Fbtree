"""
SQLite存储: 使用SQLite数据库实现的持久化存储后端
"""

import json
import os
import sqlite3
from typing import List, Dict, Optional, Any
import logging

from .base import StorageInterface
from ..core.fiber import Fiber

class SQLiteStorage(StorageInterface):
    """基于SQLite的存储实现
    
    使用SQLite数据库持久化存储Fiber对象。
    适合需要持久化存储的场景和较大数据集。
    """
    
    def __init__(self, db_path: str, logger: logging.Logger = None):
        """初始化SQLite存储
        
        Args:
            db_path: SQLite数据库文件路径
            logger: 可选的日志记录器
        """
        super().__init__(logger)
        self.db_path = db_path
        self._cache: Dict[str, Fiber] = {}
        self._init_database()
    
    def _init_database(self):
        """初始化SQLite数据库"""
        if not self.db_path:
            raise ValueError("使用SQLite存储时必须提供db_path")
            
        # 确保目录存在
        os.makedirs(os.path.dirname(os.path.abspath(self.db_path)), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建fibers表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS fibers (
            fiber_id TEXT PRIMARY KEY,
            parent_id TEXT,
            data TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_parent_id ON fibers(parent_id)')
        
        conn.commit()
        conn.close()
    
    def get_fiber(self, fiber_id: str) -> Optional[Fiber]:
        """获取指定ID的Fiber
        
        Args:
            fiber_id: 要获取的Fiber ID
            
        Returns:
            Optional[Fiber]: 找到的Fiber对象，如果不存在则返回None
        """
        # 首先检查缓存
        if fiber_id in self._cache:
            return self._cache[fiber_id]
        
        # 否则从数据库获取
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT data FROM fibers WHERE fiber_id = ?', (fiber_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            fiber_data = json.loads(result[0])
            fiber = Fiber.from_dict(fiber_data)
            self._cache[fiber_id] = fiber
            return fiber
        
        return None
    
    def save_fiber(self, fiber: Fiber):
        """保存Fiber到存储
        
        Args:
            fiber: 要保存的Fiber对象
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        fiber_data = json.dumps(fiber.to_dict())
        
        cursor.execute(
            '''
            INSERT OR REPLACE INTO fibers (fiber_id, parent_id, data, last_updated)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ''',
            (fiber.fiber_id, fiber.parent_id, fiber_data)
        )
        
        conn.commit()
        conn.close()
        
        # 更新缓存
        self._cache[fiber.fiber_id] = fiber
    
    def get_children(self, fiber_id: str) -> List[str]:
        """获取指定Fiber的所有子Fiber ID
        
        Args:
            fiber_id: 父Fiber ID
            
        Returns:
            List[str]: 子Fiber ID列表
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT fiber_id FROM fibers WHERE parent_id = ?', (fiber_id,))
        results = cursor.fetchall()
        conn.close()
        
        return [r[0] for r in results]
    
    def remove_fiber(self, fiber_id: str) -> bool:
        """从存储中删除Fiber
        
        Args:
            fiber_id: 要删除的Fiber ID
            
        Returns:
            bool: 操作是否成功
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 检查是否存在
        cursor.execute('SELECT 1 FROM fibers WHERE fiber_id = ?', (fiber_id,))
        if not cursor.fetchone():
            conn.close()
            return False
        
        # 删除
        cursor.execute('DELETE FROM fibers WHERE fiber_id = ?', (fiber_id,))
        conn.commit()
        conn.close()
        
        # 从缓存中删除
        if fiber_id in self._cache:
            del self._cache[fiber_id]
            
        return True
    
    def get_all_fibers(self) -> Dict[str, Fiber]:
        """获取所有存储的Fiber
        
        Returns:
            Dict[str, Fiber]: Fiber ID到Fiber对象的映射
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT fiber_id, data FROM fibers')
        results = cursor.fetchall()
        conn.close()
        
        fibers = {}
        for fid, data in results:
            fiber_data = json.loads(data)
            fibers[fid] = Fiber.from_dict(fiber_data)
        
        # 更新缓存
        self._cache.update(fibers)
        
        return fibers
    
    def clear(self):
        """清空存储"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM fibers')
        conn.commit()
        conn.close()
        
        self._cache.clear()
    
    def persist(self, path: str):
        """将存储内容持久化到文件
        
        Args:
            path: 输出文件路径
        """
        # SQLite本身就是持久化的，但我们可以导出为JSON格式
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT fiber_id, parent_id, data FROM fibers')
        results = cursor.fetchall()
        conn.close()
        
        # 构建导出数据
        export_data = {
            'fibers': {}
        }
        
        for fid, parent_id, data in results:
            fiber_data = json.loads(data)
            export_data['fibers'][fid] = fiber_data
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
            
        self.logger.info(f"已将{len(export_data['fibers'])}个Fiber导出到文件：{path}")
    
    def load(self, path: str):
        """从文件加载存储内容
        
        Args:
            path: 输入文件路径
        """
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.clear()
        
        if 'fibers' in data:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for fid, fiber_data in data['fibers'].items():
                parent_id = fiber_data.get('parent_id')
                data_str = json.dumps(fiber_data)
                
                cursor.execute(
                    '''
                    INSERT OR REPLACE INTO fibers (fiber_id, parent_id, data)
                    VALUES (?, ?, ?)
                    ''',
                    (fid, parent_id, data_str)
                )
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"从文件加载了{len(data['fibers'])}个Fiber：{path}")
        else:
            self.logger.warning(f"文件不包含有效的Fiber数据：{path}") 