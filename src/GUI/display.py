from loguru import logger
import cv2 as cv
from src.objects.model import BillardModel

def display(model: BillardModel, window_name:str, delay: int= 20) -> None:
    model.update()
    cv.namedWindow(winname=window_name)
    cv.imshow(winname=window_name, mat=model.matrix)
    while True:
        key = cv.waitKey(delay=delay)
        if key == ord("q"):
            break
        model.update()
        cv.imshow(winname=window_name, mat=model.matrix)
    cv.destroyWindow(window_name)
