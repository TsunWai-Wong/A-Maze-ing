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

    def _convert_to_number(self, walls: Dict[str, bool]) -> None:
        """
        e.g. from south and west to 3
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


if __name__ == "__main__":
    import maze as maze_module
    my_maze = Maze(10, 10)
    generator = maze_module.HuntAndKillGenerator(42)
    generator.generate(my_maze)
    maze_module.render_maze(my_maze)
    directions = ['S', 'S', 'E', 'E', 'E', 'E', 'N', 'E', 'E', 'E',
                  'E', 'N', 'E', 'S', 'S', 'S', 'S', 'S', 'W', 'W',
                  'S', 'E', 'E', 'S', 'S', 'W', 'W', 'W', 'S', 'E',
                  'E', 'E']
    writer = OutputWriter("output.txt", my_maze, directions)
    print(writer._write_maze())
    print(writer._write_path())
