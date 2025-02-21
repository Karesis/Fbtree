"""
五子棋AI实现 - 使用FiberTree数据库进行决策路径优化
"""

import numpy as np
from fbtree import FiberTree, Move
import random
from typing import List, Tuple, Optional
import time

class GomokuState:
    """五子棋状态表示"""
    
    def __init__(self, size=15):
        self.size = size
        # 0表示空, 1表示黑棋, 2表示白棋
        self.board = np.zeros((size, size), dtype=np.int8)
        self.current_player = 1  # 黑棋先行
        self.last_move = None
        self.moves_count = 0
    
    def copy(self):
        """创建状态的深拷贝"""
        new_state = GomokuState(self.size)
        new_state.board = self.board.copy()
        new_state.current_player = self.current_player
        new_state.last_move = self.last_move
        new_state.moves_count = self.moves_count
        return new_state
    
    def make_move(self, x: int, y: int) -> bool:
        """
        尝试在(x,y)位置落子
        
        Returns:
            bool: 移动是否有效
        """
        if not (0 <= x < self.size and 0 <= y < self.size):
            return False
        
        if self.board[x, y] != 0:
            return False
        
        self.board[x, y] = self.current_player
        self.last_move = (x, y)
        self.moves_count += 1
        self.current_player = 3 - self.current_player  # 切换玩家 (1->2, 2->1)
        return True
    
    def get_valid_moves(self) -> List[Tuple[int, int]]:
        """获取所有有效移动"""
        # 只考虑已有棋子周围的空位
        if self.moves_count == 0:
            # 第一步: 返回棋盘中心及周围点
            center = self.size // 2
            return [(center, center)]
        
        moves = set()
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x, y] != 0:  # 有棋子的位置
                    # 检查周围3x3范围内的空位
                    for dx in range(-2, 3):
                        for dy in range(-2, 3):
                            nx, ny = x + dx, y + dy
                            if (0 <= nx < self.size and 0 <= ny < self.size and 
                                self.board[nx, ny] == 0):
                                moves.add((nx, ny))
        
        return list(moves)
    
    def is_terminal(self) -> Tuple[bool, Optional[int]]:
        """
        检查游戏是否结束
        
        Returns:
            Tuple[bool, Optional[int]]: (是否结束, 赢家(1或2)或None表示平局)
        """
        if self.last_move is None:
            return False, None
        
        x, y = self.last_move
        player = self.board[x, y]
        
        # 检查四个方向: 水平, 垂直, 两个对角线
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        
        for dx, dy in directions:
            count = 1  # 当前方向连子数
            
            # 正向检查
            tx, ty = x + dx, y + dy
            while 0 <= tx < self.size and 0 <= ty < self.size and self.board[tx, ty] == player:
                count += 1
                tx, ty = tx + dx, ty + dy
            
            # 反向检查
            tx, ty = x - dx, y - dy
            while 0 <= tx < self.size and 0 <= ty < self.size and self.board[tx, ty] == player:
                count += 1
                tx, ty = tx - dx, ty - dy
            
            # 判断是否连成5子或更多
            if count >= 5:
                return True, player
        
        # 检查是否平局 (棋盘已满)
        if np.all(self.board != 0):
            return True, None
        
        return False, None
    
    def evaluate(self) -> float:
        """
        评估当前状态对AI(玩家2)的有利程度
        
        Returns:
            float: 评分越高对AI越有利
        """
        terminal, winner = self.is_terminal()
        
        if terminal:
            if winner == 2:  # AI赢
                return 1000
            elif winner == 1:  # 玩家赢
                return -1000
            else:  # 平局
                return 0
        
        # 非终局状态: 分析连子情况
        score = 0
        player_scores = {1: 0, 2: 0}  # 玩家1和玩家2的评分
        
        # 检查四个方向上的连子情况
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        
        for player in [1, 2]:
            for x in range(self.size):
                for y in range(self.size):
                    if self.board[x, y] != player:
                        continue
                    
                    for dx, dy in directions:
                        # 计算连子
                        line_score = self._evaluate_line(x, y, dx, dy, player)
                        player_scores[player] += line_score
        
        # AI评分减去玩家评分
        score = player_scores[2] - player_scores[1]
        return score
    
    def _evaluate_line(self, x: int, y: int, dx: int, dy: int, player: int) -> float:
        """评估一条线上的连子情况"""
        consecutive = 1  # 连续棋子数
        blocked_ends = 0  # 被阻挡的端点数
        
        # 正向检查
        tx, ty = x + dx, y + dy
        while 0 <= tx < self.size and 0 <= ty < self.size:
            if self.board[tx, ty] == player:
                consecutive += 1
            elif self.board[tx, ty] == 0:
                break
            else:
                blocked_ends += 1
                break
            tx, ty = tx + dx, ty + dy
        
        # 负向检查
        tx, ty = x - dx, y - dy
        while 0 <= tx < self.size and 0 <= ty < self.size:
            if self.board[tx, ty] == player:
                consecutive += 1
            elif self.board[tx, ty] == 0:
                break
            else:
                blocked_ends += 1
                break
            tx, ty = tx - dx, ty - dy
        
        # 根据连子数和阻挡情况评分
        if consecutive >= 5:
            return 100  # 五连珠
        elif consecutive == 4:
            if blocked_ends == 0:
                return 90  # 活四
            else:
                return 50  # 冲四
        elif consecutive == 3:
            if blocked_ends == 0:
                return 40  # 活三
            else:
                return 10  # 眠三
        elif consecutive == 2:
            if blocked_ends == 0:
                return 5   # 活二
            else:
                return 2   # 眠二
        
        return 0

