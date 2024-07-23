from rest_framework.test import APIClient;
import pytest;  
from .models import CustomUser, Course, Students, Attendance

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user(db):
    user = CustomUser.objects.create(username = 'username',password='password',user_type = '3')
    return user

@pytest.mark.django_db  
def test_get_attendance(client,user):  
    ENDPOINT = 'http://127.0.0.1:8000/api/get_course'
    client.force_authenticate(user=user)
    user_student = CustomUser.objects.create(username = 'student@gmail.com',password='student',user_type = '2')
    student = Students.objects.create(basic_details = user_student, guardian = 'parent')
    course = Course.objects.create(course_name='Test Course')
    Attendance.objects.create(student = student,course = course,status = 'Present')
    response = client.get(ENDPOINT)
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1





