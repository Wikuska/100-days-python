from turtle import Turtle

class Paddle(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.shapesize(1,6)
        self.color("white")
        self.penup()
        self.setheading(0)
        self.teleport(0, -250)

    def go_left(self):
        if self.xcor() > -340:
            self.backward(30)

    def go_right(self):
        if self.xcor() < 340:
            self.forward(30)
