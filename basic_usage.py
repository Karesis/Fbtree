"""
Example demonstrating basic usage of FiberTree.
"""

from fbtree import create_tree, Move

def main():
    # Create a tree in memory
    tree = create_tree()
    
    # Create and record some paths
    
    # Path 1: A winning sequence
    tree.start_path()
    tree.add_move(Move("A"))
    tree.add_move(Move("B"))
    tree.add_move(Move("C"))
    tree.record_outcome('win')
    
    # Path 2: Another winning sequence
    tree.start_path()
    tree.add_move(Move("A"))
    tree.add_move(Move("B"))
    tree.add_move(Move("D"))
    tree.record_outcome('win')
    
    # Path 3: A losing sequence
    tree.start_path()
    tree.add_move(Move("A"))
    tree.add_move(Move("E"))
    tree.record_outcome('loss')
    
    # Get the current full path
    current_path = tree.get_complete_path()
    print(f"Current path: {[str(move) for move in current_path]}")
    
    # Get statistics for the current path
    stats = tree.get_statistics()
    print(f"Current path statistics: {stats}")
    
    # Find the best continuation from a specific position
    starting_path = [Move("A")]
    best_moves = tree.get_best_continuation(starting_path, top_n=2)
    print(f"Best continuations from 'A':")
    for move_info in best_moves:
        print(f"  {move_info['move']} - Win rate: {move_info['win_rate']:.2f}, Visits: {move_info['visits']}")
    
    # Get move frequency at first position
    first_move_freq = tree.get_move_frequency(depth=1)
    print(f"First move frequencies: {first_move_freq}")
    
    # Save the tree to a file
    tree.save("my_first_tree.json")
    print("Tree saved to my_first_tree.json")
    
if __name__ == "__main__":
    main()