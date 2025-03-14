# FiberTree Advanced Topics

This document covers advanced usage, optimization strategies, and customization methods for FiberTree.

## Performance Optimization

### Storage Backend Selection

FiberTree provides two storage backends: memory storage and SQLite storage.

- **Memory Storage**: Suitable for smaller trees and scenarios requiring maximum performance. All data is stored in memory and will be lost when the program ends (unless manually exported).

- **SQLite Storage**: Suitable for large trees and scenarios requiring persistence. Data is stored in an SQLite database file, providing better scalability and persistence.

Selection criteria:
- Tree nodes expected to be fewer than 10,000: Memory storage can be used
- Tree nodes expected to exceed 10,000: SQLite storage is recommended
- Need for persistence between sessions: Use SQLite storage

Example:
```python
# Create a large persistent tree
tree = create_tree(
    storage_type='sqlite',
    db_path='large_tree.db',
    cache_size=1000  # Adjust cache size
)
```

### Cache Optimization

FiberTree internally uses an LRU cache to improve performance for frequently accessed nodes. You can adjust the cache size to balance memory usage and performance:

```python
# Set a smaller cache for memory-intensive applications
tree = create_tree(storage_type='memory', cache_size=100)

# Set a larger cache for performance-sensitive applications
tree = create_tree(storage_type='sqlite', cache_size=5000)
```

### Batch Operations

For scenarios that need to add a large number of paths, you can use batch operations to improve performance:

```python
# Enable batch mode
tree.start_batch_mode()

# Add multiple paths
for path, outcome in paths_data:
    tree.simulate_path(path, outcome, update_stats=False)  # Don't update statistics immediately

# Complete batch addition, update statistics at once
tree.end_batch_mode()
```

### Tree Pruning Strategies

Regularly pruning the tree can reduce storage space and improve performance:

```python
# Basic pruning - remove nodes with visits below threshold
tree.prune_tree(min_visits=5)

# Advanced pruning - consider both visit count and depth
def custom_prune_condition(fiber, depth):
    """Custom pruning condition"""
    # Higher depth requires higher visit count
    min_visits = depth * 2
    return fiber.stats['visit_count'] < min_visits

tree.prune_tree(custom_condition=custom_prune_condition)
```

## Advanced Analysis Features

### Path Diversity Analysis

Analyze the structural characteristics of the decision tree:

```python
diversity = tree.analyze_path_diversity()

print(f"Total nodes: {diversity['total_fibers']}")
print(f"Maximum depth: {diversity['max_depth']}")
print(f"Average branching factor: {diversity['avg_branching_factor']:.2f}")
print(f"Leaf node ratio: {diversity['leaf_nodes'] / diversity['total_fibers']:.2f}")

# Analyze depth distribution
for depth, count in diversity['depth_distribution'].items():
    print(f"Depth {depth}: {count} nodes")

# View most visited paths
for path in diversity['most_visited_paths'][:5]:
    print(f"ID: {path['fiber_id']}, Visits: {path['visits']}")
```

### Decision Path Comparison

Compare the performance of different paths:

```python
# Compare two opening strategies
path1 = [Move("center opening"), Move("flank defense")]
path2 = [Move("flank opening"), Move("center attack")]

stats1 = tree.get_path_statistics(path1)
stats2 = tree.get_path_statistics(path2)

print(f"Strategy 1 - Visits: {stats1['visit_count']}, Win rate: {stats1['win_rate']:.2f}")
print(f"Strategy 2 - Visits: {stats2['visit_count']}, Win rate: {stats2['win_rate']:.2f}")

# Analyze subsequent development
cont1 = tree.get_best_continuation(path1, top_n=3)
cont2 = tree.get_best_continuation(path2, top_n=3)

print("Strategy 1 best subsequent actions:")
for move in cont1:
    print(f"  {move['move']} - Win rate: {move['win_rate']:.2f}")

print("Strategy 2 best subsequent actions:")
for move in cont2:
    print(f"  {move['move']} - Win rate: {move['win_rate']:.2f}")
```

