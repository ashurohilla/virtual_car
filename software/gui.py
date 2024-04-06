from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QColor
import turtle
from PyQt5.QtWidgets import QVBoxLayout  # Correct import statement for QVBoxLayout


class CarWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()  # Use QVBoxLayout for vertical arrangement
        self.setLayout(self.layout)

        # Create the turtle screen within the QWidget
        self.screen = turtle.Screen()
        self.screen.setup(100, 100)  # Set the dimensions of the turtle screen
        self.screen.tracer(0)  # Turn off automatic updating

        # Create the turtle car
        self.car = turtle.Turtle()
        self.car.shape("square")
        self.car.color("red")
        self.car.shapesize(stretch_wid=2, stretch_len=3)

        # Add the turtle canvas to the layout
        self.layout.addWidget(self.screen.getcanvas())

    def move_car(self, dx, dy):
        self.car.penup()
        self.car.goto(self.car.xcor() + dx, self.car.ycor() + dy)
        self.car.pendown()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("IoT Car Desktop Application")
        self.setGeometry(100, 100, 800, 600)  # Initial size
        
        # Layout
        layout = QGridLayout()
        
        # Upper Left Window
        self.upper_left_label = QLabel("MPU Gyroscope Data")
        self.upper_left_label.setStyleSheet(" font-size: 20px;")
        # Create the car turtle
        layout.addWidget(self.upper_left_label, 0, 0)
    
        
        # Upper Right Window
        self.upper_right_label = QLabel("Live Video Stream")
        self.upper_right_label.setStyleSheet("background-color: lightgreen; font-size: 20px;")
        layout.addWidget(self.upper_right_label, 0, 1)
        
        # Lower Left Window
        self.lower_left_label = QLabel("Location of the Bot")
        self.lower_left_label.setStyleSheet("background-color: lightcoral; font-size: 20px;")
        layout.addWidget(self.lower_left_label, 1, 0)
        
        # Lower Right Window
        self.lower_right_label = QLabel("Speech to Text")
        self.lower_right_label.setStyleSheet("background-color: lightyellow; font-size: 20px;")
        layout.addWidget(self.lower_right_label, 1, 1)
        
        # Collapse button
        self.collapse_button = QPushButton("Collapse")
        self.collapse_button.clicked.connect(self.toggle_minimize)
        layout.addWidget(self.collapse_button, 2, 0, 1, 2)
        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        # Show the main window in full screen
        self.showFullScreen()
        
    def toggle_minimize(self):
        if self.isMinimized():
            self.showNormal()
        else:
            self.showMinimized()
