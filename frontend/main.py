import requests
from flask import Flask, redirect, render_template, request
import os
app = Flask(__name__)
BACKEND_SERVER = os.environ.get("BACKEND_SERVER")
@app.route('/', methods=['GET'])
def main_page():
    return render_template("index.html")

@app.route('/questions', methods=['GET'])
def questions():
    # Get the user's name, student ID, and unique identifier from the request
    name = request.args.get('name')
    student_id = request.args.get('student_id')
    id = request.args.get('id')

    # Send a POST request to the backend server to get the next question
    question_response = requests.post(BACKEND_SERVER+'/register', json={
        'name': name,
        'student_id': student_id,
        'id': id
    })

    # Get the question data from the response
    question_data = question_response.json()

    # Redirect the user to the next endpoint, passing the question data as URL parameters
    return redirect(f'/next?id={id}')

@app.route('/next', methods=['GET'])
def next():
    print("getting next question.... " )
    # Get the question data from the request
    id = request.args.get('id')
    question_response = requests.get(BACKEND_SERVER+f'/get-question?id={id}')
    question_response.raise_for_status()
    # Get the question data from the response
    question_data = question_response.json()
    print(question_data)
    # Render the next page with the question data
    return render_template('next.html', question=question_data['question'], choices=question_data['choices'], question_type=question_data['question_type'], id=id)
if __name__ == '__main__':
    app.run()
