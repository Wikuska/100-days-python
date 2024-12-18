from turtle import Turtle

class Brick(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.shapesize(1,4)
        self.color("white")
        self.penup()
