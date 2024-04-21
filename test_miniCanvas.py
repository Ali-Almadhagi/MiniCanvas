import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

# Import classes
from assignment import Assignment, Submission
from course import Course, CourseManager
from user import User, UserManager

client = TestClient(app)

# Fixture for course manager
@pytest.fixture
def course_manager():
    return CourseManager()

# Fixture for a course
@pytest.fixture
def course(course_manager):
    course_manager.create_a_course("CS101", "Fall 2024", [1, 2])
    return course_manager.course_list[0]  

# Fixture for user manager
@pytest.fixture
def user_manager():
    return UserManager()

# Fixture for assignment
@pytest.fixture
def assignment():
    return Assignment(1, "2024-12-01", 101)

# Tests for CourseManager
def test_generate_id(course_manager):
    initial_id = course_manager.counter
    course_manager.generate_id()
    assert course_manager.counter == initial_id + 1

def test_create_a_course(course_manager):
    new_course_id = course_manager.create_a_course("CS102", "Spring 2025", [1])
    assert new_course_id is not None
    assert new_course_id == course_manager.course_list[-1].course_id

def test_find_a_course(course_manager, course):
    found_course = course_manager.find_a_course(course.course_id)
    assert found_course is not None
    assert found_course.course_id == course.course_id

def test_course_str(course):
    course.teacher_list = ["Alice", "Bob"]
    course.student_list = ["Charlie", "David"]
    expected_str = "ID: 1, code: CS101, teachers: ['Alice', 'Bob'], students: ['Charlie', 'David']"
    assert str(course) == expected_str

def test_sync_with_database(course_manager):
    course_manager.sync_with_database()

# Tests for Course
def test_import_students(course):
    student_list = [1, 2, 3]
    course.import_students(student_list)
    assert course.student_list == student_list

def test_create_an_assignment(course):
    due_date = "2025-05-01"
    initial_list_size = len(course.assignment_list)
    course.create_an_assignment(due_date)

    # Check that the assignment list size has increased by 1
    assert len(course.assignment_list) == initial_list_size + 1

    # Verify the properties of the new assignment
    new_assignment = course.assignment_list[-1]  
    assert new_assignment.due_date == due_date
    assert new_assignment.course_id == course.course_id
    assert isinstance(new_assignment.assignment_id, int)  


def test_generate_assignment_id(course):
    initial_id = course.assignment_counter
    course.generate_assignment_id()
    assert course.assignment_counter == initial_id + 1

# Tests for UserManager
def test_user_manager_generate_id(user_manager):
    initial_id = user_manager.counter
    user_manager.generate_id()
    assert user_manager.counter == initial_id + 1

def test_create_a_user(user_manager):
    initial_user_count = len(user_manager.user_list)  
    user_manager.create_a_user("Bob", "password123", "student")
    
    # Check that the user list has increased by one
    assert len(user_manager.user_list) == initial_user_count + 1

    # Access the newly added user and verify its properties
    new_user = user_manager.user_list[-1]  
    assert new_user.name == "Bob"
    assert new_user.password == "password123"
    assert new_user.type == "student"
    assert isinstance(new_user.user_id, int)  

def test_find_users(user_manager):
    # Create a user and capture the initial user list length
    initial_user_count = len(user_manager.user_list)
    user_manager.create_a_user("Alice", "secure123", "teacher")
    
    # Ensure the user list is incremented
    assert len(user_manager.user_list) == initial_user_count + 1

    # Get the user ID from the newly added user
    new_user_id = user_manager.user_list[-1].user_id
    
    # Attempt to find the user by the new ID
    found_users = user_manager.find_users([new_user_id])
    assert len(found_users) == 1
    assert found_users[0].user_id == new_user_id

# Tests for User's string representation
def test_user_str_representation():
    user_id = 1
    name = "Test User"
    password = "password123"  
    user_type = "teacher"  
    user = User(user_id, name, password, user_type)
    
    # The expected string output of the __str__ method
    expected_str = f"ID: {user_id}, name: {name}, type: {user_type}"
    
    # Assert that calling str() on a User instance returns the expected string
    assert str(user) == expected_str


# Tests for Assignment
def test_submit(assignment):
    submission = Submission(1, "Answer")
    assignment.submit(submission)
    assert submission in assignment.submission_list

# Tests for main.py FastAPI endpoints
def test_welcome():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Welcome to our miniCanvas!"


def test_create_a_course_successful():
    response = client.post("/courses/CS101?semester=Fall 2024", json={
        "teacher_id_list": [1, 2]
    })
    assert response.status_code == 200
    assert isinstance(response.json(), int)  # Check if the response is an integer
    course_id = response.json()
    assert course_id > 0

def test_import_students_successful():
    # Create a course to test student import
    response = client.post("/courses/CS101?semester=Fall 2024", json={
        "teacher_id_list": [2]  
    })
    course_id = response.json()

    response = client.put(f"/courses/{course_id}/students", json={
        "student_id_list": [3, 4]
    })
    assert response.status_code == 200


    