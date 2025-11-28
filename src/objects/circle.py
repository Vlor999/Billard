import cv2 as cv
import numpy as np
from src.objects.objects import created_object

class Circle(created_object):
    def __init__(self, x0, y0, radius, color: tuple[int, int, int] | None = None, highlight_color: tuple[int, int, int] = (255, 255, 0)):
        super().__init__(x0, y0)
        self.radius = radius
        self.color = color if color else super().create_color()
        self.highlight_color = highlight_color
        self.highlight_thickness = 3  # Thickness of the surrounding ring
        self.is_closest_object = False

    def set_closest_object(self, is_closest):
        self.is_closest_object = is_closest

    def update(self, matrix:np.ndarray) -> None:
        "In place representation"
        nl, nc, _ = matrix.shape
        outer_radius = self.radius + self.highlight_thickness
        inner_radius_sq = self.radius ** 2
        outer_radius_sq = outer_radius ** 2
        
        # Draw highlight ring first if this is the closest object
        if self.is_closest_object:
            for l in range(self.x - outer_radius, self.x + outer_radius + 1):
                for c in range(self.y - outer_radius, self.y + outer_radius + 1):
                    if 0 <= l < nl and 0 <= c < nc:
                        dist_sq = (l - self.x) ** 2 + (c - self.y) ** 2
                        # Draw ring between inner and outer radius
                        if inner_radius_sq < dist_sq <= outer_radius_sq:
                            matrix[l][c] = self.highlight_color
        
        # Draw the circle itself
        for l in range(self.x - self.radius, self.x + self.radius + 1):
            for c in range(self.y - self.radius, self.y + self.radius + 1):
                if 0 <= l < nl and 0 <= c < nc: 
                    if (l - self.x) ** 2 + (c - self.y) ** 2 <= inner_radius_sq:
                        matrix[l][c] = self.color
