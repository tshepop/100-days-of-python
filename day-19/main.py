from turtle import Turtle, Screen

robot = Turtle()
screen = Screen()
# print(screen.screensize())
robot.color("firebrick")

def forward():
  robot.fd(10)

def back():
  robot.back(10)

def right_turn():
  robot.rt(10)

def left_turn():
  robot.lt(10)
  
def half_moon():
  robot.circle(-120, 180)
  

def clear():
  robot.clear()
  robot.penup()
  robot.home()
  robot.pendown()

screen.onkey(forward, "w")
screen.onkey(back, "s")
screen.onkey(right_turn, "d")
screen.onkey(left_turn, "f")
screen.onkey(half_moon, "h")
screen.onkey(clear, "c")

screen.listen()

screen.exitonclick()