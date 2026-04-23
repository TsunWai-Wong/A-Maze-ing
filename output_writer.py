from typing import Dict, List
from config_parser import Config
from maze import Maze


class OutputWriter:
    def __init__(self, config: Config, maze: Maze, directions: List) -> None:
        self.entry = config.entry
        self.exit = config.exit
        self.filename = config.output_file
        self.maze = maze
        self.directions = directions

    def _convert_to_number(self, walls: Dict[str, bool]) -> str:
        """
        e.g. from south and west to "3"
        """
        res = 0
        if walls.get("N"):
            res += 8
        if walls.get("E"):
            res += 4
        if walls.get("S"):
            res += 2
        if walls.get("W"):
            res += 1
        return hex(res)[-1].upper()

    def _write_maze(self) -> str:
        res = ""
        maze_height = self.maze.height
        maze_width = self.maze.width
        for i in range(maze_height):
            for j in range(maze_width):
                cell = self.maze.get_cell(j, i)
                if cell:
                    res += self._convert_to_number(cell.walls)
            res += "\n"
        return f"{res}\n"

    def _write_coordinates(self) -> str:
        return (f"{','.join(str(e) for e in self.entry)}\n"
                f"{','.join(str(e) for e in self.exit)}\n")

    def _write_path(self) -> str:
        return "".join(self.directions)

    def write_output(self) -> None:
        try:
            with open(self.filename, "w") as file:
                file.write(self._write_maze())
                file.write(self._write_coordinates())
                file.write(self._write_path())
        except PermissionError:
            print("Error: No permission for the output file")
            exit(1)
        except OSError as e:
            # Disk is full, File system error, Invalid file path
            print(f"Error: '{self.filename}' {e.strerror}")
            exit(1)
