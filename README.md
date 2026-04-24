_This project has been created as part of the 42 curriculum by oralniko, tswong._


# Description

# Instructions

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
* **ENTRY** sets the starting position of the maze as a pair of coordinates `(x,y)`
* **EXIT** defines the goal position of the maze
* **OUTPUT_FILE** determines the name of the file where the generated maze will be saved.
* **PERFECT** indicates whether the maze should be “perfect,” meaning it has no loops and no isolated sections—there is exactly one unique path between any two points.
* **SEED** (optional) allows you to fix the random generation process for reproducibility. If provided, the same maze will be generated each time; if omitted, the maze will vary between runs.


### Maze Generation Algorithm

Maze generator using modified Hunt-and-Kill algorithm. Produces a perfect maze — every cell is reachable and there is exactly one path between any two points.
The algorithm starts at the top-left cell and randomly walks into unvisited neighbours, carving passages as it goes (Kill phase). When it gets stuck, it scans the grid for random unvisited cell that borders an already-visited one, connects them, and resumes walking from there (Hunt phase). This repeats until every cell has been visited.

Before generation runs, a set of cells in the centre is marked as solid and permanently walled off, forming the "42" pattern in a pixel font. The algorithm never carves into solid cells, so the pattern is preserved untouched. If the maze is too small to fit the pattern, it is skipped.

Passing a seed in the config file makes generation reproducible — the same seed always produces the same maze.

### Reusuability of Codes

### Team and project managemen


Roles:
oralniko: 
tswong: file input/ output, pathfinding algorithm, maze renderering in GUI

Improvements

