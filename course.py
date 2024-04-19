from assignment import Assignment

class CourseManager:
    def __init__(self):
        self.course_list = []
        self.counter = 0

    def create_a_course(self, course_code, semester, teacher_list):
        ## automatically generate a courseId
        new_course_id = self.generate_id()
        new_course = Course(new_course_id, course_code, semester, teacher_list)

        # add the new course to the list
        self.course_list.append(new_course)
        return new_course_id

    def generate_id(self):
        self.counter += 1
        return self.counter

    def find_a_course(self, id):
        print(f"target id: {id}")
        for course in self.course_list:
            print(f"course: {course.course_id}")
            if course.course_id == id:
                return course
            
        return None

    def sync_with_database(self):
        # will not implement here
        pass

class Course:
    def __init__(self, course_id, course_code, semester, teacher_list):
        self.course_id = course_id
        self.course_code = course_code
        self.semester = semester
        self.teacher_list = teacher_list
        self.student_list = []
        self.assignment_list = []
        self.module_list = []
        self.assignment_counter = 0

    def import_students(self, student_list):
        # the admin should import the students to a course
        self.student_list = student_list
    
    def create_an_assignment(self, due_date):
        new_assignment_id = self.generate_assignment_id()
        new_assignment = Assignment(new_assignment_id, 
                                    due_date, self.course_id)
        self.assignment_list.append(new_assignment)
    
    def generate_assignment_id(self):
        self.assignment_counter += 1
        return self.assignment_counter

    def __str__(self) -> str:
        return f"ID: {self.course_id}, code: {self.course_code}, teachers: {self.teacher_list}. students: {self.student_list}"