from typing import List
from mlx import Mlx
from gui.image import Image
from maze import Maze

# format: 0xAARRGGBB
white = 0xFFFFFFFF
green = 0xFF00FF00
blue = 0xFF0000FF
yellow = 0xFFFFFF00


class Renderer:
    def __init__(self, maze: Maze):
        self.maze = maze
        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()

        self.window_width = 1200
        self.window_height = 900
        self.window = self.mlx.mlx_new_window(self.mlx_ptr, self.window_width, self.window_height, "test")
        self.info_width = 300

        self.min_padding = 30

        maze_area_width = self.window_width - self.info_width
        maze_area_height = self.window_height

        available_width = maze_area_width - 2 * self.min_padding
        available_height = maze_area_height - 2 * self.min_padding

        cell_size_x = available_width // self.maze.width
        cell_size_y = available_height // self.maze.height

        self.image_length = max(4, min(cell_size_x, cell_size_y))
        self.cell_length = self.image_length
        self.stroke_length = max(1, self.cell_length // 10)

        maze_pixel_width = self.maze.width * self.cell_length
        maze_pixel_height = self.maze.height * self.cell_length

        self.padding_x_side = (maze_area_width - maze_pixel_width) // 2
        self.padding_y_side = (self.window_height - maze_pixel_height) // 2

    def _cell_position(self, n: int) -> float:
        if n == 0:
            return 0
        return n * (self.cell_length - self.stroke_length)

    def _draw_interior_of_cell(self, image: Image, colour: str) -> None:
        image.draw_shape(colour, self.stroke_length, self.stroke_length, self.cell_length - 2 * self.stroke_length, self.cell_length - 2 * self.stroke_length)

    def _draw_side_of_cell(self, image: Image, colour: str, direction: str) -> None:
        # N
        if direction == "N":
            start_x = self.stroke_length
            start_y = 0
            image.draw_shape(colour, start_x, start_y, self.cell_length - 2 * self.stroke_length, self.stroke_length)

        # NE
        if direction == "NE":
            start_x = self.cell_length - self.stroke_length
            start_y = 0
            image.draw_shape(colour, start_x, start_y, self.stroke_length, self.stroke_length)

        # E
        if direction == "E":
            start_x = self.cell_length - self.stroke_length
            start_y = self.stroke_length
            image.draw_shape(colour, start_x, start_y, self.stroke_length, self.cell_length - 2 * self.stroke_length)

        # SE
        if direction == "SE":
            start_x = self.cell_length - self.stroke_length
            start_y = self.cell_length - self.stroke_length
            image.draw_shape(colour, start_x, start_y, self.stroke_length, self.stroke_length)

        # S
        if direction == "S":
            start_x = self.stroke_length
            start_y = self.cell_length - self.stroke_length
            image.draw_shape(colour, start_x, start_y, self.cell_length - 2 * self.stroke_length, self.stroke_length)

        # SW
        if direction == "SW":
            start_x = 0
            start_y = self.cell_length - self.stroke_length
            image.draw_shape(colour, start_x, start_y, self.stroke_length, self.stroke_length)

        # W
        if direction == "W":
            start_x = 0
            start_y = self.stroke_length
            image.draw_shape(colour, start_x, start_y, self.stroke_length, self.cell_length - 2 * self.stroke_length)

        # NW
        if direction == "NW":
            start_x = 0
            start_y = 0
            image.draw_shape(colour, start_x, start_y, self.stroke_length, self.stroke_length)

    def _close_window(self, *_):
        self.mlx.mlx_loop_exit(self.mlx_ptr)
        return 0

    def render(self, maze: Maze, path: List) -> None:
        path_position = {(cell.x, cell.y) for cell in path}
        for i in range(maze.height):
            for j in range(maze.width):
                image = Image(self.mlx, self.mlx_ptr, self.image_length, self.image_length)
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
                image.put_to_window(self.window, self._cell_position(j) + self.padding_x_side, self._cell_position(i) + self.padding_y_side)

        # Keep the window being opened
        self.mlx.mlx_hook(self.window, 33, 0, self._close_window, None)
        self.mlx.mlx_loop(self.mlx_ptr)
