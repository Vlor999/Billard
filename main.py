from src.GUI.display import UI
from src.objects.model import BillardModel
from src.objects.circle import Circle

def main():
    objects = [Circle(100, 100, 10), Circle(200, 200, 30), Circle(250, 100, 12), Circle(234, 120, 6)]
    model = BillardModel(objects)
    main_ui = UI(model=model, window_name="Test")
    main_ui.display()


if __name__ == "__main__":
    main()
