from turtle import Turtle
import random


class Food(Turtle):

    def __init__(self) -> None:
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_wid=0.9, stretch_len=0.9)
        self.color("orange")
        self.speed("fastest")
        self.refresh()

    def refresh(self):
        x_random = random.randint(-270, 270)
        y_random = random.randint(-270, 270)
        self.goto(x_random, y_random)
