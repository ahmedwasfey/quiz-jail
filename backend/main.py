import random
from flask import Flask, request
from cachetools import LRUCache
import os 
import json
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# Create a cache to store shuffled quiz questions for each student
question_cache = LRUCache(maxsize=1000)
questions = [    {        'question': 'What is the capital of France?',        'choices': ['Paris', 'London', 'Berlin', 'Rome'],
        'answer': 'Paris',
        'question_type': 'radio'
    },
    {
        'question': 'Which of the following countries are in Europe?',
        'choices': ['Spain', "France" 'Japan', 'Brazil', 'Australia'],
        'answer': ['Spain', 'France'],
        'question_type': 'checkbox'
    },
    {
        'question': 'What is the largest planet in the solar system?',
        'choices': ['Earth', 'Jupiter', 'Mars', 'Venus'],
        'answer': 'Jupiter',
        'question_type': 'radio'
    }
]


@app.route('/register', methods=['POST'])
def register():
    # Get the name, student ID, and unique identifier from the request
    name = request.json.get('name')
    student_id = request.json.get('student_id')
    id = request.json.get('id')

    # Get the list of quiz questions from the request

    # Shuffle the list of questions
    random.shuffle(questions)

    # Store the shuffled questions in the cache
    question_cache[id] = questions.copy()

    # Return a success message
    return {'message': 'Successfully registered student and shuffled questions.'}

@app.route('/get-question', methods=['GET'])
def get_question():
    # Get the unique identifier from the request
    id = request.args.get('id')

    # Get the shuffled questions from the cache
    questions = question_cache[id]

    # Get the next question from the list
    if len(questions)==0 :
        return {
            "question" : "finished",
            "choices" : [],
            "question_type":'radio'

        }
    question = dict(questions[0])
    question.pop("answer")
    # Return the question
    return question

@app.route('/submit-answer', methods=['POST' , 'OPTIONS'])
def submit_answer():
    # Get the unique identifier and answer from the request
    print("hi....")
    print(request.headers)
    print(request.data)
    if request.data :
        students_answer = json.loads(request.data.decode())
        id  = students_answer['id']
        answer = students_answer['choice']
        print(question_cache[id][0])
        print(answer)
        question_cache[id].pop(0)
    # print(request.json())
    # print(request.args)
    # print(request.json())
    return  "okay"


if __name__ == '__main__':
    port = os.environ.get("PORT", 8500)
    print(port)
    app.run(port=port)