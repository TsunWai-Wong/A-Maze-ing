from typing import List
from mlx import Mlx
from gui.image import Image
from maze import Maze


image_length = 300
cell_length = 50
stroke_length = 6

# format: 0xAARRGGBB
white = 0xFFFFFFFF
green = 0xFF00FF00
blue = 0xFF0000FF
yellow = 0xFFFFFF00


class Renderer:
    def __init__(self):
        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.window = self.mlx.mlx_new_window(self.mlx_ptr, 1200, 800, "test")

    def _cell_position(self, n: int) -> float:
        if n == 0:
            return 0
        return n * (cell_length - stroke_length)

    def _draw_interior_of_cell(self, image: Image, colour: str) -> None:
        image.draw_shape(colour, stroke_length, stroke_length, cell_length - 2 * stroke_length, cell_length - 2 * stroke_length)

    def _draw_side_of_cell(self, image: Image, colour: str, direction: str) -> None:
        # N
        if direction == "N":
            start_x = stroke_length
            start_y = 0
            image.draw_shape(colour, start_x, start_y, cell_length - 2 * stroke_length, stroke_length)

        # NE
        if direction == "NE":
            start_x = cell_length - stroke_length
            start_y = 0
            image.draw_shape(colour, start_x, start_y, stroke_length, stroke_length)

        # E
        if direction == "E":
            start_x = cell_length - stroke_length
            start_y = stroke_length
            image.draw_shape(colour, start_x, start_y, stroke_length, cell_length - 2 * stroke_length)

        # SE
        if direction == "SE":
            start_x = cell_length - stroke_length
            start_y = cell_length - stroke_length
            image.draw_shape(colour, start_x, start_y, stroke_length, stroke_length)

        # S
        if direction == "S":
            start_x = stroke_length
            start_y = cell_length - stroke_length
            image.draw_shape(colour, start_x, start_y, cell_length - 2 * stroke_length, stroke_length)

        # SW
        if direction == "SW":
            start_x = 0
            start_y = cell_length - stroke_length
            image.draw_shape(colour, start_x, start_y, stroke_length, stroke_length)

        # W
        if direction == "W":
            start_x = 0
            start_y = stroke_length
            image.draw_shape(colour, start_x, start_y, stroke_length, cell_length - 2 * stroke_length)

        # NW
        if direction == "NW":
            start_x = 0
            start_y = 0
            image.draw_shape(colour, start_x, start_y, stroke_length, stroke_length)

    def _close_window(self, *_):
        self.mlx.mlx_loop_exit(self.mlx_ptr)
        return 0

    def render(self, maze: Maze, path: List) -> None:
        path_position = list(map(lambda cell: (cell.x, cell.y), path))
        print(path_position)
        for i in range(maze.height):
            for j in range(maze.width):
                image = Image(self.mlx, self.mlx_ptr, image_length, image_length)
                # Wall
                for direction in ["NE", "SE", "SW", "NW"]:
                    self._draw_side_of_cell(image, blue, direction)
                cell = maze.get_cell(j, i)
                for direction in cell.walls:
                    if cell.walls[direction]:
                        self._draw_side_of_cell(image, blue, direction)
                    else:
                        self._draw_side_of_cell(image, white, direction)

                # Interior
                if (j, i) in path_position:
                    self._draw_interior_of_cell(image, yellow)
                else:
                    self._draw_interior_of_cell(image, white)
                image.put_to_window(self.window, self._cell_position(j), self._cell_position(i))

        # Keep the window being opened
        self.mlx.mlx_hook(self.window, 33, 0, self._close_window, None)
        self.mlx.mlx_loop(self.mlx_ptr)
