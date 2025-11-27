from loguru import logger
import cv2 as cv
from src.objects.model import BillardModel

def display(model: BillardModel, window_name:str, delay: int= 20) -> None:
    render_matrix = model.render_matrix()
    cv.namedWindow(winname=window_name)
    cv.imshow(winname=window_name, mat=render_matrix)
    while True:
        key = cv.waitKey(delay=delay)
        if key == ord("q"):
            break
        render_matrix = model.render_matrix()
        cv.imshow(winname=window_name, mat=render_matrix)
    cv.destroyWindow(window_name)
