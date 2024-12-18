from turtle import Screen
from paddle import Paddle
from bricks import Bricks

screen = Screen()
screen.title("Brakeout Game")
screen.bgcolor("black")
screen.setup(width = 840, height = 600)
screen.tracer(0)

paddle = Paddle()

brick = Bricks()
brick.bricks_setup()
screen.update()

screen.tracer(1)
screen.listen()
screen.onkeypress(paddle.go_left, "Left")
screen.onkeypress(paddle.go_right, "Right")

screen.mainloop()
