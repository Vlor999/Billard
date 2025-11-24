import numpy as np

def parametric_cardioid(phi: float | np.ndarray, alpha: float = 1.) -> np.ndarray:
    return alpha * (1 - np.cos(phi))

def parametric_triangle(phi: float | np.ndarray, alpha: float = 1.) -> np.ndarray | float:
    # TODO
    print("TO DO")
    return phi