class QuizBrain:
  def __init__(self, question_list):
    self.question_list = question_list
    self.question_number = 0
    
  
  def next_question(self):
    self.score_counter = 0
    
    for item in self.question_list:
      self.question_number += 1
      #user_answer = input("True/False? ")
      user_answer = input(f"Q.{self.question_number}: {item.text} (True/False)? ").lower()
      
      if user_answer == item.answer.lower():
        self.score_counter += 1
        print("You got it right!")
        print(f"The correct answer was: {item.answer}")
        print(f"Your current score is: {self.score_counter}/{self.question_number}")
        print("\n")
      else:
        self.score_counter = self.score_counter
        print("That's wrong!")
        print(f"The correct answer was: {item.answer}")
        print(f"Your current score is: {self.score_counter}/{self.question_number}")
        print("\n")
        

    print("You have completed the Quiz!")
    print(f"Your final score is: {self.score_counter}/{self.question_number}")