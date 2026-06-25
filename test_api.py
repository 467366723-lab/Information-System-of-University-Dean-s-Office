import requests
import subprocess
import time
import os

BASE_URL = "http://127.0.0.1:5000/api"


proc = subprocess.Popen(["python", "app.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(3)

def test_get_all_students():
    resp = requests.get(f"{BASE_URL}/students")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_add_and_delete_student():
    new_stu = {"student_id":"S999", "name":"Test User", "grade":10}
    create_resp = requests.post(f"{BASE_URL}/students", json=new_stu)
    assert create_resp.status_code == 201

    get_resp = requests.get(f"{BASE_URL}/students/S999")
    assert get_resp.json()["name"] == "Test User"

    del_resp = requests.delete(f"{BASE_URL}/students/S999")
    assert del_resp.status_code == 200

    check_resp = requests.get(f"{BASE_URL}/students/S999")
    assert check_resp.status_code == 404


def teardown_module():
    proc.terminate()