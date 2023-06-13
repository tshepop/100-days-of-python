from turtle import Turtle


class Score(Turtle):

    def __init__(self):
        super().__init__()
        self.right_score = 0
        self.left_score = 0
        self.hideturtle()
        self.penup()
        self.color("white")
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.goto(200, 280)
        self.write(f"Player One: {self.right_score}",
                   align="center", font=("Arial", 12, "normal"))
        self.goto(-200, 280)
        self.write(f"Player Two: {self.left_score}",
                   align="center", font=("Arial", 12, "normal"))

    def increase_right_score(self):
        self.right_score += 1
        self.update_scoreboard()

    def increase_left_score(self):
        self.left_score += 1
        self.update_scoreboard()
