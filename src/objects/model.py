from src.objects.objects import RigidBody
import numpy as np
from typing import Sequence

class BillardModel():
    def __init__(self, objects: Sequence[RigidBody], shape: tuple[int, int, int]=(500, 500, 3)) -> None:
        self.objects = objects
        self.count = 0
        self.matrix = np.zeros(shape=shape, dtype=np.uint8)
        self.shape = shape

    def update(self):
        self.count += 1
        # Clear the matrix before redrawing all objects
        self.matrix.fill(0)
        for ob in self.objects:
            ob.update(self.matrix)

    def verify_col(self):
        for obj1 in self.objects:
            for obj2 in self.objects:
                if obj1.collision(obj2):
                    RigidBody.handle_collision(obj1, obj2)