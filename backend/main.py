import csv
import random
from flask import Flask, jsonify, render_template, request, send_file
from cachetools import LRUCache
import os 
import json
import time
from flask_cors import CORS
from evaluate_answers import evaluate_answers
from time_diff import is_timeout
from threading import Lock
app = Flask(__name__)
CORS(app)
cache_lock = Lock()
# Create a cache to store shuffled quiz questions for each student
question_cache = LRUCache(maxsize=1000)
grades_cache = LRUCache(maxsize=1000)
questions =[]
quiz_time=2
@app.route('/', methods=['GET'])
def main_page():
    return render_template('index.html')

@app.route('/upload', methods=['GET'])
def upload_quiz():
    return render_template('load_quiz.html')

@app.route('/upload', methods=['POST'])
def process_upload():
    global questions , quiz_time
    # Get the uploaded file from the request
    uploaded_file = request.files['quiz_file']

    # Parse the file as JSON
    questions = json.loads(uploaded_file.read())
    if "quiz_time" in questions : 
        quiz_time = questions.get("quiz_time", 10)
        questions = questions.get("questions")
    print("questions =", questions)

    return render_template("uploaded.html")

@app.route('/fetch', methods=['GET'])
def fetch_json():
    # Create the JSON object to return to the client
    return render_template("fetch_results.html", data = dict(grades_cache))
@app.route('/register', methods=['POST'])
def register():
    # Get the name, student ID, and unique identifier from the request
    name = request.json.get('name')
    student_id = request.json.get('student_id')
    id = request.json.get('id')

    # Get the list of quiz questions from the request

    # Shuffle the list of questions
    cache_lock.acquire()
    try :
        random.shuffle(questions)

        # Store the shuffled questions in the cache
        question_cache[id] =questions.copy()
        grades_cache[id] = {
                "name":name,
                "student_id":  student_id, 
                "grade" : 0 ,
                "start_time":  time.time()
            }
    finally :
        cache_lock.release()
    # Return a success message
    return {'message': 'Successfully registered student and shuffled questions.'}

@app.route('/get-question', methods=['GET'])
def get_question():
    # Get the unique identifier from the request
    id = request.args.get('id')

    # Get the shuffled questions from the cache
    questions = question_cache[id]

    # Get the next question from the list
    timed_out = is_timeout(grades_cache[id]['start_time'], time.time() , quiz_time)
    if len(questions)==0 or timed_out :
        cache_lock.acquire()
        try :
            grades_cache[id]["is_timeout"]=timed_out
            grades_cache[id].pop("start_time")
        finally:
            cache_lock.release()
        return grades_cache[id]
    question = dict(questions[0])
    question.pop("answer")
    # Return the question
    return question

@app.route('/submit-answer', methods=['POST' , 'OPTIONS'])
def submit_answer():
    if request.data :
        print(request.data)
        students_answer = json.loads(json.loads(request.data.decode()))
        print(students_answer)
        id  = students_answer['id']
        answer = students_answer['choice']
        cache_lock.acquire()
        try :
            if answer : 
                grades_cache[id]['grade'] += evaluate_answers(question_cache[id][0], answer)
            question_cache[id].pop(0)
        finally :
            cache_lock.release()
        return  "okay"
    else :
        return  "your answer is not formatted correctly .."
   




@app.route('/download-csv', methods=['GET'])
def download_csv():
    data = dict(grades_cache)

    # Create a list of dictionaries with the data of the smaller JSON objects
    csv_data = [v for k, v in data.items()]

    # Create the CSV file
    si = csv.writer(open("results/data.csv", "w"))
    if csv_data :
        si.writerow(csv_data[0].keys())
        for row in csv_data:
            si.writerow(row.values())

    # Send the CSV file to the user
    return send_file(open('results/data.csv',"rb"),
                     mimetype='text/csv',
                     download_name='quiz_results.csv',
                     as_attachment=True)

@app.route('/download-json', methods=['GET'])
def download_json():
    data = dict(grades_cache)
    with open("results/data.json", "w") as f :
        json.dump(data, f)
    # Send the JSON data to the user
    return send_file("results/data.json",
                     mimetype='application/json',
                     download_name='quiz_results.json',
                     as_attachment=True)

if __name__ == '__main__':
    port = os.environ.get("PORT", 8500)
    print(port)
    app.run(port=port)
