from src.objects.objects import created_object

def verify_col(objects: list[created_object]):
    for obj1 in objects:
        for obj2 in objects:
            if obj1.collision(obj2):
                created_object.handle_collision(obj1, obj2)