### Dynamic Evaluation

Adjust evaluation criteria based on context:

```python
def dynamic_evaluation(move_stats, context):
    """Dynamically adjust action evaluation based on context"""
    base_score = move_stats['win_rate']
    
    # Example: When resources are tight, favor low-risk actions
    if context.get('resources') == 'low':
        uncertainty = move_stats['visits'] / (move_stats['visits'] + 50)
        return base_score * (1 - uncertainty * 0.5)
    
    # Example: When behind, favor high-reward actions
    if context.get('score_difference') < 0:
        return base_score * 1.2  # Increase weight
    
    return base_score

# Usage
context = {'resources': 'low', 'score_difference': -10}
best_moves = tree.get_best_continuation(path)

# Apply dynamic evaluation
evaluated_moves = [
    {**move, 'adjusted_score': dynamic_evaluation(move, context)}
    for move in best_moves
]

# Sort by adjusted score
evaluated_moves.sort(key=lambda x: x['adjusted_score'], reverse=True)
```

## Extensions and Customization

### Creating Custom Storage Backends

You can create custom storage backends by implementing the storage interface:

```python
from fbtree.storage.base import StorageBase

class CustomStorage(StorageBase):
    """Custom storage backend example"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize your storage
        
    def get_fiber(self, fiber_id):
        # Implement node retrieval
        pass
        
    def save_fiber(self, fiber_id, fiber):
        # Implement node saving
        pass
        
    def remove_fiber(self, fiber_id):
        # Implement node deletion
        pass
        
    def get_all_fibers(self):
        # Implement retrieval of all nodes
        pass
        
    # Implement other necessary methods...

# Using custom storage
from fbtree import FiberTree
tree = FiberTree(storage=CustomStorage(**custom_params))
```

### Extending Move Types

Create custom Move classes to handle domain-specific actions:

```python
from fbtree import Move

class ChessMove(Move):
    """Chess move class"""
    
    def __init__(self, from_pos, to_pos, piece_type, is_capture=False):
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.piece_type = piece_type
        self.is_capture = is_capture
        # Serialize to value
        value = f"{from_pos}-{to_pos}-{piece_type}"
        if is_capture:
            value += "-capture"
        super().__init__(value=value)
    
    def __str__(self):
        """String representation"""
        capture = "x" if self.is_capture else "-"
        return f"{self.piece_type}{self.from_pos}{capture}{self.to_pos}"
        
# Usage
knight_move = ChessMove("e4", "f6", "N", is_capture=True)
tree.add_move(knight_move)
```

### Integrating Machine Learning Models

Integrate FiberTree with machine learning models to optimize decisions:

```python
import numpy as np
from sklearn.ensemble import RandomForestClassifier

class MLEnhancedTree:
    """Machine learning enhanced decision tree"""
    
    def __init__(self, tree, feature_extractor):
        self.tree = tree
        self.feature_extractor = feature_extractor
        self.model = RandomForestClassifier()
        self.trained = False
        
    def train(self):
        """Train the model"""
        X = []
        y = []
        
        # Collect training data from the tree
        for fiber_id, fiber in self.tree:
            if fiber.stats['visit_count'] > 10:  # Only use nodes with enough data
                path = self.tree._get_path_to_fiber(fiber_id)
                features = self.feature_extractor(path)
                X.append(features)
                y.append(fiber.stats['win_rate'])
        
        if len(X) > 0:
            self.model.fit(np.array(X), np.array(y))
            self.trained = True
            
    def predict_best_move(self, current_path):
        """Predict the best subsequent action"""
        # First get candidate actions from the tree
        candidates = self.tree.get_best_continuation(current_path, top_n=10)
        
        if not self.trained or not candidates:
            return candidates
            
        # Predict win rate for each candidate action
        for i, move_info in enumerate(candidates):
            new_path = current_path + [move_info['move']]
            features = self.feature_extractor(new_path)
            predicted_win_rate = self.model.predict([features])[0]
            
            # Combine tree statistics and model predictions
            tree_confidence = min(1.0, move_info['visits'] / 50)
            candidates[i]['predicted_win_rate'] = (
                tree_confidence * move_info['win_rate'] + 
                (1 - tree_confidence) * predicted_win_rate
            )
            
        # Sort by predicted win rate
        candidates.sort(key=lambda x: x['predicted_win_rate'], reverse=True)
        return candidates
```

