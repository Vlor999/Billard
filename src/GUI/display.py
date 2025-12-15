import numpy as np
from loguru import logger
import cv2 as cv
from src.objects.model import BillardModel
from typing import Any
from src.objects.circle import Circle

class UI():
    def __init__(self, model: BillardModel, window_name: str) -> None:
        self.model = model
        self.window_name = window_name
        self.mouse_pos = (0, 0)
        nl, nc, _ = self.model.matrix.shape
        self.panel = np.ones(shape=(nl, nc // 2, 3), dtype=np.uint8) * 127
        self.closest_ball = None

    def handle_mouse_events(self, event: int,x: int,y: int, flags: int, param: Any | None) -> None:
        self.mouse_pos = (x, y)
        min_dist = float("inf")
        new_closest = None
        for elem in self.model.objects:
            dist = (x - elem.y) ** 2 + (y - elem.x) ** 2
            if dist < min_dist:
                min_dist = dist
                new_closest = elem
        
        if new_closest != self.closest_ball:
            if self.closest_ball is not None and isinstance(self.closest_ball, Circle):
                self.closest_ball.set_closest_object(False)
            if new_closest is not None and isinstance(new_closest, Circle):
                new_closest.set_closest_object(True)
            self.closest_ball = new_closest

    def draw_line_to_closest(self):
        """Draw a line between mouse position and closest ball"""
        if self.closest_ball:
            cv.line(self.model.matrix, (self.closest_ball.y, self.closest_ball.x), self.mouse_pos, (255, 0, 0), 2)

    def get_panel_informations(self):
        nl, nc, _ = self.model.matrix.shape
        self.panel = np.ones(shape=(nl, nc // 2, 3), dtype=np.uint8) * 127
        cv.putText(self.panel, f"Mouse: {self.mouse_pos}", (10, 25), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        if self.closest_ball is not None:
            cv.putText(self.panel, f"Closest element: {self.closest_ball.name}", (10, 45), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            if isinstance(self.closest_ball, Circle):
                cv.putText(self.panel, f"Radius: {self.closest_ball.radius}", (10, 65), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                color = self.closest_ball.color
                cv.rectangle(self.panel, (10, 75), (60, 105), color, -1)
                cv.putText(self.panel, f"Color", (70, 95), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    def get_main_panel(self):
        pass
            

    def display(self, delay: int= 20) -> None:
        self.model.update()
        cv.namedWindow(winname=self.window_name)
        cv.setMouseCallback(window_name=self.window_name, on_mouse=self.handle_mouse_events)
        while True:
            key = cv.waitKey(delay=delay)
            if key == ord("q"):
                break
            elif key == 13:
                if self.closest_ball is not None:
                    mouse_x, mouse_y = self.mouse_pos
                    self.closest_ball.apply_force_from_position(mouse_x, mouse_y, strength_factor=0.5)
                    logger.info(f"Force applied to {self.closest_ball.name}: {self.closest_ball.force}")
            
            self.model.update()
            self.draw_line_to_closest()
            self.get_main_panel()
            self.get_panel_informations()
            combined = np.hstack([self.model.matrix, self.panel])
            cv.imshow(winname=self.window_name, mat=combined)
        cv.destroyAllWindows()
