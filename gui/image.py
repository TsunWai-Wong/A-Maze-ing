from typing import Any
from mlx import Mlx


class Image():
    """
    Represents an image buffer for pixel-level drawing operations.

    Wraps a low-level MLX image object and provides utilities for
    pixel manipulation and rendering to a window.

    Attributes:
    mlx (Mlx): MLX interface wrapper.
    mlx_ptr (Any): MLX context pointer.
    image (Any): MLX image object.
    data (Any): Raw image buffer data.
    bpp (int): Bits per pixel.
    sl (int): Size of one image line in bytes.
    fmt (int): Image format identifier.
    """
    def __init__(self, mlx: Mlx, mlx_ptr: Any, width: int, height: int):
        """Initialize an image buffer."""
        self.mlx = mlx
        self.mlx_ptr = mlx_ptr
        self.image = self.mlx.mlx_new_image(
            mlx_ptr,
            width,
            height
        )
        # Use an image buffer
        self.data, self.bpp, self.sl, self.fmt = (self.mlx.
                                                  mlx_get_data_addr(self.image)
                                                  )

    def _put_pixel(self, data: Any, sl: int,
                   x: int, y: int, color: int) -> None:
        """
        Draw a single pixel in the image buffer.

        Args:
        data (Any): Image buffer data.
        sl (int): Line size in bytes.
        x (int): X coordinate.
        y (int): Y coordinate.
        color (int): Color value in ARGB format.
        """
        index = y * sl + x * 4  # 4 bytes per pixel

        data[index + 0] = (color >> 0) & 0xFF   # Blue
        data[index + 1] = (color >> 8) & 0xFF   # Green
        data[index + 2] = (color >> 16) & 0xFF  # Red
        data[index + 3] = (color >> 24) & 0xFF  # Alpha

    def draw_shape(self,
                   colour: int,
                   start_x: int, start_y: int,
                   x_length: int, y_length: int) -> None:
        """
        Fills a rectangular region with a solid color.

        Args:
        colour (int): Color value.
        start_x (int): Starting X coordinate.
        start_y (int): Starting Y coordinate.
        x_length (int): Width of rectangle.
        y_length (int): Height of rectangle.
        """
        for i in range(x_length):
            for j in range(y_length):
                self._put_pixel(self.data, self.sl,
                                start_x + i, start_y + j, colour)

    def put_to_window(self, window: Any, start_x: int, start_y: int) -> None:
        """
        Render the image to a window at the
        specified position.

        Args:
        window (Any): Target window object.
        start_x (int): X position in window.
        start_y (int): Y position in window.
        """
        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr,
            window,
            self.image,
            start_x,
            start_y
        )
