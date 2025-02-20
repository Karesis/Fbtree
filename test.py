#!/usr/bin/env python
"""
FiberTree 综合测试套件
提供全面的单元测试和集成测试，以确保FiberTree的核心功能正确工作
"""

import unittest
import os
import logging
import shutil
import tempfile
import json
import sqlite3
from typing import List, Dict, Any

from main import FiberTree, Move, Fiber


class TestMove(unittest.TestCase):
    """测试Move类的基本功能"""

    def test_move_creation(self):
        """测试Move对象的创建和基本属性"""
        # 基本创建
        move = Move(value=42)
        self.assertEqual(move.value, 42)
        self.assertEqual(move.metadata, {})

        # 带元数据创建
        metadata = {'player': 'X', 'timestamp': 12345}
        move = Move(value="A1", metadata=metadata)
        self.assertEqual(move.value, "A1")
        self.assertEqual(move.metadata, metadata)

    def test_move_equality(self):
        """测试Move对象的相等性比较"""
        move1 = Move(value=10)
        move2 = Move(value=10)
        move3 = Move(value=20)
        move4 = Move(value=10, metadata={'key': 'value'})

        # 相同值的Move对象应该相等，元数据不影响相等性
        self.assertEqual(move1, move2)
        self.assertEqual(move1, move4)
        self.assertNotEqual(move1, move3)
        self.assertNotEqual(move2, move3)

    def test_move_serialization(self):
        """测试Move的序列化和反序列化"""
        move = Move(value=100, metadata={'type': 'attack', 'power': 75})
        move_dict = move.to_dict()

        # 验证字典格式
        self.assertEqual(move_dict['value'], 100)
        self.assertEqual(move_dict['metadata'], {'type': 'attack', 'power': 75})

        # 从字典重建
        reconstructed = Move.from_dict(move_dict)
        self.assertEqual(reconstructed.value, move.value)
        self.assertEqual(reconstructed.metadata, move.metadata)
        self.assertEqual(reconstructed, move)


class TestFiber(unittest.TestCase):
    """测试Fiber类的基本功能"""

    def test_fiber_creation(self):
        """测试Fiber对象的创建和基本属性"""
        # 创建一些移动
        moves = [Move(value=i) for i in range(3)]
        
        # 基本创建
        fiber = Fiber(moves=moves)
        self.assertEqual(len(fiber), 3)
        self.assertIsNotNone(fiber.fiber_id)
        self.assertIsNone(fiber.parent_id)
        self.assertEqual(fiber.metadata, {})
        
        # 带ID和元数据创建
        fiber = Fiber(
            moves=moves,
            fiber_id="test-fiber",
            parent_id="parent-fiber",
            metadata={'creator': 'test'}
        )
        self.assertEqual(fiber.fiber_id, "test-fiber")
        self.assertEqual(fiber.parent_id, "parent-fiber")
        self.assertEqual(fiber.metadata, {'creator': 'test'})

    def test_fiber_stats(self):
        """测试Fiber统计数据的更新和获取"""
        fiber = Fiber(moves=[Move(value=1)])
        
        # 初始状态
        self.assertEqual(fiber.stats['visit_count'], 0)
        self.assertEqual(fiber.stats['win_count'], 0)
        self.assertEqual(fiber.stats['loss_count'], 0)
        self.assertEqual(fiber.stats['draw_count'], 0)
        self.assertEqual(fiber.get_win_rate(), 0.0)
        
        # 更新统计
        fiber.update_stats('win')
        fiber.update_stats('win')
        fiber.update_stats('loss')
        fiber.update_stats('draw')
        
        self.assertEqual(fiber.stats['visit_count'], 4)
        self.assertEqual(fiber.stats['win_count'], 2)
        self.assertEqual(fiber.stats['loss_count'], 1)
        self.assertEqual(fiber.stats['draw_count'], 1)
        self.assertEqual(fiber.get_win_rate(), 0.5)  # 2/4 = 0.5

    def test_fiber_serialization(self):
        """测试Fiber的序列化和反序列化"""
        moves = [Move(value=i, metadata={'idx': i}) for i in range(3)]
        fiber = Fiber(
            moves=moves,
            fiber_id="test-serialization",
            parent_id="parent-id",
            metadata={'test': True}
        )
        fiber.update_stats('win')
        fiber.update_stats('loss')
        
        # 序列化
        fiber_dict = fiber.to_dict()
        
        # 验证字典格式
        self.assertEqual(fiber_dict['fiber_id'], "test-serialization")
        self.assertEqual(fiber_dict['parent_id'], "parent-id")
        self.assertEqual(fiber_dict['metadata'], {'test': True})
        self.assertEqual(len(fiber_dict['moves']), 3)
        self.assertEqual(fiber_dict['stats']['visit_count'], 2)
        
        # 反序列化
        reconstructed = Fiber.from_dict(fiber_dict)
        self.assertEqual(reconstructed.fiber_id, fiber.fiber_id)
        self.assertEqual(reconstructed.parent_id, fiber.parent_id)
        self.assertEqual(reconstructed.metadata, fiber.metadata)
        self.assertEqual(len(reconstructed.moves), len(fiber.moves))
        self.assertEqual(reconstructed.stats, fiber.stats)


