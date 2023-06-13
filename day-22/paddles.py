from turtle import Turtle


class Paddle(Turtle):
    def __init__(self, position):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.penup()
        # default turtle size is: 20 x 20 pixels
        self.turtlesize(stretch_wid=5, stretch_len=1)
        self.goto(position)

    def up(self):
        # retrieve the current y coordinate
        # paddle.ycor() equals to 0, starting position
        # create a variable to hold new y coordinate
        # add a number to it , to move up
        self.new_y_cor = self.ycor() + 30
        self.goto(self.xcor(), self.new_y_cor)

    def down(self):
        self.new_y_cor = self.ycor() - 30
        self.goto(self.xcor(), self.new_y_cor)
