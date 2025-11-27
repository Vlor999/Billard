from src.objects.objects import created_object
import numpy as np

class BillardModel():
    def __init__(self, objects: list[created_object]) -> None:
        self.objects = objects
        self.count = 0
        self.matrix = np.zeros(shape=(300, 300, 3), dtype=np.uint8)
        pass

    def render_matrix(self):
        self.count += 1
        self.matrix =  (self.matrix + 1) % 255
        return self.matrix