import random


class Colour:
    def __init__(self, name: str) -> None:
        # format: 0xAARRGGBB
        preset = {
            "black":  0xFF000000,
            "white":  0xFFFFFFFF,
            "blue":   0xFF0000FF,
            "red":    0xFFFF0000,
            "green":  0xFF00FF00,
            "yellow": 0xFFFFFF00,
            "purple": 0xFF800080,
            "mustard": 0xFFDBB72D,
        }
        self.value = preset.get(name, self.get_random_colour())

    def get_random_colour(self):
        r = random.randint(100, 255)
        g = random.randint(100, 255)
        b = random.randint(100, 255)

        return (0xFF << 24) | (r << 16) | (g << 8) | b
