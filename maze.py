import random
from typing import List, Tuple, Optional

DIRECTIONS: dict[str, Tuple[int, int]] = {
    "N": (0, -1),
    "E": (1, 0),
    "S": (0, 1),
    "W": (-1, 0),
}

OPPOSITE: dict[str, str] = {
    "N": "S",
    "E": "W",
    "S": "N",
    "W": "E",
}
"""
Pattern:
+---+           +---+---+---+
|   |           |   |   |   |
+---+           +---+---+---+
|   |                   |   |
+---+---+---+   +---+---+---+
|   |   |   |   |   |   |   |
+---+---+---+   +---+---+---+
        |   |   |   |
        +---+   +---+---+---+
        |   |   |   |   |   |
        +---+   +---+---+---+
"""


class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.visited: bool = False
        self.walls = {"N": True, "E": True, "S": True, "W": True}

        self.is_pattern: bool = False


class Maze:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid: List[List[Cell]] = [
            [Cell(x, y) for x in range(width)]
            for y in range(height)
        ]

    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def neighbors(self, cell: Cell) -> List[Tuple[str, Cell]]:
        result: List[Tuple[str, Cell]] = []

        for direction, (dx, dy) in DIRECTIONS.items():
            nx, ny = cell.x + dx, cell.y + dy
            neighbor = self.get_cell(nx, ny)

            if neighbor is not None and not neighbor.is_pattern:
                result.append((direction, neighbor))
        return result

    def remove_wall(self, c1: Cell, c2: Cell, direction: str) -> None:
        c1.walls[direction] = False
        c2.walls[OPPOSITE[direction]] = False


class HuntAndKillGenerator:
    def __init__(self, seed: Optional[int] = None) -> None:
        if seed is not None:
            random.seed(seed)

    def generate(self, maze: Maze) -> None:

        current = maze.get_cell(0, 0)
        if current is None:
            return

        current.visited = True

        while current:
            # killing phase
            unvisited_neighbors = [
                (d, n)
                for d, n in maze.neighbors(current)
                if not n.visited
            ]

            if unvisited_neighbors:
                random.shuffle(unvisited_neighbors)

                moved = False

                for direction, next_cell in unvisited_neighbors:
                    if not self._creates_large_room(maze, current, direction):
                        maze. remove_wall(current, next_cell, direction)
                        next_cell.visited = True
                        current = next_cell
                        moved = True
                        break

                if not moved:
                    current = self._hunt(maze)
            else:
                current = self._hunt(maze)

    def _hunt(self, maze: Maze) -> Optional[Cell]:
        candidates = []
        for y in range(maze.height):
            for x in range(maze.width):
                cell = maze.get_cell(x, y)
                if cell is None or cell.visited or cell.is_pattern:
                    continue

                visited_neighbors = [
                    (d, n)
                    for d, n in maze.neighbors(cell)
                    if n.visited
                ]

                if visited_neighbors:
                    candidates.append((cell, visited_neighbors))

        if not candidates:
            return None
            
        cell, visited_neighbors = random.choice(candidates)
        direction, neighbor = random.choice(visited_neighbors)
        maze.remove_wall(cell, neighbor, direction)
        cell.visited = True
        return cell

    def _creates_large_room(
            self,
            maze: Maze,
            cell: Cell,
            direction: str
    ) -> bool:
        # check if we have 3x3 open areas
        dx, dy = DIRECTIONS[direction]
        nx, ny = cell.x + dx, cell.y + dy

        # checking small square around target
        for y in range(ny - 1, ny + 2):
            for x in range(nx - 1, nx + 2):
                c = maze.get_cell(x, y)
                if c is None:
                    continue
                # Counting open walls
                open_walls = sum(not w for w in c.walls.values())
                if open_walls >= 3:
                    return True
        return False


def add_42_pattern(maze: Maze) -> None:
    # check if fits
    if maze.width < 9 or maze.height < 7:
        print("Maze is too small for 42! \n Be more Ambitious.")
        return

    # finding center of maze
    center_x = maze.width // 2
    center_y = maze.height // 2

    # defining 42 coordinates
    pattern_4 = [
        (0, 0), (0, 1), (0, 2),
        (1, 2),
        (2, 2), (2, 3), (2, 4)
    ]
    pattern_2 = [
        (0, 0), (1, 0), (2, 0),
        (2, 1),
        (0, 2), (1, 2), (2, 2),
        (0, 3),
        (0, 4), (1, 4), (2, 4),
    ]

    offset_4_x = center_x - 3
    offset_4_y = center_y - 2

    offset_2_x = center_x + 1
    offset_2_y = center_y - 2

    def block_cell(x: int, y: int) -> None:
        cell = maze.get_cell(x, y)
        if cell is None:
            return

        # marking cell as a pattern part
        cell.is_pattern = True
        cell.visited = True

        # using fully closed cells for pattern
        cell.walls = {"N": True, "E": True, "S": True, "W": True}

        for direction, (dx, dy) in DIRECTIONS.items():
            neighbor = maze.get_cell(x + dx, y + dy)
            if neighbor:
                neighbor.walls[OPPOSITE[direction]] = True

    for dx, dy in pattern_4:
        block_cell(offset_4_x + dx, offset_4_y + dy)

    for dx, dy in pattern_2:
        block_cell(offset_2_x + dx, offset_2_y + dy)


def render_maze(maze: Maze) -> None:
    width = maze.width
    height = maze.height

    # drawing bordrs - top
    print("+" + "---+" * width)

    # vertical and Horizontal
    for y in range(height):
        line1 = "|"
        line2 = "+"

        for x in range(width):
            cell = maze.get_cell(x, y)
            if cell is None:
                continue

            if cell.is_pattern:
                line1 += "███"
            else:
                # space in the cell
                line1 += "   "

            # right wall
            if cell.walls["E"]:
                line1 += "|"
            else:
                line1 += " "

            # bottom wall
            if cell.walls["S"]:
                line2 += "---+"
            else:
                line2 += "   +"

        print(line1)
        print(line2)


def get_user_input() -> tuple[int, int, Optional[int]]:
    try:
        width = int(input("give me width, pls: "))
        height = int(input("And also height: "))

        seed_input = input("Last thing - seed. Enter seed number: ")
        seed = int(seed_input) if seed_input else None

        if width <= 0 or height <= 0:
            raise ValueError

        return width, height, seed
    except ValueError:
        print("bad numbers, my master.\n But I'll give you 10x10 maze")
        return 10, 10, None


def main() -> None:
    print("=== HUNT and KILL ===")
    width, height, seed = get_user_input()

    maze = Maze(width, height)

    add_42_pattern(maze)

    generator = HuntAndKillGenerator(seed)

    generator.generate(maze)

    print("\n Behold! The MAZE: \n")
    render_maze(maze)


if __name__ == "__main__":
    main()