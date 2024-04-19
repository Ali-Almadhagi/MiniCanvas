class Assignment:
    def __init__(self, assignment_id, due_date, course_id):
        self.assignment_id = assignment_id
        self.due_date = due_date
        self.course_id = course_id
        self.submission_list = []

    def submit(self, submission):
        self.submission_list.append(submission)

class Submission:
    def __init__(self, student_id, content):
        self.submission = content
        self.student_id = student_id
        self.grade = -1.0 # None