class GomokuAI:
    """五子棋AI，使用FiberTree存储和优化决策路径"""
    
    def __init__(self, tree_path=None, storage_type='memory'):
        """
        初始化五子棋AI
        
        Args:
            tree_path: FiberTree存储路径
            storage_type: 'memory'或'sqlite'
        """
        if tree_path:
            self.tree = FiberTree(storage_type=storage_type, db_path=tree_path)
        else:
            self.tree = FiberTree(storage_type=storage_type)
        
        self.max_depth = 3  # MCTS搜索深度
        self.simulation_count = 100  # 每次决策的模拟次数
        self.exploration_weight = 1.0  # UCB探索权重
        self.time_limit = 5  # 每步思考时间限制(秒)
    
    def serialize_move(self, x: int, y: int) -> int:
        """将(x,y)坐标序列化为一个整数值"""
        # 例如在15*15棋盘上，将(x,y)映射为x*15+y
        return x * 15 + y
    
    def deserialize_move(self, value: int) -> Tuple[int, int]:
        """将整数值反序列化为(x,y)坐标"""
        x = value // 15
        y = value % 15
        return x, y
    
    def get_move(self, state: GomokuState) -> Tuple[int, int]:
        """
        基于当前状态选择最佳移动
        
        Args:
            state: 当前游戏状态
            
        Returns:
            Tuple[int, int]: 最佳移动的(x,y)坐标
        """
        # 如果是第一步，直接下中心点
        if state.moves_count == 0:
            return state.size // 2, state.size // 2
        
        # 获取有效移动
        valid_moves = state.get_valid_moves()
        if not valid_moves:
            return -1, -1  # 没有合法移动
        
        # 快速评估: 检查是否有能立即获胜的移动
        for x, y in valid_moves:
            next_state = state.copy()
            next_state.make_move(x, y)
            terminal, winner = next_state.is_terminal()
            if terminal and winner == 2:  # AI获胜
                return x, y
        
        # 时间限制内执行尽可能多的模拟
        start_time = time.time()
        simulation_count = 0
        
        # 准备当前路径
        current_path = []
        for x in range(state.size):
            for y in range(state.size):
                if state.board[x, y] != 0:
                    move_value = self.serialize_move(x, y)
                    current_path.append(Move(move_value))
        
        # 开始记录新路径
        self.tree.start_path()
        for move in current_path:
            self.tree.add_move(move)
        
        # 尝试从树中获取最佳后续移动
        best_continuations = self.tree.get_best_continuation(current_path, top_n=3, min_visits=10)
        
        # 如果有足够的数据，根据树的统计选择最佳移动
        if best_continuations:
            # 按胜率和访问次数选择最佳移动
            best_continuation = max(best_continuations, 
                                   key=lambda x: (x['win_rate'], x['visits']))
            best_move = best_continuation['move'].value
            self.tree.end_path()
            return self.deserialize_move(best_move)
        
        # 如果没有足够的历史数据，使用MCTS搜索
        while time.time() - start_time < self.time_limit:
            # 评估每个移动
            move_scores = []
            for x, y in valid_moves:
                next_state = state.copy()
                next_state.make_move(x, y)
                
                # 运行一次迷你Max搜索
                score = self._minimax(next_state, depth=self.max_depth, alpha=float('-inf'), 
                                    beta=float('inf'), maximizing=False)
                move_scores.append((x, y, score))
                
                simulation_count += 1
            
            # 选择得分最高的前N个移动
            top_moves = sorted(move_scores, key=lambda x: x[2], reverse=True)[:3]
            
            # 为每个选中的移动进行模拟并记录到树中
            for x, y, score in top_moves:
                move_value = self.serialize_move(x, y)
                
                # 模拟这个移动
                sim_state = state.copy()
                sim_state.make_move(x, y)
                terminal, winner = sim_state.is_terminal()
                
                # 如果是终局状态
                if terminal:
                    outcome = 'win' if winner == 2 else ('draw' if winner is None else 'loss')
                    
                    # 将这个移动添加到路径并记录结果
                    self.tree.add_move(Move(move_value))
                    self.tree.record_outcome(outcome)
                    self.tree.start_path()  # 重置到当前路径
                    
                    for move in current_path:
                        self.tree.add_move(move)
                else:
                    # 否则运行一个快速的随机模拟
                    outcome = self._random_playout(sim_state)
                    
                    # 记录结果
                    self.tree.add_move(Move(move_value))
                    self.tree.record_outcome(outcome)
                    self.tree.start_path()  # 重置到当前路径
                    
                    for move in current_path:
                        self.tree.add_move(move)
        
        # 根据树的统计选择最佳移动
        best_continuations = self.tree.get_best_continuation(current_path, top_n=5)
        
        if best_continuations:
            # 按胜率和访问次数选择最佳移动
            best_continuation = max(best_continuations, 
                                   key=lambda x: (x['win_rate'], x['visits']))
            best_move = best_continuation['move'].value
            self.tree.end_path()
            return self.deserialize_move(best_move)
        
        # 如果树中没有足够数据，返回评分最高的移动
        sorted_moves = sorted(move_scores, key=lambda x: x[2], reverse=True)
        self.tree.end_path()
        return sorted_moves[0][0], sorted_moves[0][1]
    
    def _minimax(self, state: GomokuState, depth: int, alpha: float, beta: float, 
                maximizing: bool) -> float:
        """
        使用Alpha-Beta剪枝的Minimax搜索
        
        Args:
            state: 当前游戏状态
            depth: 剩余搜索深度
            alpha, beta: Alpha-Beta剪枝参数
            maximizing: 是否为最大化玩家
            
        Returns:
            float: 状态的评分
        """
        # 检查终局
        terminal, winner = state.is_terminal()
        if terminal:
            if winner == 2:  # AI赢
                return 1000
            elif winner == 1:  # 玩家赢
                return -1000
            else:  # 平局
                return 0
        
        # 达到深度限制
        if depth == 0:
            return state.evaluate()
        
        valid_moves = state.get_valid_moves()
        
        # 限制宽度以提高效率
        if len(valid_moves) > 8:
            # 对每个移动做简单评估
            move_values = []
            for x, y in valid_moves:
                next_state = state.copy()
                next_state.make_move(x, y)
                score = next_state.evaluate()
                move_values.append((x, y, score))
            
            # 根据评分选择前8个移动
            if maximizing:
                valid_moves = [m[:2] for m in sorted(move_values, key=lambda x: x[2], reverse=True)[:8]]
            else:
                valid_moves = [m[:2] for m in sorted(move_values, key=lambda x: x[2])[:8]]
        
        if maximizing:  # AI的回合
            max_eval = float('-inf')
            for x, y in valid_moves:
                next_state = state.copy()
                next_state.make_move(x, y)
                eval = self._minimax(next_state, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:  # 玩家的回合
            min_eval = float('inf')
            for x, y in valid_moves:
                next_state = state.copy()
                next_state.make_move(x, y)
                eval = self._minimax(next_state, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
    
    def _random_playout(self, state: GomokuState) -> str:
        """
        从当前状态随机模拟到游戏结束
        
        Returns:
            str: 游戏结果 ('win', 'loss', 或 'draw')
        """
        sim_state = state.copy()
        depth = 0
        max_depth = 30  # 防止无限循环
        
        while depth < max_depth:
            terminal, winner = sim_state.is_terminal()
            if terminal:
                if winner == 2:  # AI赢
                    return 'win'
                elif winner == 1:  # 玩家赢
                    return 'loss'
                else:  # 平局
                    return 'draw'
            
            # 随机选择一个有效移动
            valid_moves = sim_state.get_valid_moves()
            if not valid_moves:
                return 'draw'
                
            x, y = random.choice(valid_moves)
            sim_state.make_move(x, y)
            depth += 1
        
        # 如果达到最大深度，根据当前状态评估结果
        score = sim_state.evaluate()
        if score > 20:
            return 'win'
        elif score < -20:
            return 'loss'
        else:
            return 'draw'
    
    def learn_from_game(self, moves: List[Tuple[int, int]], outcome: str):
        """
        从完整游戏记录中学习
        
        Args:
            moves: 游戏中的移动列表
            outcome: 游戏结果 ('win', 'loss', 或 'draw')
        """
        # 将移动转换为Move对象
        path = [Move(self.serialize_move(x, y)) for x, y in moves]
        
        # 添加到树中
        self.tree.simulate_path(path, outcome)
    
    def save_knowledge(self, file_path: str):
        """保存AI的知识库"""
        self.tree.export_to_json(file_path)
    
    def load_knowledge(self, file_path: str):
        """加载AI的知识库"""
        self.tree = FiberTree.import_from_json(file_path, self.tree.storage_type, self.tree.db_path)


class GomokuGame:
    """五子棋游戏管理器"""
    
    def __init__(self, size=15):
        self.state = GomokuState(size)
        self.ai = GomokuAI()
        self.game_over = False
        self.winner = None
    
    def player_move(self, x: int, y: int) -> bool:
        """玩家下棋"""
        if self.game_over:
            return False
            
        if self.state.current_player != 1:
            return False
            
        if not self.state.make_move(x, y):
            return False
            
        # 检查游戏是否结束
        self.game_over, self.winner = self.state.is_terminal()
        return True
    
    def ai_move(self) -> Optional[Tuple[int, int]]:
        """AI下棋"""
        if self.game_over or self.state.current_player != 2:
            return None
            
        x, y = self.ai.get_move(self.state)
        
        if not self.state.make_move(x, y):
            return None
            
        # 检查游戏是否结束
        self.game_over, self.winner = self.state.is_terminal()
        return x, y
    
    def reset(self):
        """重置游戏"""
        self.state = GomokuState(self.state.size)
        self.game_over = False
        self.winner = None
    
    def get_board(self) -> np.ndarray:
        """获取当前棋盘状态"""
        return self.state.board.copy()


# 简单的命令行界面示例
def print_board(board):
    """打印棋盘 - 使用更美观、对齐的格式"""
    size = board.shape[0]
    
    # 打印列标题
    print("    ", end="")
    for j in range(size):
        print(f"{j:2d}", end=" ")
    print()
    
    # 打印上边框
    print("   +" + "---" * size + "+")
    
    # 打印棋盘内容
    for i in range(size):
        print(f"{i:2d} |", end=" ")
        for j in range(size):
            if board[i, j] == 0:
                print("·", end="  ")
            elif board[i, j] == 1:
                print("X", end="  ")
            else:
                print("O", end="  ")
        print("|")
    
    # 打印下边框
    print("   +" + "---" * size + "+")


def main():
    """主函数"""
    game = GomokuGame(15)
    
    print("五子棋游戏 - 玩家(X) vs AI(O)")
    print("输入坐标 (x y) 下棋，例如 '7 7'")
    print("输入 'q' 退出")
    
    while not game.game_over:
        print_board(game.get_board())
        
        if game.state.current_player == 1:
            # 玩家回合
            try:
                move = input("你的回合 (x y): ")
                if move.lower() == 'q':
                    break
                    
                x, y = map(int, move.split())
                if not game.player_move(x, y):
                    print("无效移动，请重试")
                    continue
            except ValueError:
                print("输入无效，请输入两个数字，例如 '7 7'")
                continue
        else:
            # AI回合
            print("AI思考中...")
            ai_move = game.ai_move()
            if ai_move:
                x, y = ai_move
                print(f"AI落子于: {x} {y}")
    
    print_board(game.get_board())
    
    if game.winner == 1:
        print("恭喜，你赢了！")
    elif game.winner == 2:
        print("AI获胜！")
    else:
        print("平局！")


if __name__ == "__main__":
    main()