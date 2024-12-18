from turtle import *

class Paddle:
    def __init__(self):
        self.paddle = Turtle()
        self.paddle.shape("square")
        self.paddle.shapesize(1,6)
        self.paddle.color("white")
        self.paddle.penup()
        self.paddle.setheading(0)
        self.paddle.teleport(0, -250)

    def go_left(self):
        if self.paddle.xcor() > -340:
            self.paddle.backward(30)

    def go_right(self):
        if self.paddle.xcor() < 340:
            self.paddle.forward(30)
