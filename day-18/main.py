from turtle import Turtle, Screen
import random
import colorgram

paint = Turtle()
screen = Screen()
screen.colormode(255)

# extract colors from the image
colors = colorgram.extract("spoti.jpg", 30)

# list to store colors
color_spot = []

for color in colors:
    color_spot.append((color.rgb[0], color.rgb[1], color.rgb[2]))

# print(color_spot)

# turtle default position
# print(paint.pos())

paint.penup()
paint.setpos(-200, 200)
paint.hideturtle()


def draw():
    """draw dots of size 20 pixels, in random colors"""
    paint.dot(20, random.choice(color_spot))


row_count = 10

for row in range(10):
    for col in range(10):
        draw()
        paint.fd(50)

    paint.back(50 * row_count)

    paint.right(90)
    paint.fd(50)
    paint.left(50)

screen.exitonclick()
