from typing import List
from maze import Maze, Cell


class PathFinder:
    def __init__(self, maze: Maze):
        self.maze = maze
        self.queue = []
        self.visited = set()
        self.parents = {}

    def _get_neighbors(self, cell: Cell) -> List[Cell]:
        result = []
        for direction in cell.walls:
            if cell.walls[direction] is False:
                if direction == "N":
                    neighbor_x = cell.x
                    neighbor_y = cell.y - 1
                if direction == "E":
                    neighbor_x = cell.x + 1
                    neighbor_y = cell.y
                if direction == "S":
                    neighbor_x = cell.x
                    neighbor_y = cell.y + 1
                if direction == "W":
                    neighbor_x = cell.x - 1
                    neighbor_y = cell.y
                if (neighbor_x >= 0 and neighbor_x < self.maze.width and
                   neighbor_y >= 0 and neighbor_y < self.maze.height):
                    result.append(self.maze.get_cell(neighbor_x, neighbor_y))
        return result

    def _bfs(self, start: Cell, end: Cell) -> None:
        self.queue = [start]
        self.visited = {start}
        self.parents = {start: None}

        while self.queue:
            current = self.queue.pop(0)

            if (current.x == end.x
               and current.y == end.y):
                break

            for neighbor in self._get_neighbors(current):
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    self.parents[neighbor] = current
                    self.queue.append(neighbor)

    def find_path(self, start: Cell, end: Cell) -> List[Cell]:
        self._bfs(start, end)
        path = [end]
        parent = self.parents[end]
        while parent:
            path.append(parent)
            parent = self.parents[parent]
        return path


if __name__ == "__main__":
    from maze import HuntAndKillGenerator, render_maze
    maze = Maze(10, 10)
    generator = HuntAndKillGenerator(42)
    generator.generate(maze)
    render_maze(maze)

    pathfinder = PathFinder(maze)
    start_cell = maze.get_cell(0, 0)
    end_cell = maze.get_cell(9, 9)
    path = pathfinder.find_path(start_cell, end_cell)
    for cell in path:
        print(f"{cell.x}, {cell.y}")
