import random
from typing import List, Tuple, Optional

DIRECTIONS: dict[str, Tuple[int, int]] = {
    "N": (0, -1),
    "E": (1, 0),
    "S": (0, 1),
    "W": (-1, 0),
}

OPPOSITE: dict[str, str] = {
    "N" : "S",
    "E" : "W",
    "S" : "N",
    "W" : "E",
}

class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.visited = False
        self.walls = {"N": True, "E": True, "S": True, "W": True}


class Maze:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid: List[List[Cell]] = [
            [Cell(x, y) for x in range(width)]
            for y in range(height)
        ]

    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        if 0<= x <self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None
    
    def neighbors(self, cell: Cell) -> List[Tuple[str, Cell]]:
        result: List[Tuple[str, Cell]] = []
        for direction, (dx, dy) in DIRECTIONS.items():
            nx, ny = cell.x + dx, cell.y + dy
            neighbor = self.get_cell(nx, ny)
            if neighbor is not None:
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
        for y in range(maze.height):
            for x in range(maze.width):
                cell = maze.get_cell(x, y)
                if cell is None or cell.visited:
                    continue

                visited_neighbors = [
                    (d, n)
                    for d, n in maze.neighbors(cell)
                    if n.visited
                ]

                if visited_neighbors:
                    direction, neighbor = random.choice(visited_neighbors)
                    maze.remove_wall(cell, neighbor, direction)
                    cell.visited = True
                    return cell
        return None
    
    def _creates_large_room(
            self,
            maze: Maze,
            cell: Cell,
            direction: str
    ) -> bool:
        # check if we have 3x3 open areas
        dx, dy = DIRECTIONS[direction]
        nx, ny = cell.x + dx, cell.y + dy

        #checking small square around target
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
        width = int(input("Yo, gimme maze width, fast!: "))
        height = int(input("Better also have ma maze height: "))

        seed_input = input("The seed! I need a seed, man!: ")
        seed = int(seed_input) if seed_input else None

        if width <= 0 or height <= 0:
            raise ValueError

        return width, height, seed
    except ValueError:
        print("What's yo goofy ass given me? I need real numbaz!\nI'll show you 10x10 anyways")
        return 10, 10, None

def main() -> None:
    print("=== It's a HUNT and KILL maze generator, man ===")
    width, height, seed = get_user_input()

    maze = Maze(width, height)
    generator = HuntAndKillGenerator(seed)

    generator.generate(maze)

    print("\n Behold! The MAZE: \n")
    render_maze(maze)


if __name__ == "__main__":
    main()