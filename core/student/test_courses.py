from rest_framework.test import APIClient;
import pytest;  
from .models import CustomUser, Course

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user(db):
    user = CustomUser.objects.create(username = 'username',password='password',user_type = '3')
    return user

@pytest.mark.django_db  
def test_get_course(client,user):  
    ENDPOINT = 'http://127.0.0.1:8000/api/get_course'
    client.force_authenticate(user=user)
    Course.objects.create(course_name='Test Course')
    response = client.get(ENDPOINT)
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1


@pytest.mark.django_db
def test_create_course(client,user):
    client.force_authenticate(user=user)
    ENDPOINT = 'http://127.0.0.1:8000/api/create_course'
    payload = {
        'course_name' : "c++"
    }

    response = client.post(ENDPOINT,data=payload,format='json')
    response_data = response.json() 
    assert response.status_code == 201
    assert response_data['course_name'] == 'c++'


@pytest.mark.django_db
def test_update_course(client,user):
    client.force_authenticate(user=user)
    course = Course.objects.create(course_name='Old Course Name')
    ENDPOINT = f'http://127.0.0.1:8000/api/update_course/{course.id}' 
    payload = {
        'course_name' : "c++"
    }
    response = client.put(ENDPOINT,data=payload,format = 'json')
    response_data = response.json()
    assert response.status_code == 200
    assert response_data['message'] == 'Updated successfully' 


@pytest.mark.django_db
def test_delete_course(client,user):
    client.force_authenticate(user=user)
    course = Course.objects.create(course_name='Old Course Name')
    ENDPOINT = f'http://127.0.0.1:8000/api/delete_course/{course.id}' 
    response = client.delete(ENDPOINT)
    assert response.status_code == 204
    assert Course.objects.filter(id=course.id).count() == 0
  




   
    
    