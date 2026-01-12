import numpy as np
from loguru import logger
import cv2 as cv
from src.objects.model import BillardModel
from typing import Any
from src.objects.circle import Circle


class UI:
    def __init__(self, model: BillardModel, window_name: str) -> None:
        self.model = model
        self.window_name = window_name
        self.mouse_pos = (0, 0)
        nl, nc, _ = self.model.matrix.shape
        self.panel = np.ones(shape=(nl, nc // 2, 3), dtype=np.uint8) * 127
        self.current_obj = 0
        self.player = [0, 0]
        self.current_player = 0
        self.omega_window_open = False
        self.temp_omega_val = 100

    def handle_mouse_events(
        self, event: int, x: int, y: int, flags: int, param: Any | None
    ) -> None:
        self.mouse_pos = (x, y)

    def draw_line_to_obj(self):
        """Draw a line between mouse position and closest ball"""
        if self.current_obj >= 0:
            objs = self.model.objects[self.current_obj]

            start_point = np.array([objs.y, objs.x])
            target_point = np.array(self.mouse_pos)

            vec = target_point - start_point
            dist = np.linalg.norm(vec)

            if dist > 100:
                vec = vec / dist * 100

            end_point = start_point + vec

            cv.line(
                self.model.matrix,
                (int(start_point[0]), int(start_point[1])),
                (int(end_point[0]), int(end_point[1])),
                (255, 0, 0),
                2,
            )

    def get_panel_informations(self):
        nl, nc, _ = self.model.matrix.shape
        self.panel = np.ones(shape=(nl, nc // 2, 3), dtype=np.uint8) * 127
        cv.putText(
            self.panel,
            f"Mouse: {self.mouse_pos}",
            (10, 25),
            cv.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
        )
        cv.putText(
            self.panel,
            "Points:",
            (10, 125),
            cv.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
        )
        cv.putText(
            self.panel,
            f"player 1: {self.player[0]}",
            (10, 145),
            cv.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
        )
        cv.putText(
            self.panel,
            f"player 2: {self.player[1]}",
            (10, 165),
            cv.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
        )
        cv.putText(
            self.panel,
            "Options:",
            (10, 185),
            cv.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
        )
        cv.putText(
            self.panel,
            "- enter: launch the ball",
            (10, 205),
            cv.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
        )
        cv.putText(
            self.panel,
            "- o: add some rotation to the ball",
            (10, 225),
            cv.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
        )
        cv.putText(
            self.panel,
            "- q: quit the simulation",
            (10, 245),
            cv.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
        )

        if self.current_obj is not None:
            objs = self.model.objects[self.current_obj]
            cv.putText(
                self.panel,
                f"Closest element: {objs.name}",
                (10, 45),
                cv.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1,
            )
            if isinstance(objs, Circle):
                cv.putText(
                    self.panel,
                    f"Radius: {objs.radius}",
                    (10, 65),
                    cv.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    1,
                )
                color = objs.color
                cv.rectangle(self.panel, (10, 75), (60, 105), color, -1)
                cv.putText(
                    self.panel,
                    "Color",
                    (70, 95),
                    cv.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    1,
                )

    def act(self, val):
        self.temp_omega_val = val

    def display(self, delay: int = 20) -> None:
        """Main display loop with physics from global_pgs"""
        cv.namedWindow(winname=self.window_name)
        cv.setMouseCallback(
            window_name=self.window_name, on_mouse=self.handle_mouse_events
        )
        hitted_balls: set[int] = set()
        was_moving = False
        ball_felt = 0

        while True:
            key = cv.waitKey(delay=delay)
            if key == ord("q"):
                break
            if key == ord("o"):
                self.omega_window_open = True
                cv.namedWindow("Omega", cv.WINDOW_NORMAL)
                cv.resizeWindow("Omega", 400, 50)
                cv.moveWindow("Omega", 500, 500)
                current_omega = self.model.objects[self.current_obj].ball.omega
                initial_val = int(current_omega * 100 + 100)
                self.temp_omega_val = initial_val
                cv.createTrackbar("omega", "Omega", initial_val, 200, self.act)
            elif key == 13:
                if self.omega_window_open:
                    cv.destroyWindow("Omega")
                    self.omega_window_open = False
                elif self.current_obj is not None:
                    mouse_x, mouse_y = self.mouse_pos
                    objs = self.model.objects[self.current_obj]
                    objs.apply_force_from_position(
                        mouse_x, mouse_y, strength_factor=1.0
                    )
                    logger.info(
                        f"Force applied to {objs.name}: velocity={objs.velocity}"
                    )
                    d = (self.temp_omega_val - 100) / 200
                    omega = (
                        5
                        * np.linalg.norm(objs.velocity)
                        * d
                        / (2 * self.model.objects[self.current_obj].radius)
                    )
                    self.model.objects[self.current_obj].ball.omega = float(
                        omega * 0.5 # Correction
                    )
                    hitted_balls = set()

            self.model.update()
            moving = self.model.is_moving()

            if not moving:
                self.draw_line_to_obj()
                if was_moving:
                    if self.model.mode == "FR":
                        if len(hitted_balls) != 2:
                            self.current_obj = 1 - self.current_obj
                        else:
                            self.player[self.current_obj] += 1
                        was_moving = False
                    else:
                        pocketed_colors = [obj.color for obj in self.model.pocketed]
                        if any(color == self.model.player_colors[self.current_player] for color in pocketed_colors):
                            pass
                        else:
                            self.current_player = 1 - self.current_player
                        self.model.pocketed = []
                        was_moving = False
            else:
                was_moving = True
                collisions = self.model.collisions()
                for i, j in collisions:
                    if i == self.model.objects[self.current_obj]:
                        hitted_balls.add(j)
                    elif j == self.model.objects[self.current_obj]:
                        hitted_balls.add(i)

            self.get_panel_informations()
            combined = np.hstack([self.model.matrix, self.panel])
            cv.imshow(winname=self.window_name, mat=combined)

        cv.destroyAllWindows()
