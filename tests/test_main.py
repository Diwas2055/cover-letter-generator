import os
import sys

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from main import app
from main import app, delete_file


client = TestClient(app)


def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}

def test_delete_file():
    # test case for existing file
    with open("test.txt", "w") as f:
        f.write("test file")
    delete_file("test.txt")
    assert not os.path.exists("test.txt")

    # test case for non-existing file
    try:
        delete_file("non_existing_file.txt")
    except RuntimeError as e:
        assert str(e) == "File at path non_existing_file.txt does not exist."


def test_download_file():
    # test case for valid form data
    response = client.post("/download", data={
        "job_title": "python",
        "company_name": "abc company",
        "your_name": "john doe"
    })
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/octet-stream"
    assert response.headers["content-disposition"] == "attachment; filename*=utf-8''John%20Doe-cover_letter.pdf"

    # test case for invalid form data
    response = client.post("/download", data={
        "job_title": "",
        "company_name": "",
        "your_name": ""
    })
    assert response.status_code == 422


def test_download_internship():
    # test case for valid form data
    response = client.post("/download/internship", data={
        "your_name": "john doe",
        "company_name": "abc company",
        "status": "intern",
        "study_field": "computer science",
        "university_name": "xyz university"
    })
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"

    # test case for invalid form data
    response = client.post("/download/internship", data={
        "your_name": "",
        "company_name": "",
        "status": "",
        "study_field": "",
        "university_name": ""
    })
    assert response.status_code == 422


def test_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_internship():
    response = client.get("/internship")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]