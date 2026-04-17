from mlx import Mlx

mlx = Mlx()
mlx_ptr = mlx.mlx_init()

window = mlx.mlx_new_window(mlx_ptr, 1200, 1200, "test")

image_length = 300
cell_length = 100
stroke_length = 20

# format: 0xAARRGGBB
black = 0x00FFFFFF
white = 0xFFFFFFFF
green = 0xFF00FF00


image = mlx.mlx_new_image(
            mlx_ptr,
            image_length,
            image_length
        )

# Use an image buffer
data, bpp, sl, fmt = mlx.mlx_get_data_addr(image)


def _put_pixel(data, sl, x, y, color):
    index = y * sl + x * 4  # 4 bytes per pixel

    data[index + 0] = (color >> 0) & 0xFF   # Blue
    data[index + 1] = (color >> 8) & 0xFF   # Green
    data[index + 2] = (color >> 16) & 0xFF  # Red
    data[index + 3] = (color >> 24) & 0xFF  # Alpha


def colour_cell(colour: str,
                start_x: int, start_y: int,
                x_length: int, y_length: int) -> None:
    for i in range(x_length):
        for j in range(y_length):
            _put_pixel(data, sl, start_x + i, start_y + j, colour)


def draw_interior_of_cell(colour: str) -> None:
    colour_cell(colour, stroke_length, stroke_length, cell_length - 2 * stroke_length, cell_length - 2 * stroke_length)

def draw_side_of_cell(colour: str, direction: str) -> None:
    # N
    if direction == "N":
        start_x = stroke_length
        start_y = 0
        colour_cell(colour, start_x, start_y, cell_length - 2 * stroke_length, stroke_length)

    # NE
    if direction == "NE":
        start_x = cell_length - stroke_length
        start_y = 0
        colour_cell(colour, start_x, start_y, stroke_length, stroke_length)

    # E
    if direction == "E":
        start_x = cell_length - stroke_length
        start_y = stroke_length
        colour_cell(colour, start_x, start_y, stroke_length, cell_length - 2 * stroke_length)

    # SE
    if direction == "SE":
        start_x = cell_length - stroke_length
        start_y = cell_length - stroke_length
        colour_cell(colour, start_x, start_y, stroke_length, stroke_length)

    # S
    if direction == "S":
        start_x = stroke_length
        start_y = cell_length - stroke_length
        colour_cell(colour, start_x, start_y, cell_length - 2 * stroke_length, stroke_length)

    # SW
    if direction == "SW":
        start_x = 0
        start_y = cell_length - stroke_length
        colour_cell(colour, start_x, start_y, stroke_length, stroke_length)

    # W
    if direction == "W":
        start_x = 0
        start_y = stroke_length
        colour_cell(colour, start_x, start_y, stroke_length, cell_length - 2 * stroke_length)

    # NW
    if direction == "NW":
        start_x = 0
        start_y = 0
        colour_cell(colour, start_x, start_y, stroke_length, stroke_length)


draw_side_of_cell(green, "N")
draw_side_of_cell(green, "E")
draw_side_of_cell(green, "S")
draw_side_of_cell(green, "W")
draw_interior_of_cell(white)


def put_to_window(image, start_x: int, start_y: int) -> None:
    mlx.mlx_put_image_to_window(
        mlx_ptr,
        window,
        image,
        start_x,
        start_y
    )


n_x = 0
n_y = 0
# top left corner
put_to_window(image, 0, 0)

n_x = 1
n_y = 0
put_to_window(image, n_x * cell_length - stroke_length, 0)

n_x = 0
n_y = 1
put_to_window(image, 0, n_y * cell_length - stroke_length)

n_x = 1
n_y = 1
put_to_window(image, n_x * cell_length - stroke_length, n_y * cell_length - stroke_length)


def close_window(_):
    mlx.mlx_loop_exit(mlx_ptr)
    return 0


# Keep the window being opened
mlx.mlx_hook(window, 33, 0, close_window, None)
mlx.mlx_loop(mlx_ptr)
