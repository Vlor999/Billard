from src.GUI.display import display
from src.objects.model import BillardModel
from src.objects.circle import Circle

def main():
    objects = [Circle(100, 100, 10), Circle(200, 200, 30)]
    model = BillardModel(objects)
    display(model=model, window_name="Test", delay=10)


if __name__ == "__main__":
    main()
