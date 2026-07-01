import pytest
import os
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def setup_module():
    for f in ["data/students.txt", "data/courses.txt", "data/grades.txt"]:
        if os.path.exists(f):
            os.remove(f)

def test_index(client):
    res = client.get('/')
    assert res.status_code == 200
    assert "Educational Administration API is running" in res.get_json()["message"]

# Student tests
def test_get_students_empty(client):
    res = client.get('/api/students')
    assert res.status_code == 200
    assert res.get_json() == []

def test_add_student_success(client):
    res = client.post('/api/students', json={
        "student_id": "S001",
        "name": "Alice",
        "grade": 2024
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data["student_id"] == "S001"

def test_add_student_duplicate(client):
    res = client.post('/api/students', json={
        "student_id": "S001",
        "name": "Bob",
        "grade": 2023
    })
    assert res.status_code == 409

def test_delete_student_success(client):
    res = client.delete('/api/students/S001')
    assert res.status_code == 200

def test_delete_student_not_found(client):
    res = client.delete('/api/students/S999')
    assert res.status_code == 404

# Course tests
def test_get_courses_empty(client):
    res = client.get('/api/courses')
    assert res.status_code == 200
    assert res.get_json() == []

def test_add_course_success(client):
    res = client.post('/api/courses', json={
        "course_id": "C001",
        "name": "Math",
        "credits": 4
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data["course_id"] == "C001"

def test_add_course_invalid_credits(client):
    res = client.post('/api/courses', json={
        "course_id": "C002",
        "name": "English",
        "credits": 25
    })
    assert res.status_code == 400

def test_delete_course_success(client):
    res = client.delete('/api/courses/C001')
    assert res.status_code == 200

# Grade tests
def test_get_grades_empty(client):
    res = client.get('/api/grades')
    assert res.status_code == 200
    assert res.get_json() == []

def test_add_grade_success(client):
    client.post('/api/students', json={"student_id": "S001", "name": "Alice", "grade": 2024})
    client.post('/api/courses', json={"course_id": "C001", "name": "Math", "credits": 4})
    res = client.post('/api/grades', json={
        "student_id": "S001",
        "course_id": "C001",
        "score": 88
    })
    assert res.status_code == 201

def test_add_grade_invalid_score(client):
    res = client.post('/api/grades', json={
        "student_id": "S001",
        "course_id": "C001",
        "score": 105
    })
    assert res.status_code == 400

def test_delete_grade_success(client):
    res = client.delete('/api/grades/S001/C001')
    assert res.status_code == 200