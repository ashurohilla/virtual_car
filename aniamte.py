import turtle
import math

# Set up the screen
screen = turtle.Screen()
screen.bgcolor("lightgray")
screen.title("Car Animation")

# Create the car turtle
car = turtle.Turtle()
car.shape("square")
car.color("red")
car.shapesize(stretch_wid=4, stretch_len=5)  # Adjust the car's dimensions

# Define the initial position and orientation
x, y = 0, 0
angle = 0

# Function to move the car
def move_car(dx, dy, dangle):
    global x, y, angle
    x += dx
    y += dy
    angle += dangle
    car.goto(x, y)
    car.setheading(angle)

# Example frames (you can provide your own dx, dy, dangle values)
frames = [
    (0, 0, 0), (2, 2, 10), (4, 0, 0), (2, -2, -10),
]

# Animation loop
for dx, dy, dangle in frames:
    move_car(dx, dy, dangle)

# Keep the window open until it's closed
turtle.done()