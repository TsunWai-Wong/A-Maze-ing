from typing import Tuple, Set, TypedDict, List, Any
import random
from mlx import Mlx  # type: ignore[import-not-found]
from gui.image import Image
from config_parser import Config
from maze import Maze, HuntAndKillGenerator, Cell, add_42_pattern
from path_finder import PathFinder


class Palette(TypedDict):
    name: str
    bg: int
    wall: int
    entry: int
    exit: int
    path: int
    pattern: int
    interior: int


# format: 0xAARRGGBB
PALETTES: List[Palette] = [
    {
        "name":     "Moonlit Paper",
        "bg":       0xFF2E3440,   # Dark Charcoal
        "wall":     0xFF1C1C2E,   # Dark Ink
        "entry":    0xFF2D7A3A,   # Forest Green
        "exit":     0xFF6B2FA0,   # Royal Purple
        "path":     0xFF2255DD,   # Deep Cobalt
        "pattern":  0xFFC0391B,   # Burnt Sienna
        "interior": 0xFFF0ECE2,   # Warm Linen
    },
    {
        "name":     "Tokyo Night",
        "bg":       0xFF1A1B2E,   # Deep Navy
        "wall":     0xFFC3C7E8,   # Soft Lavender
        "entry":    0xFF39FF14,   # Neon Green
        "exit":     0xFFFF6B35,   # Vivid Orange
        "path":     0xFF00D4FF,   # Electric Cyan
        "pattern":  0xFFFF2D78,   # Hot Magenta
        "interior": 0xFF1A1B2E,   # same as bg
    },
    {
        "name":     "Synthwave Sunset",
        "bg":       0xFF16001E,   # Dark Plum
        "wall":     0xFFD4B8E0,   # Pale Violet
        "entry":    0xFF00FFE1,   # Sky Cyan
        "exit":     0xFFFF00AA,   # Vivid Pink
        "path":     0xFFF9F002,   # Neon Yellow
        "pattern":  0xFFFF4F58,   # Deep Coral
        "interior": 0xFF16001E,   # same as bg
    },
    {
        "name":     "Nordic Forest",
        "bg":       0xFF2E3440,   # Dark Charcoal
        "wall":     0xFFECEFF4,   # Frost White
        "entry":    0xFFEBCB8B,   # Soft Gold
        "exit":     0xFFBF616A,   # Muted Rose
        "path":     0xFFA3BE8C,   # Aurora Green
        "pattern":  0xFF88C0D0,   # Glacier Blue
        "interior": 0xFF2E3440,   # same as bg
    },
]


