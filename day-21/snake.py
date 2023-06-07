from turtle import Turtle

MOVE_DISTANCE = 20

# snake segments
STARTING_POSITION = [(0, 0), (-20, 0), (-40, 0)]

# turtle orientation (directions)
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0
LEFT = 180


class Snake:
    def __init__(self) -> None:
        self.snake_body = []
        self.create_snake()
        self.snake_head = self.snake_body[0]

    def create_snake(self):
        for position in STARTING_POSITION:
            self.body_segment(position)
            # self.snake = Turtle("square")
            # self.snake.penup()
            # self.snake.color("white")
            # self.snake.goto(position)
            # self.snake_body.append(self.snake)

    def extend(self):
        # add a new segment to extend the snake body
        # position() function/method belongs to the Turtle
        # position returns the  turtle current location
        self.body_segment(self.snake_body[-1].position())

    def body_segment(self, position):
        self.snake = Turtle("square")
        self.snake.penup()
        self.snake.color("white")
        self.snake.goto(position)
        self.snake_body.append(self.snake)

    def move(self):
        # make the snake body to move as one, the segments to move in unison
        # loop backwards and  return x and y coordinates,
        # pass the x and y to the goto method

        for seg_num in range(len(self.snake_body) - 1, 0, -1):
            pos_x = self.snake_body[seg_num - 1].xcor()
            pos_y = self.snake_body[seg_num - 1].ycor()
            self.snake_body[seg_num].goto(pos_x, pos_y)

        self.snake_head.fd(MOVE_DISTANCE)

    # prevent the snake changing direction - e.g.(moving forward prevent backward moving)
    # use the if statement,
    # repeat the steps for up, down, right, left functions

    def up(self):
        if self.snake_head.heading() != DOWN:
            self.snake_head.setheading(UP)

    def down(self):
        if self.snake_head.heading() != UP:
            self.snake_head.setheading(DOWN)

    def right(self):
        if self.snake_head.heading() != LEFT:
            self.snake_head.setheading(RIGHT)

    def left(self):
        if self.snake_head.heading() != RIGHT:
            self.snake_head.setheading(LEFT)
