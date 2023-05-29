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
