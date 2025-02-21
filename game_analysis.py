"""
Advanced example: Using FiberTree to analyze game moves.
"""

from fbtree import create_tree, load_tree, Move
import random

class SimpleGame:
    """A simple game with 3x3 board for demonstration purposes."""
    
    def __init__(self):
        self.board = [None] * 9
        self.current_player = 'X'
        self.moves_made = 0
    
    def make_move(self, position):
        """Make a move at the given position (0-8)."""
        if not (0 <= position < 9) or self.board[position] is not None:
            return False
        
        self.board[position] = self.current_player
        self.moves_made += 1
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True
    
    def check_win(self):
        """Check if the game has been won."""
        # Check rows, columns, and diagonals
        win_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        
        for pattern in win_patterns:
            if (self.board[pattern[0]] is not None and
                self.board[pattern[0]] == self.board[pattern[1]] == self.board[pattern[2]]):
                return self.board[pattern[0]]
        
        if self.moves_made == 9:
            return 'draw'
        
        return None
    
    def available_moves(self):
        """Return list of available move positions."""
        return [i for i, val in enumerate(self.board) if val is None]
    
    def reset(self):
        """Reset the game."""
        self.board = [None] * 9
        self.current_player = 'X'
        self.moves_made = 0

def simulate_games(num_games=100):
    """Simulate games and build a FiberTree of game paths."""
    # Create a tree to store game paths
    tree = create_tree()
    
    for _ in range(num_games):
        game = SimpleGame()
        move_sequence = []
        
        # Play a game with random moves
        while True:
            available = game.available_moves()
            if not available:
                break
                
            # Make a random move
            move = random.choice(available)
            game.make_move(move)
            move_sequence.append(Move(move))
            
            # Check for game end
            result = game.check_win()
            if result:
                break
        
        # Record the game path in the tree
        tree.start_path()
        for move in move_sequence:
            tree.add_move(move)
        
        # Determine outcome
        if result == 'X':
            tree.record_outcome('win')
        elif result == 'O':
            tree.record_outcome('loss')
        else:
            tree.record_outcome('draw')
    
    return tree

def analyze_game_tree(tree):
    """Analyze the game tree."""
    # Get overall statistics
    print("\nGame Tree Analysis:")
    print(f"Total fibers: {len(tree)}")
    
    # Get move frequency at each depth
    for depth in range(1, 10):
        freq = tree.get_move_frequency(depth=depth)
        if freq:
            print(f"\nDepth {depth} move frequencies:")
            sorted_moves = sorted(freq.items(), key=lambda x: x[1], reverse=True)
            for move, count in sorted_moves[:3]:
                print(f"  Position {move}: {count} times")
    
    # Generate a heatmap
    heatmap = tree.generate_move_heatmap(board_size=3)
    print("\nMove heatmap (frequency):")
    for row in heatmap:
        print("  " + " ".join(f"{val:3d}" for val in row))
    
    # Get common paths
    print("\nCommon paths:")
    common_paths = tree.get_common_path_statistics(min_visits=5)
    for i, path_info in enumerate(common_paths[:3]):
        moves_str = " → ".join(str(move) for move in path_info['path'])
        print(f"  Path {i+1}: {moves_str}")
        print(f"    Visits: {path_info['visits']}, Win rate: {path_info['win_rate']:.2f}")
    
    # Get path diversity analysis
    diversity = tree.analyze_path_diversity()
    print("\nPath diversity:")
    print(f"  Max depth: {diversity['max_depth']}")
    print(f"  Avg branching factor: {diversity['avg_branching_factor']:.2f}")
    print(f"  Leaf nodes: {diversity['leaf_nodes']}")

def main():
    # Simulate games and build tree
    print("Simulating 100 random games...")
    tree = simulate_games(100)
    
    # Analyze the resulting tree
    analyze_game_tree(tree)
    
    # Save the tree
    tree.save("game_analysis.json")
    print("\nTree saved to game_analysis.json")
    
    # Optional: Visualize tree (limited depth for readability)
    print("\nTree visualization (limited to depth 3):")
    tree.visualize(max_depth=3)

if __name__ == "__main__":
    main()