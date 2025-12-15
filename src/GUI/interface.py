from src.objects.objects import RigidBody

def verify_col(objects: list[RigidBody]):
    for obj1 in objects:
        for obj2 in objects:
            if obj1.collision(obj2):
                RigidBody.handle_collision(obj1, obj2)