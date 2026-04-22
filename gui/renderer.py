from typing import Tuple, Set
import random
from mlx import Mlx
from gui.colour import Colour
from gui.image import Image
from config_parser import Config
from maze import Maze, HuntAndKillGenerator, Cell, add_42_pattern
from path_finder import PathFinder

# format: 0xAARRGGBB
white = 0xFFFFFFFF
green = 0xFF00FF00
blue = 0xFF0000FF
yellow = 0xFFFFFF00
black = 0x00000000


class Renderer:
    def __init__(self, config: Config, maze: Maze, path: Tuple):
        self.config = config
        self.maze = maze
        self.path = path
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
            step = (available * 9) // (9 * self.maze.width + 1)
            self.stroke_length = max(1, step // 3)
            self.cell_length = step + self.stroke_length

            real_width = self.maze.width * step + self.stroke_length
            real_height = self.maze.height * step + self.stroke_length

            self.padding_x_side = (self.maze_area_width - real_width) // 2
            self.padding_y_side = (self.maze_area_height - real_height) // 2

        # tall rectangle
        else:
            available = self.maze_area_height - 2 * self.min_padding
            step = (available * 9) // (9 * self.maze.height + 1)
            self.stroke_length = max(1, step // 3)
            self.cell_length = step + self.stroke_length

            real_width = self.maze.width * step + self.stroke_length
            real_height = self.maze.height * step + self.stroke_length

            self.padding_x_side = (self.maze_area_width - real_width) // 2
            self.padding_y_side = (self.maze_area_height - real_height) // 2

        # colour
        self.bg_colour = Colour("black").value
        self.wall_colour = Colour("blue").value
        self.entry_colour = Colour("red").value
        self.exit_colour = Colour("green").value
        self.path_colour = Colour("mustard").value
        self.protect_colour = Colour("purple").value
        self.interior_colour = Colour("black").value

        # To show the path or not
        self.show_path = True

    def _get_interior_colour(self, cur_position: Tuple[int, int], path_positions: Set[Tuple]):
        if cur_position == self.config.entry:
            return self.entry_colour
        elif cur_position == self.config.exit:
            return self.exit_colour
        elif cur_position in path_positions and self.show_path:
            return self.path_colour
        elif self.maze.get_cell(*cur_position).is_pattern:
            return self.protect_colour
        else:
            return self.interior_colour

    def _get_wall_colour(self, cell: Cell, direction: str):
        if self.show_path:
            if cell in self.path[0] and (cell.x, cell.y) != self.config.exit and direction == self.path[1][self.path[0].index(cell)]:
                return self.path_colour
            # Extra check for path wall since some path walls are overwritten
            elif cell in self.path[0] and (cell.x, cell.y) != self.config.entry:
                prev_cell = self.path[0].index(cell) - 1
                prev_direction = self.path[1][prev_cell]
                if prev_direction == "S" and direction == "N":
                    return self.path_colour
                if prev_direction == "E" and direction == "W":
                    return self.path_colour
        if cell.walls[direction]:
            return self.wall_colour
        else:
            return self.interior_colour

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

    def _on_key(self, keycode, *_):
        ESC_KEY = 65307  # X11 Escape key

        if keycode == ESC_KEY:
            self._close_window()
        elif keycode == 112:  # P
            self.show_path = not self.show_path
            self.render()
        elif keycode == 114:  # R
            seed = random.randint(1, 500)
            self.maze = Maze(self.maze.width, self.maze.height)
            add_42_pattern(self.maze)
            generator = HuntAndKillGenerator(seed)
            generator.generate(self.maze)
            entry_cell = self.maze.get_cell(*self.config.entry)
            exit_cell = self.maze.get_cell(*self.config.exit)
            self.path = PathFinder(self.maze).find_path(entry_cell, exit_cell)
            self.render()
        elif keycode == 99:   # C
            print("C pressed")

        return 0

    def render(self) -> None:
        path_positions = {(cell.x, cell.y) for cell in self.path[0]}
        step = self.cell_length - self.stroke_length

        # background
        self.canvas.draw_shape(self.bg_colour, 0, 0, self.maze_area_width, self.maze_area_height)

        for i in range(self.maze.height):
            y0 = i * step + self.padding_y_side
            for j in range(self.maze.width):
                x0 = j * step + self.padding_x_side
                cell = self.maze.get_cell(j, i)

                # Walls
                for direction in ["NE", "SE", "SW", "NW"]:
                    self._draw_side_of_cell(self.canvas, self.wall_colour, direction, x0, y0)

                for direction in cell.walls:
                    self._draw_side_of_cell(
                        self.canvas,
                        self._get_wall_colour(cell, direction),
                        direction,
                        x0,
                        y0
                    )

                # interior
                self._draw_interior_of_cell(
                    self.canvas,
                    self._get_interior_colour((j, i), path_positions),
                    x0,
                    y0
                )
        self.canvas.put_to_window(self.window, 0, 0)
        # Handle cross button of the window
        self.mlx.mlx_hook(self.window, 33, 0, self._close_window, None)
        # Handle keyboard events
        self.mlx.mlx_hook(self.window, 2, 1 << 0, self._on_key, None)
        self.mlx.mlx_loop(self.mlx_ptr)
