from question_model import Question
from data import question_data
from quiz_brain import QuizBrain

"""
My solution to this challenge does not include a while loop and a still_has_questions() method.
It returns the desired results.

Data from: Open Trivia DB
url: https://opentdb.com
"""
question_bank = []

for index in question_data:
    # q = f"q{count} {index['text']}"
    # a = f"a{count} {index['answer']}"
    #print(q, a)
    # print(a)
    #result = Question(q, a)
    # question_bank.append(result)

    q = index['question']
    a = index['correct_answer']
    question_bank.append(Question(q, a))


# print(question_bank[0].text)

user_quiz = QuizBrain(question_bank)
user_quiz.next_question()
