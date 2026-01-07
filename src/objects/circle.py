import cv2 as cv
import numpy as np
from src.objects.objects import RigidBody

class Circle(RigidBody):
    def __init__(self, x0, y0, radius, color: tuple[int, int, int] | None = None, highlight_color: tuple[int, int, int] = (255, 255, 0), image_path: str | None = None):
        super().__init__(x0, y0, radius=radius, image_path=image_path)
        self.color = color if color else super().create_color()
        self.highlight_color = highlight_color
        self.highlight_thickness = 3
        self.is_played_object = False

    def set_closest_object(self, is_closest):
        self.is_played_object = is_closest

    def update(self, matrix:np.ndarray) -> None:
        "In place representation - physics is handled by BillardModel.step()"
        nl, nc, _ = matrix.shape
        
        # Convert position to int for drawing
        x_int = int(self.x)
        y_int = int(self.y)
        
        inner_radius_sq = self.radius ** 2
                
        # Draw the circle itself
        for l in range(x_int - self.radius, x_int + self.radius + 1):
            for c in range(y_int - self.radius, y_int + self.radius + 1):
                if 0 <= l < nl and 0 <= c < nc: 
                    if (l - x_int) ** 2 + (c - y_int) ** 2 <= inner_radius_sq:
                        matrix[l][c] = self.color
