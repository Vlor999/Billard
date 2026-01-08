from src.GUI.display import UI
from src.objects.model import BillardModel
from src.objects.circle import Circle

def main():
    """Launch the billard simulation using global_pgs physics engine"""
    # Create circles for the simulation
    NL = 1000
    NC = 500
    objects = [
        Circle(250, 300, 20, 0., (255, 255, 255)), 
        Circle(150, 700, 20, 0., (0, 165, 255)), 
        Circle(350, 700, 20, 0., (0, 0, 255)),
    ]
    
    # Create the model with global_pgs physics parameters

    lateral_step = 150
    horizontal_step = 100

    model = BillardModel(
        objects,
        shape=(NC, NL, 3),
        box=[horizontal_step, NC - horizontal_step, lateral_step, NL - lateral_step],  # [xmin, xmax, ymin, ymax]
        mu=0.1,     # friction coefficient
        e=0.95,     # restitution
        dt=0.1      # time step
    )
    
    # Launch the UI
    main_ui = UI(model=model, window_name="Billard Simulation")
    main_ui.display()


if __name__ == "__main__":
    main()
