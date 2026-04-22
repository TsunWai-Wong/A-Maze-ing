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
        self.window = self.mlx.mlx_new_window(self.mlx_ptr, self.window_width, self.window_height, "maze")
        self.info_width = 300

        self.min_padding = 20

        # Canva
        self.maze_area_width = self.window_width - self.info_width
        self.maze_area_height = self.window_height
        self.canvas = Image(self.mlx, self.mlx_ptr, self.maze_area_width, self.maze_area_height)

        # Maze
        # wide rectangle
        if self.maze.width >= self.maze.height:
            available = self.maze_area_width - 2 * self.min_padding
            step = (available * 9) // (9 * self.maze.width + 1)   # ← accounts for stroke
            self.stroke_length = max(1, step // 9)
            self.cell_length = step + self.stroke_length

            real_width = self.maze.width * step + self.stroke_length
            real_height = self.maze.height * step + self.stroke_length

            self.padding_x_side = (self.maze_area_width - real_width) // 2
            self.padding_y_side = (self.maze_area_height - real_height) // 2

        # tall rectangle
        else:
            available = self.maze_area_height - 2 * self.min_padding
            step = (available * 9) // (9 * self.maze.height + 1)
            self.stroke_length = max(1, step // 9)
            self.cell_length = step + self.stroke_length

            real_width = self.maze.width * step + self.stroke_length
            real_height = self.maze.height * step + self.stroke_length

            self.padding_x_side = (self.maze_area_width - real_width) // 2
            self.padding_y_side = (self.maze_area_height - real_height) // 2

    def _draw_interior_of_cell(self, image: Image, colour: int, x0: int, y0: int) -> None:
        image.draw_shape(
            colour,
            x0 + self.stroke_length,
            y0 + self.stroke_length,
            self.cell_length - 2 * self.stroke_length,
            self.cell_length - 2 * self.stroke_length
        )

    def _draw_side_of_cell(self, image: Image, colour: int, direction: str, x0: int, y0: int) -> None:
        if direction == "N":
            image.draw_shape(colour, x0 + self.stroke_length, y0, self.cell_length - 2 * self.stroke_length, self.stroke_length)
        elif direction == "NE":
            image.draw_shape(colour, x0 + self.cell_length - self.stroke_length, y0, self.stroke_length, self.stroke_length)
        elif direction == "E":
            image.draw_shape(colour, x0 + self.cell_length - self.stroke_length, y0 + self.stroke_length, self.stroke_length, self.cell_length - 2 * self.stroke_length)
        elif direction == "SE":
            image.draw_shape(colour, x0 + self.cell_length - self.stroke_length, y0 + self.cell_length - self.stroke_length, self.stroke_length, self.stroke_length)
        elif direction == "S":
            image.draw_shape(colour, x0 + self.stroke_length, y0 + self.cell_length - self.stroke_length, self.cell_length - 2 * self.stroke_length, self.stroke_length)
        elif direction == "SW":
            image.draw_shape(colour, x0, y0 + self.cell_length - self.stroke_length, self.stroke_length, self.stroke_length)
        elif direction == "W":
            image.draw_shape(colour, x0, y0 + self.stroke_length, self.stroke_length, self.cell_length - 2 * self.stroke_length)
        elif direction == "NW":
            image.draw_shape(colour, x0, y0, self.stroke_length, self.stroke_length)

    def _close_window(self, *_):
        self.mlx.mlx_loop_exit(self.mlx_ptr)
        return 0

    def render(self, maze: Maze, path: List) -> None:
        path_position = {(cell.x, cell.y) for cell in path}
        step = self.cell_length - self.stroke_length

        # background
        # self.canvas.draw_shape(white, 0, 0, self.canvas_width, self.canvas_height)

        for i in range(maze.height):
            y0 = i * step + self.padding_y_side
            for j in range(maze.width):
                x0 = j * step + self.padding_x_side
                cell = maze.get_cell(j, i)

                # Walls
                for direction in ["NE", "SE", "SW", "NW"]:
                    self._draw_side_of_cell(self.canvas, blue, direction, x0, y0)

                for direction in cell.walls:
                    self._draw_side_of_cell(
                        self.canvas,
                        blue if cell.walls[direction] else white,
                        direction,
                        x0,
                        y0
                    )

                # interior
                self._draw_interior_of_cell(
                    self.canvas,
                    yellow if (j, i) in path_position else white,
                    x0,
                    y0
                )
        self.canvas.put_to_window(self.window, 0, 0)
        self.mlx.mlx_hook(self.window, 33, 0, self._close_window, None)
        self.mlx.mlx_loop(self.mlx_ptr)
