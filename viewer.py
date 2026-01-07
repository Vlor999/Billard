import pygame
from global_pgs import Ball, detect_contacts, step_system, project_positions
import numpy as np

# Initialize Pygame and set up the display
pygame.init()
screen = pygame.display.set_mode((640, 480)) #(xmax,ymax)
clock = pygame.time.Clock()

ball_A = Ball(
    x=0, 
    y=400,
    vx= 50, 
    vy=50,
    omega=30.0,
    m=40, 
    R=20,
    image_path="tennis-ball.png"
)
ball_B = Ball(
    x=460,
    y=50,
    vx=10, 
    vy=100,
    omega=0.0,
    m=10, 
    R=50,
    image_path="tennis-ball.png"
)
ball_C = Ball(
    x=120,
    y=400,
    vx=-50, 
    vy=-50,
    omega=20,
    m=100, 
    R=50,
    image_path="tennis-ball.png"
)
balls = [ball_A]

nbr_balls = 10
balls = []
for _ in range(nbr_balls):
    x=np.random.randint(0,480)
    y=np.random.randint(0,640)
    vx=np.random.randint(-20,20)
    vy=np.random.randint(-20,20)
    omega=np.random.randint(-20,20)
    R=np.random.randint(1,50)
    image_path="tennis-ball.png"
    m=np.pi * R ** 2
    b = Ball(
        x=x,
        y=y,
        vx=vx,
        vy=vy,
        omega=omega,
        m=m,
        R=R,
        image_path=image_path
        )
    balls.append(b)
box = [0,640,0,480] # [xmin, xmax, ymin, ymax]
dt = 1e-1
mu = 0.1
e = 0.95   # restitution
original_image = pygame.image.load("tennis-ball.png")

# Run the game loop
running = True
while running:
    # Handle user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    contacts = detect_contacts(balls, box, mu, e)
    # print("contacts=",contacts)
    step_system(balls, box, mu, e, dt)
    
    screen.fill((0,0,0))
    for ball in balls:
        # Draw the ball and update the display
        circle = pygame.draw.circle(screen, (255, 255, 255), (ball.q[0], ball.q[1]), ball.R)
        # image = pygame.transform.rotate(ball.image, ball.theta)
        # screen.blit(image, ball.q)
    pygame.display.flip()
    clock.tick(60)
    
# Quit Pygame when the game loop is finished
pygame.quit()