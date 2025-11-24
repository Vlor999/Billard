import numpy as np
from typing import Callable

class object:
    def __init__(self, x0: int, y0: int, parametric_repr: Callable, density: Callable) -> None:
        self.x = x0
        self.y = y0
        self.parametric_repr = parametric_repr
        self.density = density
        self.force = np.zeros(shape=(2,2), dtype=np.float64)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def collision(self, obj2: 'object'):
        return bool
    
    @classmethod
    def handle_collision(cls, obj1: 'object', obj2: 'object') -> None:
        #TODO
        return