## Distributed and Parallel Processing

For applications that need to process large-scale data, distributed FiberTree can be implemented:

```python
# Pseudocode example
class DistributedFiberTree:
    """Distributed FiberTree implementation"""
    
    def __init__(self, worker_count, central_db_uri):
        self.worker_count = worker_count
        self.central_db_uri = central_db_uri
        self.worker_trees = []
        
    def initialize_workers(self):
        """Initialize worker nodes"""
        for i in range(self.worker_count):
            # Create local tree for each worker node
            worker_tree = create_tree(
                storage_type='sqlite',
                db_path=f'worker_{i}.db'
            )
            self.worker_trees.append(worker_tree)
            
    def simulate_batch(self, paths_batch):
        """Simulate a batch of paths in parallel"""
        # Assign tasks to worker nodes
        tasks = [[] for _ in range(self.worker_count)]
        for i, path_data in enumerate(paths_batch):
            worker_idx = i % self.worker_count
            tasks[worker_idx].append(path_data)
            
        # Execute in parallel (using multiprocessing or threading)
        import concurrent.futures
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = []
            for worker_idx, task in enumerate(tasks):
                futures.append(
                    executor.submit(self._worker_simulate, worker_idx, task)
                )
            concurrent.futures.wait(futures)
            
    def _worker_simulate(self, worker_idx, paths):
        """Worker node processing function"""
        worker_tree = self.worker_trees[worker_idx]
        for path, outcome in paths:
            worker_tree.simulate_path(path, outcome)
            
    def synchronize(self):
        """Synchronize all worker node data to the central database"""
        central_tree = create_tree(
            storage_type='sqlite',
            db_path=self.central_db_uri
        )
        
        # Merge all worker node trees
        for worker_tree in self.worker_trees:
            central_tree.merge(worker_tree, conflict_strategy='stats_sum')
            
        return central_tree
```

## Security and Encryption

For applications processing sensitive decision data, encrypted storage can be implemented:

```python
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class EncryptedJSONStorage:
    """Encrypted JSON storage backend"""
    
    def __init__(self, file_path, password):
        self.file_path = file_path
        # Generate encryption key
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.cipher = Fernet(key)
        self.fibers = {}
        
    def save(self):
        """Encrypt and save data"""
        import json
        data = json.dumps(self.fibers).encode()
        encrypted_data = self.cipher.encrypt(data)
        with open(self.file_path, 'wb') as f:
            f.write(encrypted_data)
            
    def load(self):
        """Load and decrypt data"""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'rb') as f:
                encrypted_data = f.read()
            data = self.cipher.decrypt(encrypted_data)
            import json
            self.fibers = json.loads(data.decode())
```

## Best Practices Summary

1. **Choose the appropriate storage backend**: Select memory or SQLite storage based on expected scale and persistence needs.

2. **Regular maintenance**: For long-term used trees, periodically prune low-frequency nodes to avoid performance impacts due to tree size.

3. **Batch processing**: Use batch mode when adding many paths to reduce update overhead.

4. **Cache optimization**: Adjust cache size based on application characteristics.

5. **Structure monitoring**: Regularly analyze tree structure to detect abnormal growth or imbalances.

6. **Data backup**: Regularly export important decision trees for backup.

7. **Combined strategies**: Consider combining tree decisions with other methods (like machine learning, rule systems) to improve decision quality.

8. **Domain customization**: Customize Move classes and evaluation functions for specific application scenarios. 