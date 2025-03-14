"""
序列化工具: 提供数据转换和序列化功能
"""

import json
from typing import Dict, Any, List
import datetime

def dumps(data: Any, indent: int = None, ensure_ascii: bool = False) -> str:
    """将数据转换为JSON字符串
    
    支持基本Python类型和自定义对象（带to_dict方法）的序列化。
    
    Args:
        data: 要序列化的数据
        indent: 缩进空格数，None表示不缩进
        ensure_ascii: 是否确保所有非ASCII字符被转义
        
    Returns:
        str: JSON字符串
    """
    return json.dumps(data, indent=indent, ensure_ascii=ensure_ascii, default=_json_default)

def loads(json_str: str) -> Any:
    """从JSON字符串加载数据
    
    Args:
        json_str: JSON字符串
        
    Returns:
        Any: 解析后的数据
    """
    return json.loads(json_str)

def _json_default(obj: Any) -> Any:
    """处理JSON序列化时的默认转换
    
    支持datetime对象和带to_dict方法的对象。
    
    Args:
        obj: 要转换的对象
        
    Returns:
        转换后的值
    """
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    if hasattr(obj, 'to_dict') and callable(obj.to_dict):
        return obj.to_dict()
    raise TypeError(f"无法序列化类型: {type(obj)}") 