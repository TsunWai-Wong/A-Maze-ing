from typing import Any
from mlx import Mlx  # type: ignore[import-not-found]


class Image():
    def __init__(self, mlx: Mlx, mlx_ptr: Any, width: int, height: int):
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
        index = y * sl + x * 4  # 4 bytes per pixel

        data[index + 0] = (color >> 0) & 0xFF   # Blue
        data[index + 1] = (color >> 8) & 0xFF   # Green
        data[index + 2] = (color >> 16) & 0xFF  # Red
        data[index + 3] = (color >> 24) & 0xFF  # Alpha

    def draw_shape(self,
                   colour: int,
                   start_x: int, start_y: int,
                   x_length: int, y_length: int) -> None:
        for i in range(x_length):
            for j in range(y_length):
                self._put_pixel(self.data, self.sl,
                                start_x + i, start_y + j, colour)

    def put_to_window(self, window: Any, start_x: int, start_y: int) -> None:
        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr,
            window,
            self.image,
            start_x,
            start_y
        )
