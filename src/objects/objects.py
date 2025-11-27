import abc
import numpy as np
from typing import Callable
from random import randint

class created_object:
    def __init__(self, x0: int, y0: int, parametric_repr: Callable | None = None, density: Callable | None = None) -> None:
        self.x = x0
        self.y = y0
        self.parametric_repr = parametric_repr
        self.density = density
        self.force = np.zeros(shape=(2,2), dtype=np.float64)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def collision(self, obj2: 'created_object') -> bool:
        return False
    
    @classmethod
    def handle_collision(cls, obj1: 'created_object', obj2: 'created_object') -> None:
        #TODO
        return
    
    @abc.abstractmethod
    def update(self, matrix) -> None:
        return
    
    @classmethod
    def create_color(cls) -> tuple[int,int,int]:
        return (randint(0,255), randint(0,255), randint(0, 255))