class Renderer:
    def __init__(self, config: Config, maze: Maze,
                 path: Tuple[List[Cell], List[str]]):
        self.config = config
        self.maze = maze
        self.path = path
        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()

        self.window_width = 1200
        self.window_height = 900
        self.window = self.mlx.mlx_new_window(
            self.mlx_ptr,
            self.window_width,
            self.window_height,
            "Behold! The MAZE!"
        )
        self.info_width = 300

        self.min_padding = 20

        # Canva
        self.maze_area_width = self.window_width - self.info_width
        self.maze_area_height = self.window_height
        self.canvas = Image(
            self.mlx,
            self.mlx_ptr,
            self.maze_area_width,
            self.maze_area_height
        )

        self.info_canvas = Image(
            self.mlx, self.mlx_ptr,
            self.info_width, self.window_height
        )

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

        self.palette_index = 0
        self._apply_palette()

        # To show the path or not
        self.show_path = True

    def _apply_palette(self) -> None:
        p = PALETTES[self.palette_index]
        self.bg_colour = p["bg"]
        self.wall_colour = p["wall"]
        self.entry_colour = p["entry"]
        self.exit_colour = p["exit"]
        self.path_colour = p["path"]
        self.protect_colour = p["pattern"]
        self.interior_colour = p["interior"]
        self.keyword_colour = 0xFFFFFF00
        self.text_colour = 0xFFFFFFFF

    # to wrap around when list of palettes ends
    def _cycle_palette(self) -> None:
        self.palette_index = (self.palette_index + 1) % len(PALETTES)
        self._apply_palette()

    def _draw_colour_panel(self) -> None:
        # fill panel background
        self.info_canvas.draw_shape(
            self.bg_colour, 0, 0, self.info_width, self.window_height
        )

        margin_x = 20
        margin_y = 40

        indicator_w = (self.info_width - 2 * margin_x) // len(PALETTES)
        for i, _ in enumerate(PALETTES):
            colour = 0xFFFFFFFF if i == self.palette_index else 0xFF555566
            self.info_canvas.draw_shape(
                colour,
                margin_x + i * indicator_w,
                margin_y - 20,
                indicator_w - 2,
                6
            )

        name = PALETTES[self.palette_index]["name"]
        text_x = self.maze_area_width + margin_x
        text_y = margin_y + 10
        text_colour = 0xFFFFFFFF
        self.info_canvas.put_to_window(self.window, self.maze_area_width, 0)
        self.mlx.mlx_string_put(
            self.mlx_ptr,
            self.window,
            text_x,
            text_y,
            text_colour,
            name,
        )

    def _draw_control_panel(self) -> None:
        margin_x = 20
        margin_y = 40
        text_x = self.maze_area_width + margin_x
        text_y = margin_y + 10

        controls_y = text_y + 120
        self.mlx.mlx_string_put(self.mlx_ptr, self.window, text_x, controls_y,
                                self.text_colour, "Controls")

        shortcuts = [
            ("ESC", "Exit programme"),
            ("R",   "Regenerate maze"),
            ("P",   "Show / hide path"),
            ("C",   "Change colour"),
        ]
        instruction_y = controls_y + 30
        for key, description in shortcuts:
            self.mlx.mlx_string_put(self.mlx_ptr, self.window, text_x,
                                    instruction_y, self.keyword_colour,
                                    f"[{key}]")
            self.mlx.mlx_string_put(self.mlx_ptr, self.window, text_x + 60,
                                    instruction_y, self.text_colour,
                                    description)
            instruction_y += 30

    def _get_interior_colour(
            self, cur_position: Tuple[int, int],
            path_positions: Set[Tuple[int, int]]
            ) -> int:
        cell = self.maze.get_cell(*cur_position)

        if cur_position == self.config.entry:
            return self.entry_colour
        elif cur_position == self.config.exit:
            return self.exit_colour
        elif cur_position in path_positions and self.show_path:
            return self.path_colour
        elif cell and cell.is_pattern:
            return self.protect_colour
        else:
            return self.interior_colour

    def _get_wall_colour(self, cell: Cell, direction: str) -> int:
        if self.show_path:
            if (cell in self.path[0] and
               (cell.x, cell.y) != self.config.exit and
               direction == self.path[1][self.path[0].index(cell)]):
                return self.path_colour
            # Extra check for path wall since some path walls are overwritten
            elif (cell in self.path[0] and
                  (cell.x, cell.y) != self.config.entry):
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

    def _draw_interior_of_cell(
            self, image: Image,
            colour: int, x0: int, y0: int
            ) -> None:
        image.draw_shape(
            colour,
            x0 + self.stroke_length,
            y0 + self.stroke_length,
            self.cell_length - 2 * self.stroke_length,
            self.cell_length - 2 * self.stroke_length
        )

    def _draw_side_of_cell(
            self, image: Image,
            colour: int,
            direction: str,
            x0: int,
            y0: int
            ) -> None:
        if direction == "N":
            image.draw_shape(
                colour, x0 + self.stroke_length,
                y0, self.cell_length - 2 * self.stroke_length,
                self.stroke_length
            )
        elif direction == "NE":
            image.draw_shape(
                colour,
                x0 + self.cell_length - self.stroke_length,
                y0, self.stroke_length,
                self.stroke_length
            )
        elif direction == "E":
            image.draw_shape(
                colour,
                x0 + self.cell_length - self.stroke_length,
                y0 + self.stroke_length,
                self.stroke_length,
                self.cell_length - 2 * self.stroke_length
            )
        elif direction == "SE":
            image.draw_shape(
                colour,
                x0 + self.cell_length - self.stroke_length,
                y0 + self.cell_length - self.stroke_length,
                self.stroke_length,
                self.stroke_length
            )
        elif direction == "S":
            image.draw_shape(
                colour,
                x0 + self.stroke_length,
                y0 + self.cell_length - self.stroke_length,
                self.cell_length - 2 * self.stroke_length,
                self.stroke_length
            )
        elif direction == "SW":
            image.draw_shape(
                colour,
                x0,
                y0 + self.cell_length - self.stroke_length,
                self.stroke_length,
                self.stroke_length
            )
        elif direction == "W":
            image.draw_shape(
                colour,
                x0,
                y0 + self.stroke_length,
                self.stroke_length,
                self.cell_length - 2 * self.stroke_length
            )
        elif direction == "NW":
            image.draw_shape(
                colour,
                x0,
                y0,
                self.stroke_length,
                self.stroke_length
            )

    def _close_window(self, *_: Any) -> None:
        self.mlx.mlx_loop_exit(self.mlx_ptr)

    def _on_key(self, keycode: int, *_: Any) -> None:
        ESC_KEY = 65307  # X11 Escape key

        if keycode == ESC_KEY:
            self._close_window()
        elif keycode == 112:  # P
            self.show_path = not self.show_path
            self._render()
        elif keycode == 114:  # R
            seed = random.randint(1, 500)
            self.maze = Maze(self.maze.width, self.maze.height)
            add_42_pattern(self.maze)
            generator = HuntAndKillGenerator(seed)
            generator.generate(self.maze)
            entry_cell = self.maze.get_cell(*self.config.entry)
            exit_cell = self.maze.get_cell(*self.config.exit)
            self.path = PathFinder(self.maze).find_path(entry_cell, exit_cell)
            self._render()
        elif keycode == 99:   # C
            self._cycle_palette()
            self._draw_colour_panel()
            self._draw_control_panel()
            self._render()

    def _render(self) -> None:
        path_positions = {(cell.x, cell.y) for cell in self.path[0]}
        step = self.cell_length - self.stroke_length

        # background
        self.canvas.draw_shape(
            self.bg_colour,
            0,
            0,
            self.maze_area_width,
            self.maze_area_height
        )

        for i in range(self.maze.height):
            y0 = i * step + self.padding_y_side
            for j in range(self.maze.width):
                x0 = j * step + self.padding_x_side
                cell = self.maze.get_cell(j, i)

                # Walls
                for direction in ["NE", "SE", "SW", "NW"]:
                    self._draw_side_of_cell(
                        self.canvas,
                        self.wall_colour,
                        direction,
                        x0, y0
                    )

                if cell:
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

    def run(self) -> None:
        self._draw_colour_panel()
        self._draw_control_panel()
        self._render()
        # Handle cross button of the window
        self.mlx.mlx_hook(self.window, 33, 0, self._close_window, None)
        # Handle keyboard events
        self.mlx.mlx_hook(self.window, 2, 1 << 0, self._on_key, None)
        self.mlx.mlx_loop(self.mlx_ptr)
