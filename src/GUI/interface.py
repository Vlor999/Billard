from src.objects.objects import object

def verify_col(objects: list[object]):
    for obj1 in objects:
        for obj2 in objects:
            if obj1.collision(obj2):
                object.handle_collision(obj1, obj2)