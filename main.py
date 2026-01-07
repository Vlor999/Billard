from src.GUI.display import UI
from src.objects.model import BillardModel
from src.objects.circle import Circle

def main():
    """Launch the billard simulation using global_pgs physics engine"""
    # Create circles for the simulation
    objects = [
        Circle(100, 100, 20, (255, 255, 255)), 
        Circle(200, 200, 20, (0, 165, 255)), 
        Circle(250, 100, 20, (0, 0, 255)),
    ]
    
    # Create the model with global_pgs physics parameters
    model = BillardModel(
        objects,
        shape=(500, 500, 3),
        box=[0, 500, 0, 500],  # [xmin, xmax, ymin, ymax]
        mu=0.1,     # friction coefficient
        e=0.95,     # restitution
        dt=0.1      # time step
    )
    
    # Launch the UI
    main_ui = UI(model=model, window_name="Billard Simulation - global_pgs")
    main_ui.display()


if __name__ == "__main__":
    main()
