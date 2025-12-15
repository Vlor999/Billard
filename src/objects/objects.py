import abc
import numpy as np
from typing import Callable
from random import randint

global count
count = 0
class RigidBody:
    def __init__(self, x0: int, y0: int, parametric_repr: Callable | None = None, density: Callable | None = None, name: str | None = None) -> None:
        global count
        count += 1
        self.x = x0
        self.y = y0
        self.parametric_repr = parametric_repr
        self.density = density
        self.force = np.zeros(shape=(2,), dtype=np.float64)
        self.name = name if name is not None else f"Elem_{count}"

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def collision(self, obj2: 'RigidBody') -> bool:
        return False
    
    @classmethod
    def handle_collision(cls, obj1: 'RigidBody', obj2: 'RigidBody') -> None:
        #TODO
        return
    
    def apply_force_from_position(self, mouse_x: int, mouse_y: int, strength_factor: float = 0.1) -> None:
        """Apply force based on distance and direction from mouse to object.
        
        Args:
            mouse_x: Mouse x position (column)
            mouse_y: Mouse y position (row)
            strength_factor: Multiplier for force magnitude
        """
        dx = self.y - mouse_x
        dy = self.x - mouse_y
        
        distance = np.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            force_magnitude = strength_factor * distance
            self.force[0] = (dx / distance) * force_magnitude
            self.force[1] = (dy / distance) * force_magnitude
    
    @abc.abstractmethod
    def update(self, matrix) -> None:
        return
    
    @classmethod
    def create_color(cls) -> tuple[int,int,int]:
        return (randint(0,255), randint(0,255), randint(0, 255))

