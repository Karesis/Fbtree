"""
FiberTree: A path-oriented database for storing and analyzing sequential decision paths.

FiberTree helps you track, analyze and optimize sequential decision processes by storing 
decision paths (fibers) and their outcomes.

Basic usage:
    from fbtree import FiberTree, Move
    
    # Create a tree
    tree = FiberTree()
    
    # Start building a path
    tree.start_path()
    
    # Add moves to the path
    tree.add_move(Move(1))
    tree.add_move(Move(2))
    tree.add_move(Move(3))
    
    # Record the outcome
    tree.record_outcome('win')
    
    # Get statistics
    stats = tree.get_statistics()
"""

from .main import FiberTree, Fiber, Move

# Simplified interface
def create_tree(storage_type='memory', db_path=None, max_cache_size=1000):
    """
    Create a new FiberTree with simplified parameters.
    
    Args:
        storage_type: 'memory' (faster, non-persistent) or 'sqlite' (persistent)
        db_path: Path to SQLite database file (required if storage_type='sqlite')
        max_cache_size: Maximum number of fibers to cache in memory
        
    Returns:
        FiberTree: A new tree instance
    """
    return FiberTree(storage_type=storage_type, db_path=db_path, max_cache_size=max_cache_size)

def load_tree(file_path, storage_type='memory', db_path=None):
    """
    Load a FiberTree from a JSON file.
    
    Args:
        file_path: Path to the JSON file to load
        storage_type: 'memory' or 'sqlite' for the loaded tree
        db_path: Path to SQLite database (required if storage_type='sqlite')
        
    Returns:
        FiberTree: The loaded tree instance
    """
    return FiberTree.import_from_json(file_path, storage_type, db_path)

# Add simplified method aliases to FiberTree class
FiberTree.start_path = FiberTree.start_adding_mode
FiberTree.end_path = FiberTree.end_adding_mode
FiberTree.record_outcome = FiberTree.update_statistics
FiberTree.save = FiberTree.export_to_json

# Version info
__version__ = "1.0.0"