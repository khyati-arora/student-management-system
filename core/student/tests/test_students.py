from rest_framework.test import APIClient;
import pytest;  
from ..models import CustomUser, Students

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user(db):
    user = CustomUser.objects.create(username = 'username',password='password',user_type = '3')
    return user

@pytest.mark.django_db  
def test_get_student(client,user):  
    ENDPOINT = 'http://127.0.0.1:8000/api/get_student'
    client.force_authenticate(user=user)
    user_student = CustomUser.objects.create(username = 'student@gmail.com',password='student',user_type = '2')
    Students.objects.create(basic_details = user_student, guardian = 'parent')
    response = client.get(ENDPOINT)
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1


@pytest.mark.django_db
def test_post_student(client,user):
    ENDPOINT = 'http://127.0.0.1:8000/api/create_student'
    client.force_authenticate(user=user)

    payload = {
        'basic_details' : {
            'username' : 'user1@gmail.com',
            'password' : 'student',
            "user_type" : "2",
            "address" : "354",
            "gender" : "Female",
            "name" : "Khyati"
        },
        "guardian" : "Sat Pal"
    }
    response = client.post(ENDPOINT,data=payload,format='json')
    response_data = response.json() 
    assert response.status_code == 201
    assert response_data['guardian'] == 'Sat Pal'

@pytest.mark.django_db
def test_post_student_missing_fields(client,user):
    ENDPOINT = 'http://127.0.0.1:8000/api/create_student'
    client.force_authenticate(user=user)

    payload = {
        'basic_details' : {
            'password' : 'student',
            "user_type" : "2",
            "address" : "354",
            "gender" : "Female",
            "name" : "Khyati"
        },
        "guardian" : "Sat Pal"
    }
    response = client.post(ENDPOINT,data=payload,format='json')
    assert response.status_code == 400
    
@pytest.mark.django_db
def test_post_student_invalid_input(client,user):
    ENDPOINT = 'http://127.0.0.1:8000/api/create_student'
    client.force_authenticate(user=user)

    payload = {
        'basic_details' : {
            'password' : 'student',
            "user_type" : "2",
            "address" : "354",
            "gender" : "Female",
            "name" : "Khyati",
            "username" : 123
        },
        "guardian" : "Sat Pal"
    }
    response = client.post(ENDPOINT,data=payload,format='json')
    assert response.status_code == 400   


@pytest.mark.django_db
def test_update_student(client,user):
    client.force_authenticate(user=user)
    user_student = CustomUser.objects.create(username = 'student@gmail.com',password='student',user_type = '2')
    student = Students.objects.create(basic_details = user_student, guardian = 'parent')
    ENDPOINT = f'http://127.0.0.1:8000/api/update_student/{student.id}' 
    payload = {
        'guardian' : 'parent1'
    }
    response = client.put(ENDPOINT,data=payload,format = 'json')
    response_data = response.json()
    assert response.status_code == 200
    assert response_data['message'] == 'Updated successfully' 


@pytest.mark.django_db
def test_update_student_missing_payload(client,user):
    client.force_authenticate(user=user)
    user_student = CustomUser.objects.create(username = 'student@gmail.com',password='student',user_type = '2')
    student = Students.objects.create(basic_details = user_student, guardian = 'parent')
    ENDPOINT = f'http://127.0.0.1:8000/api/update_student/{student.id}' 
    payload = {
       
    }
    response = client.put(ENDPOINT,data=payload,format = 'json')
    response_data = response.json()
    assert response.status_code == 400
    


@pytest.mark.django_db
def test_delete_student(client,user):
    client.force_authenticate(user=user)
    user_student = CustomUser.objects.create(username = 'student@gmail.com',password='student',user_type = '2')
    student = Students.objects.create(basic_details = user_student, guardian = 'parent')
    ENDPOINT = f'http://127.0.0.1:8000/api/delete_student/{student.id}' 

    response = client.delete(ENDPOINT)
    assert response.status_code == 204
    assert Students.objects.filter(id=student.id).count() == 0
    assert CustomUser.objects.filter(id=user_student.id).count() == 0






   