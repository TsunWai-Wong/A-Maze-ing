from typing import List, Tuple, Set, Dict
from maze import Maze, Cell


class PathFinder:
    def __init__(self, maze: Maze):
        self.maze = maze
        self.queue: List[Cell] = []
        self.visited: Set[Cell] = set()
        self.parents: Dict = {}

    def _get_neighbors(self, cell: Cell) -> List[Tuple[str, Cell | None]]:
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
                    result.append((direction, self.maze.get_cell(neighbor_x,
                                                                 neighbor_y)))
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

            for direction, neighbor in self._get_neighbors(current):
                if neighbor is None:
                    continue
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    self.parents[neighbor] = (direction, current)
                    self.queue.append(neighbor)

    def find_path(self, start: Cell | None,
                  end: Cell | None) -> Tuple[List[Cell], List[str]]:
        if not start or not end:
            return ([], [])

        self._bfs(start, end)

        if end not in self.parents:
            return ([], [])

        path = []
        directions = []
        current = end

        while current is not None:
            path.append(current)
            parent_info = self.parents[current]
            if parent_info is None:
                break
            direction, parent = parent_info
            directions.append(direction)
            current = parent

        path.reverse()
        directions.reverse()
        return path, directions
