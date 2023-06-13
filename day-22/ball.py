from turtle import Turtle


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.x_move = 10
        self.y_move = 10
        # start/default ball speed
        self.ball_speed = 0.1

    def move(self):
        # Get the current x and y coordinates,
        # the coordinates + number (direction to move to)
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self):
        self.y_move *= -1

    def bounce_x(self):
        self.x_move *= -1
        # increase the speed of the ball after each contact with paddle
        self.ball_speed *= 0.9

    def ball_reset(self):
        self.goto(0, 0)
        # reset the ball speed
        self.ball_speed = 0.1
        self.bounce_x()
