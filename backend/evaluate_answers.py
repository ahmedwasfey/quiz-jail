def evaluate_answers(question, student_response):
    correct_answer = question['answer']
    if question['question_type'] == 'radio':
            # For radio buttons, the answer is correct if it matches the correct answer
            result = correct_answer == student_response[0]
    elif question['question_type'] == 'checkbox':
            # For checkboxes, the answer is correct if all the chosen options are correct
            result = set(correct_answer) == set(student_response)
    return result