# FiberTree 高级主题

本文档涵盖FiberTree的高级用法、优化策略和定制方法。

## 性能优化

### 存储后端选择

FiberTree提供两种存储后端：内存存储和SQLite存储。

- **内存存储**：适用于较小的树和需要最高性能的场景。所有数据保存在内存中，程序结束时数据会丢失（除非手动导出）。

- **SQLite存储**：适用于大型树和需要持久化的场景。数据保存在SQLite数据库文件中，提供更好的可扩展性和持久性。

选择标准：
- 树节点预计少于10,000个：可以使用内存存储
- 树节点预计超过10,000个：推荐使用SQLite存储
- 需要会话间持久化：使用SQLite存储

示例：
```python
# 创建大型持久化树
tree = create_tree(
    storage_type='sqlite',
    db_path='large_tree.db',
    cache_size=1000  # 调整缓存大小
)
```

### 缓存优化

FiberTree内部使用LRU缓存来提高频繁访问节点的性能。您可以调整缓存大小以平衡内存使用和性能：

```python
# 为内存密集型应用设置较小的缓存
tree = create_tree(storage_type='memory', cache_size=100)

# 为性能敏感型应用设置较大的缓存
tree = create_tree(storage_type='sqlite', cache_size=5000)
```

### 批量操作

对于需要添加大量路径的场景，可以使用批量操作提高性能：

```python
# 启用批量模式
tree.start_batch_mode()

# 添加多条路径
for path, outcome in paths_data:
    tree.simulate_path(path, outcome, update_stats=False)  # 不立即更新统计信息

# 完成批量添加，一次性更新统计信息
tree.end_batch_mode()
```

### 树修剪策略

定期修剪树可以减少存储空间并提高性能：

```python
# 基本修剪 - 移除访问次数低于阈值的节点
tree.prune_tree(min_visits=5)

# 高级修剪 - 同时考虑访问次数和深度
def custom_prune_condition(fiber, depth):
    """自定义修剪条件"""
    # 深度越深，要求的访问次数越高
    min_visits = depth * 2
    return fiber.stats['visit_count'] < min_visits

tree.prune_tree(custom_condition=custom_prune_condition)
```

## 高级分析功能

### 路径多样性分析

分析决策树的结构特征：

```python
diversity = tree.analyze_path_diversity()

print(f"总节点数: {diversity['total_fibers']}")
print(f"最大深度: {diversity['max_depth']}")
print(f"平均分支因子: {diversity['avg_branching_factor']:.2f}")
print(f"叶节点比例: {diversity['leaf_nodes'] / diversity['total_fibers']:.2f}")

# 分析深度分布
for depth, count in diversity['depth_distribution'].items():
    print(f"深度 {depth}: {count} 个节点")

# 查看最常访问路径
for path in diversity['most_visited_paths'][:5]:
    print(f"ID: {path['fiber_id']}, 访问: {path['visits']}")
```

### 决策路径比较

比较不同路径的表现：

```python
# 比较两个开局策略
path1 = [Move("中心开局"), Move("侧翼防守")]
path2 = [Move("侧翼开局"), Move("中心进攻")]

stats1 = tree.get_path_statistics(path1)
stats2 = tree.get_path_statistics(path2)

print(f"策略1 - 访问: {stats1['visit_count']}, 胜率: {stats1['win_rate']:.2f}")
print(f"策略2 - 访问: {stats2['visit_count']}, 胜率: {stats2['win_rate']:.2f}")

# 分析后续发展
cont1 = tree.get_best_continuation(path1, top_n=3)
cont2 = tree.get_best_continuation(path2, top_n=3)

print("策略1后续最佳动作:")
for move in cont1:
    print(f"  {move['move']} - 胜率: {move['win_rate']:.2f}")

print("策略2后续最佳动作:")
for move in cont2:
    print(f"  {move['move']} - 胜率: {move['win_rate']:.2f}")
```

### 动态评估

根据上下文调整评估标准：

```python
def dynamic_evaluation(move_stats, context):
    """根据上下文动态调整动作评估"""
    base_score = move_stats['win_rate']
    
    # 例：在资源紧张时更看重低风险动作
    if context.get('resources') == 'low':
        uncertainty = move_stats['visits'] / (move_stats['visits'] + 50)
        return base_score * (1 - uncertainty * 0.5)
    
    # 例：落后时更看重高收益动作
    if context.get('score_difference') < 0:
        return base_score * 1.2  # 提高权重
    
    return base_score

# 使用
context = {'resources': 'low', 'score_difference': -10}
best_moves = tree.get_best_continuation(path)

# 应用动态评估
evaluated_moves = [
    {**move, 'adjusted_score': dynamic_evaluation(move, context)}
    for move in best_moves
]

# 按调整后的分数排序
evaluated_moves.sort(key=lambda x: x['adjusted_score'], reverse=True)
```

## 扩展与定制

### 创建自定义存储后端

您可以通过实现存储接口创建自定义存储后端：

```python
from fbtree.storage.base import StorageBase

class CustomStorage(StorageBase):
    """自定义存储后端示例"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 初始化您的存储
        
    def get_fiber(self, fiber_id):
        # 实现获取节点
        pass
        
    def save_fiber(self, fiber_id, fiber):
        # 实现保存节点
        pass
        
    def remove_fiber(self, fiber_id):
        # 实现删除节点
        pass
        
    def get_all_fibers(self):
        # 实现获取所有节点
        pass
        
    # 实现其他必要的方法...

# 使用自定义存储
from fbtree import FiberTree
tree = FiberTree(storage=CustomStorage(**custom_params))
```

### 扩展移动类型

创建自定义Move类来处理特定领域的动作：

