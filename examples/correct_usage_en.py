"""
FiberTree 1.2.0 Correct Usage Example
Demonstrating complete usage including basic features, analysis, and visualization
"""

import os
import json
from pprint import pprint
import fbtree
from fbtree import create_tree, Move
from fbtree import analyze_path_frequency, find_winning_paths, calculate_move_impact
from fbtree import visualize_tree_text, generate_path_summary, generate_graphviz, generate_d3_json

print(f"FiberTree version: {fbtree.__version__}")

# 1. Creating a tree and adding paths
print("\n=== 1. Creating a Tree and Adding Paths ===")
tree = create_tree()  # Using memory storage backend
print("* Tree created")

# Adding the first path (win)
print("* Adding path 1 (win)")
tree.start_path()
tree.add_move(Move("Action A"))
tree.add_move(Move("Result 1"))
tree.record_outcome("win")  # Correct way to record outcome

# Adding the second path (win)
print("* Adding path 2 (win)")
tree.start_path()
tree.add_move(Move("Action B"))
tree.add_move(Move("Result 2"))
tree.record_outcome("win")

# Adding the third path (loss)
print("* Adding path 3 (loss)")
tree.start_path()
tree.add_move(Move("Action C"))
tree.add_move(Move("Result 3"))
tree.record_outcome("loss")

# Adding the fourth path (win) - reusing previous action
print("* Adding path 4 (win - reusing Action A)")
tree.start_path()
tree.add_move(Move("Action A"))
tree.add_move(Move("Result 4"))
tree.record_outcome("win")

# 2. Getting basic statistics
print("\n=== 2. Basic Statistics ===")
stats = tree.get_statistics()
print("* Tree statistics:")
pprint(stats)

# 3. Saving and loading
print("\n=== 3. Saving and Loading Tree ===")
json_file = "example_tree_en.json"
tree.save(json_file)
print(f"* Tree saved to {json_file}")

# You can use the following method to load a tree
# loaded_tree = fbtree.load_tree(json_file)
# print("* Tree loaded successfully")

# 4. Using analysis features
print("\n=== 4. Using Analysis Features ===")
# Get all fibers for analysis
fibers = tree.get_all_fibers()

# Analyze path frequency
print("\n* Path frequency analysis:")
freq_results = analyze_path_frequency(fibers)
pprint(freq_results)

# Find winning paths
print("\n* Winning paths analysis:")
winning_paths = find_winning_paths(fibers, min_visits=1, min_win_rate=0.5)
for path, win_rate in winning_paths:
    path_str = " -> ".join([str(move) for move in path])
    print(f"  Path: {path_str}, Win Rate: {win_rate:.2f}")

# Calculate move impact
print("\n* Move impact analysis:")
impact_results = calculate_move_impact(fibers)
for move, stats in impact_results.items():
    print(f"  Move {move}: Win Rate={stats['win_rate']:.2f}, Count={stats['count']}")

# 5. Using visualization features
print("\n=== 5. Using Visualization Features ===")

# Text visualization
print("\n* Tree text visualization:")
text_viz = visualize_tree_text(fibers, max_depth=3)
print(text_viz)

# Path summary
print("\n* Path summary:")
path_summary = generate_path_summary(fibers, min_visits=1)
print(path_summary)

# Graphviz visualization (optional)
dot_file = "example_tree_en.dot"
dot_string = generate_graphviz(fibers, max_depth=3)
with open(dot_file, "w") as f:
    f.write(dot_string)
print(f"\n* Generated Graphviz DOT file: {dot_file}")

# D3.js JSON data (optional)
d3_file = "example_tree_en_d3.json"
d3_json = generate_d3_json(fibers)
with open(d3_file, "w") as f:
    f.write(d3_json)
print(f"* Generated D3.js JSON file: {d3_file}")

# 6. Cleanup
print("\n=== 6. Cleanup ===")
# Only delete generated files when the example is done
for file in [json_file, dot_file, d3_file]:
    if os.path.exists(file):
        os.remove(file)
        print(f"* Removed temporary file: {file}")

print("\nExample completed!") 