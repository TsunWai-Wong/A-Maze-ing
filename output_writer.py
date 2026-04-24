from typing import Dict, List
from config_parser import Config
from maze import Maze


class OutputWriter:
    """
    Handles writing maze generation output to a file.
    This class formats and writes  the maze structure,
    entry/exit coordinates, and solution path, into
    a specified output file.

    Attributes:
    entry (tuple[int, int]): Maze entry coordinate.
    exit (tuple[int, int]): Maze exit coordinate.
    filename (str): Output file path.
    maze (Maze): Maze instance containing grid data.
    directions (List[str]): Path directions for solution output.
    """
    def __init__(self, config: Config, maze: Maze,
                 directions: List[str]) -> None:
        """Initialize the output writer"""
        self.entry = config.entry
        self.exit = config.exit
        self.filename = config.output_file
        self.maze = maze
        self.directions = directions

    def _convert_to_number(self, walls: Dict[str, bool]) -> str:
        """
        Convert wall configuration to a hexadecimal digit representation.

        Args:
        walls (Dict[str, bool]): Dictionary indicating presence of
        walls in directions 'N', 'E', 'S', and 'W'.

        Returns:
        str: Single hexadecimal character representing the wall state.
        """
        res = 0
        if walls.get("W"):
            res += 8
        if walls.get("S"):
            res += 4
        if walls.get("E"):
            res += 2
        if walls.get("N"):
            res += 1
        return hex(res)[-1].upper()

    def _write_maze(self) -> str:
        """
        Serialize the maze structure into a string representation.
        Iterates through all cells in the maze grid and converts each
        cell's wall configuration into a hexadecimal character.

        Returns:
        str: String representation of the full maze layout.
        """
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
        """
        Format entry and exit coordinates as output string.

        Returns:
        str: Formatted entry and exit coordinates.
        """
        return (f"{','.join(str(e) for e in self.entry)}\n"
                f"{','.join(str(e) for e in self.exit)}\n")

    def _write_path(self) -> str:
        """
        Joins all direction steps into a single continuous string.

        Returns:
        str: Concatenated path directions.
        """
        return "".join(self.directions)

    def write_output(self) -> None:
        """
        Write maze data, coordinates, and path to an output file.

        Creates or overwrites the output file and writes the serialized
        maze, entry/exit coordinates, and solution path in order.
        """
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
