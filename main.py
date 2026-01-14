from src.GUI.display import UI
from src.objects.model import BillardModel
from src.objects.circle import Circle
from argparse import ArgumentParser

def get_arguments():
    parser = ArgumentParser(prog="Billard simulation")
    parser.add_argument("--mode", default="FR", choices=["FR", "US"], help="Choose wich model to play billard")
    return parser.parse_args()

def main():
    # Create circles for the simulation
    NL = 1000
    NC = 500
    RADIUS = 20
    args = get_arguments()
    mode = args.mode
    if mode == "FR":
        objects = [
            Circle(250, 300, RADIUS, 0., (255, 255, 255)), 
            Circle(150, 700, RADIUS, 0., (0, 165, 255)), 
            Circle(350, 700, RADIUS, 0., (0, 0, 255)),
        ]
    else:
        objects = [
            Circle(250, 300, RADIUS, 0., (255, 255, 255)), # White

            Circle(250, 690, RADIUS, 0., (0, 0, 255)), # Red

            Circle(230, 725, RADIUS, 0., (0, 165, 255)), # Orange
            Circle(270, 725, RADIUS, 0., (0, 0, 255)), # Red

            Circle(210, 760, RADIUS, 0., (0, 165, 255)), # Orange
            Circle(250, 760, RADIUS, 0., (0, 0, 0)), # Black
            Circle(290, 760, RADIUS, 0., (0, 165, 255)), # Orange

            Circle(190, 795, RADIUS, 0., (0, 0, 255)), # Red
            Circle(230, 795, RADIUS, 0., (0, 165, 255)), # Orange
            Circle(270, 795, RADIUS, 0., (0, 0, 255)), # Red
            Circle(310, 795, RADIUS, 0., (0, 165, 255)), # Orange

            Circle(170, 840, RADIUS, 0., (0, 165, 255)), # Orange
            Circle(210, 840, RADIUS, 0., (0, 0, 255)), # Red
            Circle(250, 840, RADIUS, 0., (0, 165, 255)), # Orange
            Circle(290, 840, RADIUS, 0., (0, 0, 255)), # Red
            Circle(330, 840, RADIUS, 0., (0, 165, 255)), # Orange
        ]

    lateral_step = 150
    horizontal_step = 100

    model = BillardModel(
        objects,
        shape=(NC, NL, 3),
        box=[horizontal_step, NC - horizontal_step, lateral_step, NL - lateral_step],  # [xmin, xmax, ymin, ymax]
        mu=0.1,     # friction coefficient
        e=0.95,     # restitution
        dt=0.1,      # time step
        mode=mode
    )
    
    # Launch the UI
    main_ui = UI(model=model, window_name="Billard Simulation")
    main_ui.display()


if __name__ == "__main__":
    main()