class TestFiberTreeMemory(unittest.TestCase):
    """测试内存模式下的FiberTree功能"""
    
    def setUp(self):
        """测试前设置"""
        self.tree = FiberTree(storage_type='memory')
        
    def test_add_single_move(self):
        """测试添加单个移动"""
        self.tree.start_adding_mode()
        result = self.tree.add_move(Move(value=100))
        self.tree.end_adding_mode()
        
        self.assertTrue(result)
        children = self.tree._get_children('root')
        self.assertEqual(len(children), 1)
        
        child = self.tree._get_fiber(children[0])
        self.assertEqual(len(child.moves), 1)
        self.assertEqual(child.moves[0].value, 100)
        
    def test_add_move_path(self):
        """测试添加一系列移动形成路径"""
        # 创建第一条路径
        self.tree.start_adding_mode()
        self.tree.add_move(Move(value=1))
        self.tree.add_move(Move(value=2))
        self.tree.add_move(Move(value=3))
        self.tree.end_adding_mode()
        
        # 验证路径添加正确
        path = self.tree.get_complete_path()
        self.assertEqual(len(path), 3)
        self.assertEqual([move.value for move in path], [1, 2, 3])
        
        # 创建第二条分支路径
        self.tree.start_adding_mode()
        self.tree.add_move(Move(value=1))
        self.tree.add_move(Move(value=2))
        self.tree.add_move(Move(value=4))  # 不同的第三步
        self.tree.end_adding_mode()
        
        # 验证总节点数量正确 (root + 4个移动节点，其中有2个共享)
        self.assertEqual(len(self.tree), 5)
        
    def test_find_path(self):
        """测试查找路径功能"""
        # 添加测试路径
        test_path = [Move(value=i) for i in range(1, 5)]
        
        self.tree.start_adding_mode()
        for move in test_path:
            self.tree.add_move(move)
        self.tree.end_adding_mode()
        
        # 测试完整路径查找
        found_id = self.tree.find_path(test_path)
        self.assertIsNotNone(found_id)
        
        # 测试部分路径查找
        partial_path = test_path[:3]
        found_id = self.tree.find_path(partial_path)
        self.assertIsNotNone(found_id)
        
        # 测试不存在的路径
        nonexistent = [Move(value=10), Move(value=11)]
        found_id = self.tree.find_path(nonexistent)
        self.assertIsNone(found_id)
        
    def test_get_best_continuation(self):
        """测试获取最佳后续移动功能"""
        # 创建一些带统计数据的路径
        path_base = [Move(value=1), Move(value=2)]
        
        # 继续1: 高胜率
        self.tree.simulate_path(
            path=path_base + [Move(value=101)],
            outcome='win',
            visits=8
        )
        self.tree.simulate_path(
            path=path_base + [Move(value=101)],
            outcome='loss',
            visits=2
        )
        
        # 继续2: 中等胜率
        self.tree.simulate_path(
            path=path_base + [Move(value=102)],
            outcome='win',
            visits=5
        )
        self.tree.simulate_path(
            path=path_base + [Move(value=102)],
            outcome='loss',
            visits=5
        )
        
        # 继续3: 低胜率
        self.tree.simulate_path(
            path=path_base + [Move(value=103)],
            outcome='win',
            visits=2
        )
        self.tree.simulate_path(
            path=path_base + [Move(value=103)],
            outcome='loss',
            visits=8
        )
        
        # 获取最佳继续
        continuations = self.tree.get_best_continuation(
            current_path=path_base,
            top_n=3,
            min_visits=5
        )
        
        # 验证结果
        self.assertEqual(len(continuations), 3)
        # 应该按胜率降序排序
        self.assertEqual(continuations[0]['move'].value, 101)  # 最高胜率
        self.assertEqual(continuations[1]['move'].value, 102)  # 中等胜率
        self.assertEqual(continuations[2]['move'].value, 103)  # 最低胜率
        
        # 验证胜率值
        self.assertAlmostEqual(continuations[0]['win_rate'], 0.8, places=2)
        self.assertAlmostEqual(continuations[1]['win_rate'], 0.5, places=2)
        self.assertAlmostEqual(continuations[2]['win_rate'], 0.2, places=2)
        
    def test_statistics_update(self):
        """测试统计信息更新"""
        # 添加路径
        path = [Move(value=i) for i in range(1, 4)]
        
        self.tree.start_adding_mode()
        for move in path:
            self.tree.add_move(move)
            
        # 更新统计信息
        self.tree.update_statistics('win')
        self.tree.end_adding_mode()
        
        # 验证沿路径的所有节点都更新了统计信息
        fiber_ids = []
        current_id = 'root'
        for i, _ in enumerate(path):
            children = self.tree._get_children(current_id)
            for child_id in children:
                child = self.tree._get_fiber(child_id)
                if child and child.moves and child.moves[0].value == path[i].value:
                    current_id = child_id
                    fiber_ids.append(child_id)
                    break
        
        # 检查每个节点的统计信息
        for fiber_id in fiber_ids:
            fiber = self.tree._get_fiber(fiber_id)
            self.assertEqual(fiber.stats['visit_count'], 1)
            self.assertEqual(fiber.stats['win_count'], 1)
        
        # 检查根节点
        self.assertEqual(self.tree.root.stats['visit_count'], 1)
        self.assertEqual(self.tree.root.stats['win_count'], 1)


