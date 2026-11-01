# Haunted Maze Pathfinder

A Pygame maze project I built up over a few labs in my A.I. for Game Programming class. It is a maze where AI characters search for the exit and I can watch how they think.

## What it does
- Generates a random maze every time using DFS (recursive backtracker)
- Player you can move around with the arrow keys or WASD
- Two NPCs that start at the entrance and search for the goal at the same time
  - BFS (finds the path with the fewest steps)
  - Dijkstra (finds the cheapest path)
- Weighted terrain: floor costs 1, mud costs 3, web costs 6, so the shortest path isn't always the cheapest
- Visualization: you can see explored cells, the frontier, the current cell, and the final path. Dijkstra also shows the total cost on each cell it explored
- Search results (steps, total cost, nodes explored) print in the terminal for each NPC

**Controls:** arrow keys/WASD to move, SPACE for a new maze

## What I learned
BFS and Dijkstra look similar but BFS only counts steps, while Dijkstra counts cost. On a maze with mud and webs, BFS can take fewer steps but pay more in total.