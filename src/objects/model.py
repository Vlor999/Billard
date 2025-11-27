from src.objects.objects import created_object
import numpy as np

class BillardModel():
    def __init__(self, objects: list[created_object]) -> None:
        self.objects = objects
        self.count = 0
        self.matrix = np.zeros(shape=(300, 300, 3), dtype=np.uint8)

    def update(self):
        self.count += 1
        for ob in self.objects:
            ob.update(self.matrix)

    def verify_col(self):
        for obj1 in self.objects:
            for obj2 in self.objects:
                if obj1.collision(obj2):
                    created_object.handle_collision(obj1, obj2)