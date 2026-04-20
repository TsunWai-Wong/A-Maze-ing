from typing import Dict, List
from maze import Maze
# walls={"N": True, "E": True, "S": True, "W": True}


# for development
import maze as maze_module


class OutputWriter:
    def __init__(self, filename: str, maze: Maze, directions: List):
        self.filename = filename
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
        return res

    def _write_coordinates(self) -> None:
        pass

    def _write_path(self) -> None:
        return "".join(self.directions)

    def write_output(self) -> None:
        try:
            with open(self.filename) as file:
                file.write()
        except IOError:
            # Disk is full, File system error, Invalid file path
            print()
        except PermissionError:
            print(0)


if __name__ == "__main__":
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
