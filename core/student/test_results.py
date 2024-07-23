from rest_framework.test import APIClient;
import pytest;  
from .models import CustomUser, Students, Course,Results

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user(db):
    user = CustomUser.objects.create(username = 'username',password='password',user_type = '3')
    return user

def test_get_result(client,user):
    ENDPOINT = 'http://127.0.0.1:8000/api/get_result'
    client.force_authenticate(user=user)
    user_student = CustomUser.objects.create(username = 'student@gmail.com',password='student',user_type = '2')
    student = Students.objects.create(basic_details = user_student, guardian = 'parent')
    course = Course.objects.create(course_name='Test Course')
    Results.objects.create(student = student,course=course,grade = 'A+')
    response = client.get(ENDPOINT)
    response_data = response.json()
    print(response_data)
    assert response.status_code == 200
    assert len(response_data) == 1

def test_add_result(client,user):
    ENDPOINT = 'http://127.0.0.1:8000/api/create_result'
    client.force_authenticate(user=user)
    user_student = CustomUser.objects.create(username = 'student@gmail.com',password='student',user_type = '2')
    student = Students.objects.create(basic_details = user_student, guardian = 'parent')
    course = Course.objects.create(course_name='Test Course')

    payload = {
        'student' : student.id,
        'course' : course.id,
        'grade' : 'B+'
    }

    response = client.post(ENDPOINT,data=payload,format='json')
    response_data = response.json()
    print(response_data)
    assert response.status_code == 201
    assert response_data['grade'] == 'B+' 

def test_add_result_invalid_field(client,user):
    ENDPOINT = 'http://127.0.0.1:8000/api/create_result'
    client.force_authenticate(user=user)
    user_student = CustomUser.objects.create(username = 'student@gmail.com',password='student',user_type = '2')
    student = Students.objects.create(basic_details = user_student, guardian = 'parent')
    course = Course.objects.create(course_name='Test Course')

    payload = {
        'student' : -1,
        'course' : course.id,
        'grade' : 'B+'
    }

    response = client.post(ENDPOINT,data=payload,format='json')
    response_data = response.json()
    print(response_data)
    assert response.status_code == 400

def test_add_result_invalid_field_course_id(client,user):
    ENDPOINT = 'http://127.0.0.1:8000/api/create_result'
    client.force_authenticate(user=user)
    user_student = CustomUser.objects.create(username = 'student@gmail.com',password='student',user_type = '2')
    student = Students.objects.create(basic_details = user_student, guardian = 'parent')
    course = Course.objects.create(course_name='Test Course')

    payload = {
        'student' : student.id,
        'course' : -1,
        'grade' : 'B+'
    }

    response = client.post(ENDPOINT,data=payload,format='json')
    response_data = response.json()
    print(response_data)
    assert response.status_code == 400   

def test_add_result_missing_field(client,user):
    ENDPOINT = 'http://127.0.0.1:8000/api/create_result'
    client.force_authenticate(user=user)
    user_student = CustomUser.objects.create(username = 'student@gmail.com',password='student',user_type = '2')
    student = Students.objects.create(basic_details = user_student, guardian = 'parent')
    course = Course.objects.create(course_name='Test Course')

    payload = {
        'student' : student.id,
        'course' : course.id
    }

    response = client.post(ENDPOINT,data=payload,format='json')
    response_data = response.json()
    print(response_data)
    assert response.status_code == 400      

def test_update_result(client,user):   
    client.force_authenticate(user=user)
    user_student = CustomUser.objects.create(username = 'student@gmail.com',password='student',user_type = '2')
    student = Students.objects.create(basic_details = user_student, guardian = 'parent')
    course = Course.objects.create(course_name='Test Course')
    Results.objects.create(student = student,course=course,grade = 'B+')
    ENDPOINT = f'http://127.0.0.1:8000/api/update_result/{course.id}/{student.id}'
    payload = {
        'grade' : 'A+'
    }
    response = client.put(ENDPOINT,data=payload,format='json')
    response_data = response.json()
    assert response.status_code == 200
    assert response_data['message'] == 'Updated successfully'

def test_update_result_missing_payload(client,user):   
    client.force_authenticate(user=user)
    user_student = CustomUser.objects.create(username = 'student@gmail.com',password='student',user_type = '2')
    student = Students.objects.create(basic_details = user_student, guardian = 'parent')
    course = Course.objects.create(course_name='Test Course')
    Results.objects.create(student = student,course=course,grade = 'B+')
    ENDPOINT = f'http://127.0.0.1:8000/api/update_result/{course.id}/{student.id}'
    payload = {
        
    }
    response = client.put(ENDPOINT,data=payload,format='json')
    response_data = response.json()
    assert response.status_code == 400
   

def test_delete_result(client,user):
    client.force_authenticate(user=user)
    user_student = CustomUser.objects.create(username = 'student@gmail.com',password='student',user_type = '2')
    student = Students.objects.create(basic_details = user_student, guardian = 'parent')
    course = Course.objects.create(course_name='Test Course')
    result = Results.objects.create(student = student,course=course,grade = 'B+')
    ENDPOINT = f'http://127.0.0.1:8000/api/delete_result/{course.id}/{student.id}' 
    response = client.delete(ENDPOINT)
    assert response.status_code == 204
    assert Results.objects.filter(id=course.id).count() == 0
