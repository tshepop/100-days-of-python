from turtle import Screen
import time

from snake import Snake
from food import Food
from scoreboard import Score


screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("Munching Snake")
screen.tracer(0)  # turn animation off

snake = Snake()
food = Food()
scoreboard = Score()

screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.right, "Right")
screen.onkey(snake.left, "Left")

game_is_on = True

while game_is_on:
    screen.update()  # update the page/screen refresh, activate animation
    time.sleep(0.2)
    snake.move()

    # detect the collision with food
    # then randomly move the food
    # when the head collides with food, increase score count
    # and the snake grows, by one segment
    if snake.snake_head.distance(food) < 14:
        food.refresh()
        snake.extend()
        scoreboard.increase_score()

    # test or detect collision with the wall
    # if there is  collision end game
    if snake.snake_head.xcor() < -290 or snake.snake_head.xcor() > 290 or snake.snake_head.ycor() < -290 or snake.snake_head.ycor() > 290:
        game_is_on = False
        scoreboard.game_over()

    # detect collision with tail
    for segment in snake.snake_body[1:]:
        # exclude first segment(head)
        # test if snake head collides with any part of the body
        #
        if snake.snake_head.distance(segment) < 10:
            game_is_on = False
            scoreboard.game_over()

screen.exitonclick()
