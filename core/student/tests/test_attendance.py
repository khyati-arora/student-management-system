from rest_framework.test import APIClient;
import pytest;  
from student.models import CustomUser, Course, Students, Attendance
from django.utils import timezone

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user(db):
    user = CustomUser.objects.create(username = 'username',password='password',user_type = '3')
    return user


def test_get_attendance(client,user):  
    
    client.force_authenticate(user=user)
    user_student = CustomUser.objects.create(username = 'student@gmail.com',password='student',user_type = '2')
    student = Students.objects.create(basic_details = user_student, guardian = 'parent')
    course = Course.objects.create(course_name='Test Course')
    ENDPOINT = f'http://127.0.0.1:8000/api/get_attendance/{course.id}/{student.id}'
    Attendance.objects.create(student = student,course = course,status = 'Present')
    response = client.get(ENDPOINT)
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1

def test_get_attendance_course__present(client,user):  
    
    client.force_authenticate(user=user)
    user_student = CustomUser.objects.create(username = 'student@gmail.com',password='student',user_type = '2')
    student = Students.objects.create(basic_details = user_student, guardian = 'parent')
    course = Course.objects.create(course_name='Test Course')
    Attendance.objects.create(student = student,course = course,status='Present')
    ENDPOINT = f'http://127.0.0.1:8000/api/get_attendance/{course.id}'
    response = client.get(ENDPOINT)
    assert response.status_code == 200

def test_get_attendance_course_not_present(client,user):  
    
    client.force_authenticate(user=user)
    user_student = CustomUser.objects.create(username = 'student@gmail.com',password='student',user_type = '2')
    student = Students.objects.create(basic_details = user_student, guardian = 'parent')
    course = Course.objects.create(course_name='Test Course')
    ENDPOINT = f'http://127.0.0.1:8000/api/get_attendance/{course.id}'
    response = client.get(ENDPOINT)
    assert response.status_code == 404


def test_add_attendance(client,user):  
    client.force_authenticate(user=user)
    ENDPOINT = 'http://127.0.0.1:8000/api/create_attendance'
    user_student = CustomUser.objects.create(username = 'student@gmail.com',password='student',user_type = '2')
    student = Students.objects.create(basic_details = user_student, guardian = 'parent')
    course = Course.objects.create(course_name='Test Course')

    payload = {
        'student' : student.id,
        'course' : course.id,
        'status' : 'Present'
    }

    response = client.post(ENDPOINT,data=payload,format='json')
    response_data = response.json() 
    assert response.status_code == 201
    assert response_data['status'] == 'Present'

def test_add_attendance_missing_field(client,user):  
    client.force_authenticate(user=user)
    ENDPOINT = 'http://127.0.0.1:8000/api/create_attendance'
    user_student = CustomUser.objects.create(username = 'student@gmail.com',password='student',user_type = '2')
    student = Students.objects.create(basic_details = user_student, guardian = 'parent')
    course = Course.objects.create(course_name='Test Course')

    payload = {
        'student' : student.id,
        'course' : course.id
    }

    response = client.post(ENDPOINT,data=payload,format='json')
    response_data = response.json() 
    assert response.status_code == 400

def test_add_attendance_invalid_course_id(client,user):  
    client.force_authenticate(user=user)
    ENDPOINT = 'http://127.0.0.1:8000/api/create_attendance'
    user_student = CustomUser.objects.create(username = 'student@gmail.com',password='student',user_type = '2')
    student = Students.objects.create(basic_details = user_student, guardian = 'parent')
    course = Course.objects.create(course_name='Test Course')

    payload = {
        'student' : student.id,
        'course' : -1,
        'status' : 'Present'
    }

    response = client.post(ENDPOINT,data=payload,format='json')
    response_data = response.json() 
    assert response.status_code == 400

def test_add_attendance_invalid_student_id(client,user):  
    client.force_authenticate(user=user)
    ENDPOINT = 'http://127.0.0.1:8000/api/create_attendance'
    user_student = CustomUser.objects.create(username = 'student@gmail.com',password='student',user_type = '2')
    student = Students.objects.create(basic_details = user_student, guardian = 'parent')
    course = Course.objects.create(course_name='Test Course')

    payload = {
        'student' : -1,
        'course' : course.id,
        'status' : 'Present'
    }

    response = client.post(ENDPOINT,data=payload,format='json')
    response_data = response.json() 
    assert response.status_code == 400    

def test_add_attendance_invalid_type(client,user):  
    client.force_authenticate(user=user)
    ENDPOINT = 'http://127.0.0.1:8000/api/create_attendance'
    user_student = CustomUser.objects.create(username = 'student@gmail.com',password='student',user_type = '2')
    student = Students.objects.create(basic_details = user_student, guardian = 'parent')
    course = Course.objects.create(course_name='Test Course')

    payload = {
        'student' : "student",
        'course' : course.id,
        'status' : 'Present'
    }

    response = client.post(ENDPOINT,data=payload,format='json')
    response_data = response.json() 
    assert response.status_code == 400    

   

def test_update_attendance(client,user):  
    client.force_authenticate(user=user)
    user_student = CustomUser.objects.create(username = 'student@gmail.com',password='student',user_type = '2')
    student = Students.objects.create(basic_details = user_student, guardian = 'parent')
    course = Course.objects.create(course_name='Test Course')
    Attendance.objects.create(student = student,course=course,status='Present')
    ENDPOINT = f'http://127.0.0.1:8000/api/update_attendance/{course.id}/{student.id}'
    payload = {
        'status' : 'Absent'
    }
    response = client.put(ENDPOINT,data=payload,format='json')
    response_data = response.json()
    assert response.status_code == 200
    assert response_data == 'Updated successfully'

def test_update_attendance_without_payload(client,user):  
    client.force_authenticate(user=user)
    user_student = CustomUser.objects.create(username = 'student@gmail.com',password='student',user_type = '2')
    student = Students.objects.create(basic_details = user_student, guardian = 'parent')
    course = Course.objects.create(course_name='Test Course')
    Attendance.objects.create(student = student,course=course,status='Present')
    ENDPOINT = f'http://127.0.0.1:8000/api/update_attendance/{course.id}/{student.id}'
    payload = {
        
    }
    response = client.put(ENDPOINT,data=payload,format='json')
    assert response.status_code == 400

def test_update_attendance__payload(client,user):  
    client.force_authenticate(user=user)
    user_student = CustomUser.objects.create(username = 'student@gmail.com',password='student',user_type = '2')
    student = Students.objects.create(basic_details = user_student, guardian = 'parent')
    course = Course.objects.create(course_name='Test Course')
    Attendance.objects.create(student = student,course=course,status='Present')
    ENDPOINT = f'http://127.0.0.1:8000/api/update_attendance/{course.id}/{student.id}'
    payload = {
        'status' : 1
    }
    response = client.put(ENDPOINT,data=payload,format='json')
    assert response.status_code == 400   
      

def test_delete_result(client,user):
    client.force_authenticate(user=user)
    user_student = CustomUser.objects.create(username = 'student@gmail.com',password='student',user_type = '2')
    student = Students.objects.create(basic_details = user_student, guardian = 'parent')
    course = Course.objects.create(course_name='Test Course')
    Attendance.objects.create(student = student,course=course,status = 'Present',date=timezone.now().date())
    ENDPOINT = f'http://127.0.0.1:8000/api/delete_attendance/{course.id}/{student.id}' 
    response = client.delete(ENDPOINT)
    assert response.status_code == 204
    assert Attendance.objects.filter(id=course.id).count() == 0