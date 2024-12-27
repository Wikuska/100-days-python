from turtle import Screen
from paddle import Paddle
from ball import Ball
from brick import Brick

bricks = []

def create_bricks():
    for row in range(6):
        for col in range(9):
            brick = Brick()
            x = -360 + col * 90
            y = 280 - row * 30
            brick.goto(x, y)
            bricks.append(brick)


screen = Screen()
screen.title("Brakeout Game")
screen.bgcolor("black")
screen.setup(width = 840, height = 600)
screen.tracer(0)

paddle = Paddle()

ball = Ball()

create_bricks()

screen.listen()
screen.onkeypress(paddle.go_left, "Left")
screen.onkeypress(paddle.go_right, "Right")

game_is_on = True
while game_is_on:
    screen.update()
    ball.move()
    # Detect collision with paddle
    if ball.ycor() > -240 and ball.ycor() < -230 and ball.distance(paddle) < 60:
        ball.y_bounce()

    # Detect collision with side wall
    if ball.xcor() > 405 or ball.xcor() < -405:
        ball.x_bounce()

    # Detect collision with top wall
    if ball.ycor() > 285:
        ball.y_bounce()
    
    # Detect collision with brick
    for brick in bricks:
        if ball.xcor() > (brick.xcor() - 40) and ball.xcor() < (brick.xcor() + 40) and ball.distance(brick) < 40:
            ball.y_bounce()
            brick.hideturtle()
            bricks.remove(brick)
        if ball.ycor() > (brick.ycor() - 10) and ball.ycor() < (brick.ycor() + 10) and ball.distance(brick) < 60:
            ball.x_bounce()
            brick.hideturtle()
            bricks.remove(brick)

    # Detect when ball miss paddle
    if ball.ycor() < -285:
        ball.reset_ball()
                        

screen.mainloop()
