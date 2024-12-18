from turtle import *

class Bricks:
    def __init__(self):
        self.bricks_list = []
        self.start_x = -360
        self.start_y = 280
        self.row_spacing = 50
        self.column_spacing = 90

    def bricks_setup(self):
        for row in range(6):
            for col in range(9):
                brick = Turtle()
                brick.shape("square")
                brick.shapesize(1,4)
                brick.color("white")
                brick.penup()

                x = self.start_x + col * self.column_spacing
                y = self.start_y - row * self.row_spacing
                brick.goto(x, y)
                self.bricks_list.append(brick)

