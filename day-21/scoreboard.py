from turtle import Turtle


class Score(Turtle):
    def __init__(self) -> None:
        super().__init__()
        self.score = 0
        self.hideturtle()
        self.penup()
        self.color("white")
        self.goto(0, 280)
        # self.write(f"Score: {self.score}", False, align="center",
        #           font = ("Arial", 12, "normal"))
        self.increase_score()

    def increase_score(self):
        self.clear()
        self.write(f"Score: {self.score}", False, align="center",
                   font=("Arial", 12, "normal"))
        self.score += 1

    def game_over(self):
        self.goto(0, 0)
        self.write("GAME OVER", False, align="center",
                   font=("Aril", 12, "normal"))
