from turtle import Screen
import time

from paddles import Paddle
from ball import Ball
from scoreboard import Score

screen = Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("Bounce")
screen.tracer(0)

# objects
right_paddle = Paddle((375, 0))  # pass xcor position
left_paddle = Paddle((-375, 0))

ball = Ball()
score = Score()

# move paddle objects up and down
screen.listen()
screen.onkey(right_paddle.up, "Up")
screen.onkey(right_paddle.down, "Down")

screen.onkey(left_paddle.up, "a")
screen.onkey(left_paddle.down, "d")

game_on = True

while game_on:
    # time.sleep(0.2)
    time.sleep(ball.ball_speed)
    screen.update()

    ball.move()

    # detect ball collision with top or bottom wall
    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.bounce_y()

    # detect ball collision with paddles
    if ball.distance(right_paddle) < 50 and ball.xcor() > 345 or ball.distance(left_paddle) < 50 and ball.xcor() < -345:
        ball.bounce_x()

    # prevent paddles from moving off screen
    if right_paddle.ycor() >= 290:
        right_paddle.down()
    elif right_paddle.ycor() <= -290:
        right_paddle.up()

    if left_paddle.ycor() >= 290:
        left_paddle.down()
    elif left_paddle.ycor() <= -290:
        left_paddle.up()

    # detect if ball is out of bounds
    # and increase or count score
    if ball.xcor() > 380:
        # right paddles
        score.increase_left_score()
        ball.ball_reset()

    if ball.xcor() < -380:
        # left paddle
        score.increase_right_score()
        ball.ball_reset()

screen.exitonclick()
