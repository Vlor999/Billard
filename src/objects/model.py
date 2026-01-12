from src.objects.objects import RigidBody

import numpy as np
from typing import Sequence
from src.global_pgs import step_system
from src.objects.objects import Ball
import cv2 as cv


class BillardModel:
    def __init__(
        self,
        objects: Sequence[RigidBody],
        shape: tuple[int, int, int] = (500, 500, 3),
        box: list | None = None,
        mu: float = 0.1,
        e: float = 0.95,
        dt: float = 0.1,
        mode: str = "FR"
    ) -> None:
        self.objects = objects
        self.count = 0
        self.matrix = np.zeros(shape=shape, dtype=np.uint8)
        self.shape = shape
        self.mode = mode
        self.pocketed = []
        self.player_colors = {0: (0, 165, 255), 1: (0, 0, 255)}  # orange, red

        # Physics parameters
        self.box = (
            box if box else [0, shape[1], 0, shape[0]]
        )
        self.matrix[self.box[0] : self.box[1], self.box[2] : self.box[3], 0] = 43
        self.matrix[self.box[0] : self.box[1], self.box[2] : self.box[3], 1] = 64
        self.matrix[self.box[0] : self.box[1], self.box[2] : self.box[3], 2] = 6
        ymin, ymax, xmin, xmax = self.box
        self.pockets = [
            (xmin, ymin),  # top-left
            (xmax, ymin),  # top-right
            (xmin, ymax),  # bottom-left
            (xmax, ymax),  # bottom-right
            ((xmin + xmax) // 2, ymin),  # top-mid
            ((xmin + xmax) // 2, ymax),  # bottom-mid
        ] 
        if self.mode == "US":
            for pocket in self.pockets:
                cv.circle(self.matrix, pocket, 20, (255, 255, 255), -1)
        self.mu = mu  # friction coefficient
        self.e = e  # restitution
        self.dt = dt  # time step

        # Extract Ball objects from RigidBody wrappers
        self.balls: list[Ball] = [obj.ball for obj in objects]

    def update(self):
        """Update simulation step using global_pgs physics"""
        self.count += 1

        # Step the physics simulation
        step_system(self.balls, self.box, self.mu, self.e, self.dt)

        # Check for pocketed balls (only in US mode)
        if self.mode == "US":
            to_remove = []
            for i, ball in enumerate(self.balls):
                # Don't remove the white ball (index 0)
                if i == 0:
                    continue
                x, y = ball.q[0], ball.q[1]
                for pocket in self.pockets:
                    px, py = pocket
                    if (y - px)**2 + (x - py)**2 <= 1000:
                        print(f"Ball pocketed: {self.objects[i].name}, color: {self.objects[i].color}")
                        self.pocketed.append(self.objects[i])
                        to_remove.append(i)
                        break
            # Remove pocketed balls from lists
            for i in reversed(to_remove):
                if self.objects[i].color == (0,0,0):
                    print("The black ball enter - loose")
                if self.objects[i].color == (255,255,255):
                    self.objects[i].x = 200
                    self.objects[i].y = 750
                    print("white")
                    continue
                del self.objects[i]
                del self.balls[i]

        # Clear the matrix before redrawing all objects
        self.matrix.fill(0)
        self.matrix[self.box[0] : self.box[1], self.box[2] : self.box[3], 0] = 43
        self.matrix[self.box[0] : self.box[1], self.box[2] : self.box[3], 1] = 64
        self.matrix[self.box[0] : self.box[1], self.box[2] : self.box[3], 2] = 6
        if self.mode == "US":
            for pocket in self.pockets:
                cv.circle(self.matrix, pocket, 20, (255, 255, 255), -1)
        for ob in self.objects:
            ob.update(self.matrix)

    def is_moving(self) -> bool:
        """Check if any object is moving"""
        for obj in self.objects:
            if obj.is_moving():
                return True
        return False

    def collisions(self) -> list[tuple[int, int]]:
        """Detect all collisions between all pairs of balls using global_pgs logic."""
        col = []
        n = len(self.balls)
        for i in range(n):
            for j in range(i + 1, n):
                ball1 = self.balls[i]
                ball2 = self.balls[j]
                x1, y1, r1 = ball1.q[0], ball1.q[1], ball1.R
                x2, y2, r2 = ball2.q[0], ball2.q[1], ball2.R
                dist = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                if dist <= r1 + r2:
                    print(
                        f"Collision detected: {self.objects[i].name} <-> {self.objects[j].name} (dist={dist:.2f}, r1+r2={r1 + r2})"
                    )
                    col.append((self.objects[i], self.objects[j]))
        return col
