_This project has been created as part of the 42 curriculum by oralniko, tswong._


# Description
A-Maze-ing is a Python project that generates mazes from a configuration file, saves them in a hexadecimal wall format, and displays them visually in a GUI. Its goal is to create a valid maze with configurable size, entry and exit points, optional perfect-maze generation, and reproducible results using a seed.

The program also computes the shortest path from the entry to the exit, writes the maze and path data to an output file, and shows the maze with interactive controls to regenerate it, hide or show the path, and change wall colors. The code is organized into reusable parts so that the generation, pathfinding, writing, and rendering logic can be used independently in other projects.  

# Instructions 
1. Configuration  
The program uses default_config.txt by default.
You can use a different configuration file, but you must update the CONFIG_FILE variable in the Makefile accordingly.

2. Install dependencies  
Install all required dependencies, including the GUI library (mlx-2.2-py3-none-any.whl):
```
make install
```

3. Run the program  
```
make run
```

4. GUI Interaction  
Once the window is open, you can interact with the maze:
- Press `R` to regenerate the maze
- Press `P` to show or hide the solution path
- Press `C` to change the color palette
- Press `ESC` to exit  

# Resources
Documentation on MiniLibx: https://harm-smits.github.io/42docs/libs/minilibx/getting_started.html
Tutorial video on MiniLibx: https://www.youtube.com/watch?v=bYS93r6U0zg
DFS Maze generation algorithm: https://www.algosome.com/articles/maze-generation-depth-first.html
PEP style guide: https://google.github.io/styleguide/pyguide.html

GenAI is used for clarifying technical idea, debugging and documentation

# Technical Details

### Configuration files
This configuration file defines the parameters used to generate a maze:
- **WIDTH** and **HEIGHT** specify the maze’s dimensions in columns and rows, respectively.
- **ENTRY** sets the starting position of the maze as a pair of coordinates `x,y`
- **EXIT** defines the goal position of the maze
- **OUTPUT_FILE** determines the name of the file where the generated maze will be saved.
- **PERFECT** indicates whether the maze should be “perfect,” meaning it has no loops and no isolated sections—there is exactly one unique path between any two points.
- **SEED** (optional) allows you to fix the random generation process for reproducibility. If provided, the same maze will be generated each time; if omitted, the maze will vary between runs.


### Maze Generation Algorithm

Maze generator using modified Hunt-and-Kill algorithm. Produces a perfect maze — every cell is reachable and there is exactly one path between any two points.
The algorithm starts at the top-left cell and randomly walks into unvisited neighbours, carving passages as it goes (Kill phase). When it gets stuck, it scans the grid for random unvisited cell that borders an already-visited one, connects them, and resumes walking from there (Hunt phase). This repeats until every cell has been visited.

Before generation runs, a set of cells in the centre is marked as solid and permanently walled off, forming the "42" pattern in a pixel font. The algorithm never carves into solid cells, so the pattern is preserved untouched. If the maze is too small to fit the pattern, it is skipped.

Passing a seed in the config file makes generation reproducible — the same seed always produces the same maze.

### Path Finding Algorithm
The pathfinding is implemented using the Breadth-First Search (BFS) algorithm, which guarantees the shortest path in an unweighted grid such as a maze. Starting from the entry cell, the algorithm explores all reachable neighboring cells level by level, ensuring that the first time the exit is reached corresponds to the shortest possible path.  

Accessible neighbors are determined by checking which walls are open, meaning movement is only allowed where no wall blocks the direction. During traversal, each visited cell is stored along with its parent and the direction taken to reach it. This information is later used to reconstruct the path.  

Once the exit is found, the algorithm backtracks from the exit to the start using the stored parent relationships, producing both the sequence of cells and the list of directions (N, E, S, W). If no path exists, an empty result is returned.  

### Reusability of Codes

1. Maze generation:
The Maze and Cell classes are independent of the generation algorithm, so they can be reused with other maze-generation strategies or grid-based applications. The HuntAndKillGenerator encapsulates the algorithm logic and can be easily replaced or extended without modifying the maze structure.

2. Path-finder:
It is designed as a standalone module that operates on a Maze without modifying its structure, making it reusable for any grid-based maze implementation that follows the same interface.

3. Maze renderer:
It is modular and separates visualization from maze generation and pathfinding logic, making it reusable for any grid-based data structure with similar properties. It only depends on external inputs (Maze, PathFinder, and configuration).

### Team and project management

Roles:
oralniko: maze generation, data structure and modeling, UI Design and Colouring features
tswong: file input/ output, pathfinding algorithm, maze renderering in GUI

Possible Improvements:
- Scale of the maze: It can modified to support larger maze generation 
- Performance: Speed of the programme can be improved if the alogirhm is further optimized
