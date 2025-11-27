from src.GUI.display import display
from src.objects.model import BillardModel

def main():
    objects = []
    model = BillardModel(objects)
    display(model=model, window_name="Test", delay=10)


if __name__ == "__main__":
    main()
