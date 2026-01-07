import abc
import numpy as np
from typing import Callable
from random import randint
from global_pgs import Ball

global count
count = 0

class RigidBody:
    def __init__(self, x0: int, y0: int, density: Callable | None = None, name: str | None = None, mass: float = 1.0, radius: float = 10.0, omega: float = 0.0, image_path: str | None = None) -> None:
        global count
        count += 1
        self.radius = radius
        self.mass = mass
        # Create underlying Ball object from global_pgs
        self.ball = Ball(x=float(x0), y=float(y0), vx=0.0, vy=0.0, omega=omega, m=mass, R=radius, image_path=image_path)
        self.density = density
        self.name = name if name is not None else f"Elem_{count}"

    @property
    def x(self) -> float:
        return self.ball.q[0]
    
    @x.setter
    def x(self, value: float) -> None:
        self.ball.q[0] = value
    
    @property
    def y(self) -> float:
        return self.ball.q[1]
    
    @y.setter
    def y(self, value: float) -> None:
        self.ball.q[1] = value
    
    @property
    def velocity(self) -> np.ndarray:
        return self.ball.v
    
    @velocity.setter
    def velocity(self, value: np.ndarray) -> None:
        self.ball.v = value
    
    @property
    def force(self) -> np.ndarray:
        # For compatibility with old interface
        return np.zeros(2)
    
    @force.setter
    def force(self, value: np.ndarray) -> None:
        # Apply force as acceleration
        if np.linalg.norm(value) > 1e-6:
            self.ball.v += value / self.mass

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def collision(self, obj2: 'RigidBody') -> bool:
        return False
    
    @classmethod
    def handle_collision(cls, obj1: 'RigidBody', obj2: 'RigidBody') -> None:
        # Handled by global_pgs contact solver
        return
    
    def apply_force_from_position(self, mouse_x: int, mouse_y: int, strength_factor: float = 0.1) -> None:
        dx = self.y - mouse_x
        dy = self.x - mouse_y
        
        distance = np.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            force_magnitude = strength_factor * distance
            force = np.array([dy / distance * force_magnitude, dx / distance * force_magnitude])
            self.ball.v += force / self.mass
    
    @abc.abstractmethod
    def update(self, matrix) -> None:
        return
    
    @classmethod
    def create_color(cls) -> tuple[int,int,int]:
        return (randint(0,255), randint(0,255), randint(0, 255))
    
    def is_moving(self) -> bool:
        return bool(np.linalg.norm(self.ball.v) > 0.01)

