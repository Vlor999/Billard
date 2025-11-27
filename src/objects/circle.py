import cv2 as cv
import numpy as np
from src.objects.objects import created_object

class Circle(created_object):
    def __init__(self, x0, y0, radius, color: tuple[int, int, int] | None = None):
        super().__init__(x0, y0)
        self.radius = radius
        self.color = color if color else super().create_color()

    def update(self, matrix:np.ndarray) -> None:
        "In place representation"
        nl, nc, _ = matrix.shape
        for l in range(self.x - self.radius, self.x + self.radius + 1):
            for c in range(self.y - self.radius, self.y + self.radius + 1):
                if 0 <= l < nl and 0 <= c < nc: 
                    if (l - self.x) ** 2 + (c - self.y) ** 2 <= self.radius ** 2:
                        matrix[l][c] = self.color