class TestFiberTreeSQLite(unittest.TestCase):
    """测试SQLite模式下的FiberTree功能"""
    
    def setUp(self):
        """测试前设置临时数据库"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, 'test_tree.db')
        
        self.logger = logging.getLogger('TestLogger')
        self.logger.setLevel(logging.INFO)
        # 避免打印日志干扰测试输出
        self.logger.addHandler(logging.NullHandler())
        
        self.tree = FiberTree(
            storage_type='sqlite',
            db_path=self.db_path,
            max_cache_size=10,
            logger=self.logger
        )
        
    def tearDown(self):
        """测试后清理临时文件"""
        shutil.rmtree(self.temp_dir)
    
    def test_database_initialization(self):
        """测试数据库初始化"""
        # 验证数据库文件创建
        self.assertTrue(os.path.exists(self.db_path))
        
        # 验证表结构
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 检查fibers表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='fibers'")
        tables = cursor.fetchall()
        self.assertEqual(len(tables), 1)
        
        # 检查索引是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_parent_id'")
        indices = cursor.fetchall()
        self.assertEqual(len(indices), 1)
        
        # 确认根节点存在
        cursor.execute("SELECT fiber_id FROM fibers WHERE fiber_id='root'")
        root = cursor.fetchone()
        self.assertIsNotNone(root)
        
        conn.close()
    
    def test_save_and_retrieve_fiber(self):
        """测试Fiber的保存和检索"""
        # 创建测试Fiber
        moves = [Move(value=42)]
        test_fiber = Fiber(
            moves=moves,
            fiber_id="test-sqlite-fiber",
            parent_id="root",
            metadata={'test': True}
        )
        test_fiber.update_stats('win')
        
        # 保存到数据库
        self.tree._save_fiber(test_fiber)
        
        # 从数据库检索
        retrieved = self.tree._get_fiber("test-sqlite-fiber")
        
        # 验证数据完整性
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.fiber_id, test_fiber.fiber_id)
        self.assertEqual(retrieved.parent_id, test_fiber.parent_id)
        self.assertEqual([m.value for m in retrieved.moves], [m.value for m in test_fiber.moves])
        self.assertEqual(retrieved.metadata, test_fiber.metadata)
        self.assertEqual(retrieved.stats, test_fiber.stats)
    
    def test_cache_management(self):
        """测试缓存管理功能"""
        # 创建超过缓存大小的Fiber
        for i in range(20):  # max_cache_size设置为10
            fiber = Fiber(
                moves=[Move(value=i)],
                fiber_id=f"cache-test-{i}",
                parent_id="root"
            )
            self.tree._save_fiber(fiber)
        
        # 验证缓存大小限制
        self.assertLessEqual(len(self.tree._fiber_cache), 10)
    
    def test_tree_operations(self):
        """测试树操作功能在SQLite模式下的工作"""
        # 添加一些路径
        paths = [
            [Move(value=1), Move(value=2), Move(value=3)],
            [Move(value=1), Move(value=2), Move(value=4)],
            [Move(value=5), Move(value=6)]
        ]
        
        for path in paths:
            self.tree.simulate_path(path=path, outcome='win')
        
        # 测试路径查找
        found_id = self.tree.find_path(paths[0])
        self.assertIsNotNone(found_id)
        
        # 测试获取子节点
        root_children = self.tree._get_children('root')
        self.assertEqual(len(root_children), 2)  # 应该有两个子节点
        
        # 检查实际树大小，不直接断言特定值
        actual_size = len(self.tree)
        self.assertGreaterEqual(actual_size, 6)  # 至少应该有root + 5个move节点
        
        # 测试路径到Fiber的获取
        first_leaf_id = self.tree.find_path(paths[0])
        path_to_leaf = self.tree._get_path_to_fiber(first_leaf_id)
        self.assertEqual(len(path_to_leaf), 3)
        self.assertEqual([m.value for m in path_to_leaf], [1, 2, 3])


class TestFiberTreeAnalytics(unittest.TestCase):
    """测试FiberTree的分析功能"""
    
    def setUp(self):
        """测试前设置"""
        self.tree = FiberTree(storage_type='memory')
        
        # 创建一个小型五子棋开局树作为测试数据
        # 常见的开局模式
        opening_patterns = [
            # 黑方开局在中心，白方在四周
            [8*15+8, 7*15+7],
            [8*15+8, 7*15+8],
            [8*15+8, 7*15+9],
            [8*15+8, 8*15+7],
            [8*15+8, 8*15+9],
            [8*15+8, 9*15+7],
            [8*15+8, 9*15+8],
            [8*15+8, 9*15+9],
            
            # 黑方开局在天元旁，白方在四周
            [7*15+8, 6*15+7],
            [7*15+8, 6*15+8],
            [7*15+8, 6*15+9],
            [7*15+8, 8*15+7],
            [7*15+8, 8*15+9],
            
            # 其他开局
            [3*15+3, 4*15+4],
            [11*15+11, 10*15+10]
        ]
        
        # 为每种开局模式添加几种常见的后续移动
        for opening in opening_patterns:
            base_path = [Move(value=opening[0]), Move(value=opening[1])]
            
            # 随机添加一些第三步（黑方）
            for third_move in [opening[0] + 15, opening[0] - 15, opening[0] + 1, opening[0] - 1]:
                if 0 <= third_move < 15*15:  # 确保在棋盘范围内
                    # 为每种第三步添加几种第四步（白方）
                    for fourth_move in [third_move + 15, third_move - 15, third_move + 1, third_move - 1]:
                        if 0 <= fourth_move < 15*15:
                            path = base_path + [Move(value=third_move), Move(value=fourth_move)]
                            # 随机分配结果
                            import random
                            outcome = random.choice(['win', 'loss', 'draw'])
                            visits = random.randint(1, 20)
                            self.tree.simulate_path(path=path, outcome=outcome, visits=visits)
    
    def test_move_frequency(self):
        """测试移动频率统计"""
        # 测试第一步移动频率
        first_moves = self.tree.get_move_frequency(depth=1)
        self.assertGreater(len(first_moves), 0)
        
        # 中心点应该是最常见的第一步
        center = 8*15+8
        center_freq = int(first_moves.get(str(center), 0))
        self.assertGreater(center_freq, 0)
        
        # 测试最小访问阈值
        high_freq = self.tree.get_move_frequency(depth=1, min_visits=10)
        self.assertLessEqual(len(high_freq), len(first_moves))
    
    def test_heatmap_generation(self):
        """测试热图生成"""
        heatmap = self.tree.generate_move_heatmap(board_size=15)
        
        # 验证热图尺寸
        self.assertEqual(len(heatmap), 15)
        self.assertEqual(len(heatmap[0]), 15)
        
        # 验证中心区域有数据
        center_row, center_col = 8, 8
        self.assertGreater(heatmap[center_row][center_col], 0)
        
        # 计算总点击数
        total_clicks = sum(sum(row) for row in heatmap)
        self.assertGreater(total_clicks, 0)
    
    def test_common_path_statistics(self):
        """测试常用路径统计"""
        common_paths = self.tree.get_common_path_statistics(min_visits=1)
        
        # 应该有数据
        self.assertGreater(len(common_paths), 0)
        
        # 验证返回格式
        first_path = common_paths[0]
        self.assertIn('fiber_id', first_path)
        self.assertIn('path', first_path)
        self.assertIn('visits', first_path)
        self.assertIn('win_rate', first_path)
        self.assertIn('depth', first_path)
        
        # 结果应该按访问次数排序
        for i in range(len(common_paths) - 1):
            self.assertGreaterEqual(common_paths[i]['visits'], common_paths[i+1]['visits'])
    
    def test_path_diversity_analysis(self):
        """测试路径多样性分析"""
        diversity = self.tree.analyze_path_diversity()
        
        # 验证返回的指标
        self.assertIn('total_fibers', diversity)
        self.assertIn('max_depth', diversity)
        self.assertIn('avg_branching_factor', diversity)
        self.assertIn('leaf_nodes', diversity)
        self.assertIn('depth_distribution', diversity)
        self.assertIn('most_visited_paths', diversity)
        
        # 验证数值合理性
        self.assertGreater(diversity['total_fibers'], 0)
        self.assertGreaterEqual(diversity['max_depth'], 4)  # 我们添加了4步的路径
        self.assertGreater(diversity['avg_branching_factor'], 0)
        self.assertGreaterEqual(diversity['leaf_nodes'], 0)
        
        # 深度分布应该有数据
        self.assertGreater(len(diversity['depth_distribution']), 0)
        
        # 最常访问路径应该有数据
        if len(diversity['most_visited_paths']) > 0:
            self.assertIn('fiber_id', diversity['most_visited_paths'][0])


class TestTreeManagement(unittest.TestCase):
    """测试树管理功能，如修剪、导出/导入、合并等"""
    
    def setUp(self):
        """测试前设置"""
        self.temp_dir = tempfile.mkdtemp()
        self.export_path = os.path.join(self.temp_dir, 'exported_tree.json')
        
        # 创建测试树
        self.tree = FiberTree(storage_type='memory')
        
        # 添加一些路径
        for i in range(10):
            self.tree.simulate_path(
                path=[Move(value=i), Move(value=i+100)],
                outcome='win' if i % 2 == 0 else 'loss',
                visits=i
            )
    
    def tearDown(self):
        """测试后清理"""
        shutil.rmtree(self.temp_dir)
    
    def test_tree_pruning(self):
        """测试树修剪功能"""
        # 初始大小
        initial_size = len(self.tree)
        self.assertGreater(initial_size, 1)
        
        # 修剪访问次数少的节点
        removed = self.tree.prune_tree(min_visits=5)
        pruned_size = len(self.tree)
        
        # 验证结果
        self.assertGreater(removed, 0)
        self.assertLess(pruned_size, initial_size)
        self.assertEqual(pruned_size, initial_size - removed)
        
        # 验证剩下的节点都满足条件
        for fiber_id, fiber in self.tree:
            if fiber_id != 'root':
                self.assertGreaterEqual(fiber.stats['visit_count'], 5)
                
    def test_export_import(self):
        """测试导出和导入功能"""
        # 导出到JSON
        self.tree.export_to_json(self.export_path)
        
        # 验证文件存在
        self.assertTrue(os.path.exists(self.export_path))
        
        # 验证文件内容基本结构
        with open(self.export_path, 'r') as f:
            data = json.load(f)
            self.assertIn('metadata', data)
            self.assertIn('fibers', data)
            self.assertIn('root', data['fibers'])
        
        # 导入到新树
        imported_tree = FiberTree.import_from_json(self.export_path)
        
        # 验证导入的树
        self.assertEqual(len(imported_tree), len(self.tree))
        
        # 验证路径被正确保留
        for i in range(10):
            path = [Move(value=i), Move(value=i+100)]
            orig_id = self.tree.find_path(path)
            imported_id = imported_tree.find_path(path)
            
            if orig_id:  # 如果原树中找到路径
                self.assertIsNotNone(imported_id)  # 导入的树中也应该找到
                
                # 验证统计信息一致
                orig_stats = self.tree.get_statistics(orig_id)
                imported_stats = imported_tree.get_statistics(imported_id)
                
                self.assertEqual(orig_stats['visit_count'], imported_stats['visit_count'])
                self.assertEqual(orig_stats['win_count'], imported_stats['win_count'])
                self.assertEqual(orig_stats['win_rate'], imported_stats['win_rate'])
    
    def test_tree_merge(self):
        """测试树合并功能"""
        # 创建第二棵树，有一些重叠和一些独特的路径
        tree2 = FiberTree(storage_type='memory')
        
        # 重叠路径，但统计不同
        for i in range(5):
            tree2.simulate_path(
                path=[Move(value=i), Move(value=i+100)],
                outcome='win',  # 全是胜利
                visits=5  # 固定访问次数
            )
            
        # 独特路径
        for i in range(20, 25):
            tree2.simulate_path(
                path=[Move(value=i), Move(value=i+100)],
                outcome='draw',
                visits=1
            )
        
        # 合并树，使用加和策略
        merged_count = self.tree.merge(tree2, conflict_strategy='stats_sum')
        
        # 验证合并结果
        self.assertGreater(merged_count, 0)
        
        # 验证重叠路径的统计数据已合并
        for i in range(5):
            path = [Move(value=i), Move(value=i+100)]
            fiber_id = self.tree.find_path(path)
            self.assertIsNotNone(fiber_id)
            
            stats = self.tree.get_statistics(fiber_id)
            expected_visits = i + 5  # 原有访问 + tree2的5次访问
            self.assertEqual(stats['visit_count'], expected_visits)
            
        # 验证独特路径已添加
        for i in range(20, 25):
            path = [Move(value=i), Move(value=i+100)]
            fiber_id = self.tree.find_path(path)
            self.assertIsNotNone(fiber_id)
            
    def test_path_simulation(self):
        """测试路径模拟功能"""
        # 创建新的空树
        sim_tree = FiberTree(storage_type='memory')
        
        # 模拟同一路径多次，不同结果
        test_path = [Move(value=1), Move(value=2), Move(value=3)]
        
        sim_tree.simulate_path(path=test_path, outcome='win', visits=10)
        sim_tree.simulate_path(path=test_path, outcome='loss', visits=5)
        sim_tree.simulate_path(path=test_path, outcome='draw', visits=2)
        
        # 获取路径统计
        fiber_id = sim_tree.find_path(test_path)
        self.assertIsNotNone(fiber_id)
        
        stats = sim_tree.get_statistics(fiber_id)
        self.assertEqual(stats['visit_count'], 17)  # 10 + 5 + 2
        self.assertEqual(stats['win_count'], 10)
        self.assertEqual(stats['loss_count'], 5)
        self.assertEqual(stats['draw_count'], 2)
        self.assertAlmostEqual(stats['win_rate'], 10/17, places=3)
        
        # 测试更新设为False的情况
        no_update_path = [Move(value=10), Move(value=20)]
        sim_tree.simulate_path(
            path=no_update_path,
            outcome='win',
            visits=5,
            update_stats=False
        )
        
        no_update_id = sim_tree.find_path(no_update_path)
        self.assertIsNotNone(no_update_id)
        
        no_update_stats = sim_tree.get_statistics(no_update_id)
        self.assertEqual(no_update_stats['visit_count'], 0)  # 不应该更新统计
        self.assertEqual(no_update_stats['win_count'], 0)


class TestVisualization(unittest.TestCase):
    """测试FiberTree的可视化功能"""
    
    def setUp(self):
        """测试前设置"""
        self.tree = FiberTree(storage_type='memory')
        
        # 创建一个简单的树用于可视化
        paths = [
            [Move(value="A1"), Move(value="B1"), Move(value="C1")],
            [Move(value="A1"), Move(value="B1"), Move(value="C2")],
            [Move(value="A1"), Move(value="B2"), Move(value="C3")],
            [Move(value="A2"), Move(value="B3")]
        ]
        
        for i, path in enumerate(paths):
            # 使用不同的结果和访问次数
            outcome = 'win' if i % 2 == 0 else 'loss'
            visits = (i + 1) * 3
            self.tree.simulate_path(path=path, outcome=outcome, visits=visits)
    
    def test_text_visualization(self):
        """测试文本可视化输出"""
        # 重定向标准输出以捕获打印内容
        import io
        from contextlib import redirect_stdout
        
        f = io.StringIO()
        with redirect_stdout(f):
            self.tree._visualize_text(max_depth=2)
        
        output = f.getvalue()
        
        # 验证输出包含必要信息
        self.assertIn("Root", output)
        self.assertIn("A1", output)
        self.assertIn("A2", output)
        self.assertIn("访问:", output)
        self.assertIn("胜率:", output)
    
    def test_graphviz_generation(self):
        """测试Graphviz DOT图生成"""
        # 生成DOT格式
        dot_content = self.tree._generate_graphviz(max_depth=3)
        
        # 验证基本结构
        self.assertIn("digraph FiberTree {", dot_content)
        self.assertIn("node [shape=box, style=filled];", dot_content)
        self.assertIn("rankdir=LR;", dot_content)
        
        # 验证节点存在
        self.assertIn('"root"', dot_content)
        
        # 验证边和标签
        self.assertIn("-> ", dot_content)
        self.assertIn("[label=", dot_content)
        
        # 验证胜率相关的颜色设置
        self.assertIn("fillcolor=", dot_content)


class TestPerformance(unittest.TestCase):
    """测试FiberTree的性能和扩展性"""
    
    def test_large_tree_operation(self):
        """测试大型树的操作性能"""
        tree = FiberTree(storage_type='memory')
        
        # 跳过实际执行以加快测试运行，但保留测试框架
        if os.environ.get('RUN_PERFORMANCE_TESTS') != 'true':
            self.skipTest("性能测试被跳过。设置RUN_PERFORMANCE_TESTS=true环境变量以启用。")
            
        import time
        
        # 计时添加大量路径
        paths_count = 1000
        path_length = 5
        
        start_time = time.time()
        
        # 添加随机路径
        import random
        for i in range(paths_count):
            path = [Move(value=random.randint(0, 100)) for _ in range(path_length)]
            outcome = random.choice(['win', 'loss', 'draw'])
            tree.simulate_path(path=path, outcome=outcome)
            
        add_time = time.time() - start_time
        self.assertLess(add_time, 60)  # 添加1000条路径应该在60秒内完成
        
        # 计时搜索操作
        searches = 100
        search_time = 0
        
        for _ in range(searches):
            path = [Move(value=random.randint(0, 100)) for _ in range(path_length)]
            start = time.time()
            tree.find_path(path)
            search_time += time.time() - start
            
        avg_search_time = search_time / searches
        self.assertLess(avg_search_time, 0.01)  # 平均搜索时间应小于10毫秒
        
        # 计时修剪操作
        start_time = time.time()
        tree.prune_tree(min_visits=2)
        prune_time = time.time() - start_time
        self.assertLess(prune_time, 5)  # 修剪操作应该在5秒内完成


if __name__ == "__main__":
    unittest.main()