```python
from fbtree import Move

class ChessMove(Move):
    """国际象棋移动类"""
    
    def __init__(self, from_pos, to_pos, piece_type, is_capture=False):
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.piece_type = piece_type
        self.is_capture = is_capture
        # 序列化为值
        value = f"{from_pos}-{to_pos}-{piece_type}"
        if is_capture:
            value += "-capture"
        super().__init__(value=value)
    
    def __str__(self):
        """字符串表示"""
        capture = "x" if self.is_capture else "-"
        return f"{self.piece_type}{self.from_pos}{capture}{self.to_pos}"
        
# 使用
knight_move = ChessMove("e4", "f6", "N", is_capture=True)
tree.add_move(knight_move)
```

### 集成机器学习模型

将FiberTree与机器学习模型集成，以优化决策：

```python
import numpy as np
from sklearn.ensemble import RandomForestClassifier

class MLEnhancedTree:
    """结合机器学习的增强决策树"""
    
    def __init__(self, tree, feature_extractor):
        self.tree = tree
        self.feature_extractor = feature_extractor
        self.model = RandomForestClassifier()
        self.trained = False
        
    def train(self):
        """训练模型"""
        X = []
        y = []
        
        # 从树中收集训练数据
        for fiber_id, fiber in self.tree:
            if fiber.stats['visit_count'] > 10:  # 只使用有足够数据的节点
                path = self.tree._get_path_to_fiber(fiber_id)
                features = self.feature_extractor(path)
                X.append(features)
                y.append(fiber.stats['win_rate'])
        
        if len(X) > 0:
            self.model.fit(np.array(X), np.array(y))
            self.trained = True
            
    def predict_best_move(self, current_path):
        """预测最佳后续动作"""
        # 先从树获取候选动作
        candidates = self.tree.get_best_continuation(current_path, top_n=10)
        
        if not self.trained or not candidates:
            return candidates
            
        # 为每个候选动作预测胜率
        for i, move_info in enumerate(candidates):
            new_path = current_path + [move_info['move']]
            features = self.feature_extractor(new_path)
            predicted_win_rate = self.model.predict([features])[0]
            
            # 结合树统计和模型预测
            tree_confidence = min(1.0, move_info['visits'] / 50)
            candidates[i]['predicted_win_rate'] = (
                tree_confidence * move_info['win_rate'] + 
                (1 - tree_confidence) * predicted_win_rate
            )
            
        # 按预测胜率排序
        candidates.sort(key=lambda x: x['predicted_win_rate'], reverse=True)
        return candidates
```

## 分布式和并行处理

对于需要处理大规模数据的应用，可以实现分布式FiberTree：

```python
# 伪代码示例
class DistributedFiberTree:
    """分布式FiberTree实现"""
    
    def __init__(self, worker_count, central_db_uri):
        self.worker_count = worker_count
        self.central_db_uri = central_db_uri
        self.worker_trees = []
        
    def initialize_workers(self):
        """初始化工作节点"""
        for i in range(self.worker_count):
            # 为每个工作节点创建本地树
            worker_tree = create_tree(
                storage_type='sqlite',
                db_path=f'worker_{i}.db'
            )
            self.worker_trees.append(worker_tree)
            
    def simulate_batch(self, paths_batch):
        """并行模拟一批路径"""
        # 分配任务给工作节点
        tasks = [[] for _ in range(self.worker_count)]
        for i, path_data in enumerate(paths_batch):
            worker_idx = i % self.worker_count
            tasks[worker_idx].append(path_data)
            
        # 并行执行 (使用多进程或线程)
        import concurrent.futures
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = []
            for worker_idx, task in enumerate(tasks):
                futures.append(
                    executor.submit(self._worker_simulate, worker_idx, task)
                )
            concurrent.futures.wait(futures)
            
    def _worker_simulate(self, worker_idx, paths):
        """工作节点处理函数"""
        worker_tree = self.worker_trees[worker_idx]
        for path, outcome in paths:
            worker_tree.simulate_path(path, outcome)
            
    def synchronize(self):
        """同步所有工作节点数据到中央数据库"""
        central_tree = create_tree(
            storage_type='sqlite',
            db_path=self.central_db_uri
        )
        
        # 合并所有工作节点的树
        for worker_tree in self.worker_trees:
            central_tree.merge(worker_tree, conflict_strategy='stats_sum')
            
        return central_tree
```

## 安全与加密

对于处理敏感决策数据的应用，可以实现加密存储：

```python
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class EncryptedJSONStorage:
    """加密JSON存储后端"""
    
    def __init__(self, file_path, password):
        self.file_path = file_path
        # 生成加密密钥
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
        """加密保存数据"""
        import json
        data = json.dumps(self.fibers).encode()
        encrypted_data = self.cipher.encrypt(data)
        with open(self.file_path, 'wb') as f:
            f.write(encrypted_data)
            
    def load(self):
        """加密加载数据"""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'rb') as f:
                encrypted_data = f.read()
            data = self.cipher.decrypt(encrypted_data)
            import json
            self.fibers = json.loads(data.decode())
```

## 最佳实践总结

1. **合理选择存储后端**：根据预期规模和持久化需求选择内存或SQLite存储。

2. **定期维护**：对于长期使用的树，定期修剪低频节点，避免树过大影响性能。

3. **批量处理**：添加大量路径时使用批量模式，减少更新开销。

4. **缓存优化**：根据应用特性调整缓存大小。

5. **结构监控**：定期分析树结构，检测异常增长或不平衡。

6. **数据备份**：对重要决策树定期导出备份。

7. **组合策略**：考虑将树决策与其他方法（如机器学习、规则系统）结合，提高决策质量。

8. **领域定制**：针对特定应用场景定制Move类和评估函数。 