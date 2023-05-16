# DFS_Maze_Generation_Visualizer
Visualizes the Depth First Search algorithm for maze generation. Visualizer was fully coded in python using pygame.
The cover page and interaction with buttons/sliders was coded using pygame GUI. 

# Interactions
Press Visualize button to start visualization. 

Press Quit button to quit the application.

Utilize the slider to adjust speed of visualization. 

# Game Demo


https://github.com/OP-Patel/DFS_Maze_Generation_Visualizer/assets/133251616/429746b2-219e-4e92-b3e1-24851a63b158



# Basic Algorithm Logic
The algorithm starts at a given cell and marks it as visited. 
It selects a random neighboring cell that hasn't been visited yet and makes that one the current cell, marks it as visited and removes 
the wall between the two cells. The current cell is then the next cell, and so on. The current cell is added to the stack, which is then popped to return when no neighbouring cells are unvisited, this allows the algorithm to visit all the cells.
