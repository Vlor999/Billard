import cv2 as cv
from src.objects.objects import RigidBody
import numpy as np

class Circle(RigidBody):
    def __init__(
        self,
        x0: int,
        y0: int,
        radius: int | float,
        omega: float,
        color: tuple[int, int, int] | None = None,
        highlight_color: tuple[int, int, int] = (255, 255, 0),
        image_path: str | None = None,
    ):
        super().__init__(x0, y0, radius=radius, image_path=image_path, omega=omega)
        self.color = color if color else super().create_color()
        self.highlight_color = highlight_color
        self.highlight_thickness = 3
        self.is_played_object = False
        self.image_path = image_path
        self.omega = omega

        self.image = None
        if self.image_path:
            im = cv.imread(self.image_path)
            if im is not None:
                d = int(2 * self.radius)
                self.image = cv.resize(im, (d, d))

    def update(self, matrix: np.ndarray) -> None:
        "In place representation - physics is handled by BillardModel.step()"
        nl, nc, _ = matrix.shape

        x_int = int(self.x)
        y_int = int(self.y)
        r = int(self.radius)

        if self.image is not None:
            # Angle in degrees for OpenCV
            angle_deg = np.degrees(self.ball.theta)
            
            d = self.image.shape[0]
            center = (d // 2, d // 2)
            M = cv.getRotationMatrix2D(center, angle_deg, 1.0)
            rotated_img = cv.warpAffine(self.image, M, (d, d))
            
            # Mask
            mask = np.zeros((d, d), dtype=np.uint8)
            cv.circle(mask, center, r, 255, -1)

            # ROI
            r1, c1 = x_int - r, y_int - r
            r2, c2 = r1 + d, c1 + d

            # Clip
            r1_c, c1_c = max(0, r1), max(0, c1)
            r2_c, c2_c = min(nl, r2), min(nc, c2)

            if r1_c < r2_c and c1_c < c2_c:
                img_r1, img_c1 = r1_c - r1, c1_c - c1
                img_r2, img_c2 = img_r1 + (r2_c - r1_c), img_c1 + (c2_c - c1_c)

                img_slice = rotated_img[img_r1:img_r2, img_c1:img_c2]
                mask_slice = mask[img_r1:img_r2, img_c1:img_c2]
                bg_slice = matrix[r1_c:r2_c, c1_c:c2_c]

                mask_bool = mask_slice > 0
                bg_slice[mask_bool] = img_slice[mask_bool]

        else:
            # Draw color circle
            cv.circle(matrix, (y_int, x_int), r, self.color, -1)
            
            # Draw orientation line
            angle = self.ball.theta
            end_col = int(y_int + r * np.cos(angle))
            end_row = int(x_int + r * np.sin(angle))
            
            line_color = tuple(max(0, c - 50) for c in self.color)
            cv.line(matrix, (y_int, x_int), (end_col, end_row), line_color, 2)

