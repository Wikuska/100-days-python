from turtle import Screen
from paddle import Paddle

screen = Screen()
screen.title("Brakeout Game")
screen.bgcolor("black")
screen.setup(width = 800, height = 600)
paddle = Paddle()
screen.listen()
screen.onkeypress(paddle.go_left, "Left")
screen.onkeypress(paddle.go_right, "Right")
screen.mainloop()
