from rest_framework.test import APIClient;
import pytest;  
from .models import CustomUser

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user(db):
    user = CustomUser.objects.create(username = 'username',password='password',user_type = '3')
    return user




@pytest.mark.django_db  
def test_get_admin(client,user):  
    ENDPOINT = 'http://127.0.0.1:8000/api/get_admin'
    client.force_authenticate(user=user)
    CustomUser.objects.create(username = 'student@gmail.com',password='student',user_type = '3')
    response = client.get(ENDPOINT)
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 2


@pytest.mark.django_db
def test_create_admin(client,user):
    client.force_authenticate(user=user)
    ENDPOINT = 'http://127.0.0.1:8000/api/create_admin'
    payload = {
        "name" : "admin",
        "password" : "admin",
        "user_type" : "3",
        "address" : "1130/29A krishna colony",
        "gender" : "Female",
        "username" : "khyati1311.arora@gmail.com"
    }

    response = client.post(ENDPOINT,data=payload,format='json')
    response_data = response.json() 
    assert response.status_code == 201
    assert response_data['name'] == 'admin'

@pytest.mark.django_db
def test_create_admin_again(client,user):
    client.force_authenticate(user=user)
    ENDPOINT = 'http://127.0.0.1:8000/api/create_admin'
    payload = {
        "name" : "admin",
        "password" : "admin",
        "user_type" : "3",
        "address" : "1130/29A krishna colony",
        "gender" : "Female",
        "username" : "khyati1311.arora@gmail.com"
    }
    response = client.post(ENDPOINT,data=payload,format='json')
    response1 = client.post(ENDPOINT,data=payload,format='json')
    
    assert response1.status_code == 400
      
@pytest.mark.django_db
def test_create_admin_invalid_data(client,user):
    client.force_authenticate(user=user)
    ENDPOINT = 'http://127.0.0.1:8000/api/create_admin'
    payload = {
        "name" : "admin",
        "password" : "admin",
        "user_type" : 3,
        "address" : "1130/29A krishna colony",
        "gender" : "Female",
        "username" : "khyati1311.arora@gmail.com"
    }

    response = client.post(ENDPOINT,data=payload,format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_update_admin(client,user):
    client.force_authenticate(user=user)
    admin = CustomUser.objects.create(username = 'student1@gmail.com',password='student',user_type = '3',address='abc')
    ENDPOINT = f'http://127.0.0.1:8000/api/update_admin/{admin.username}' 

    payload = {
        'address' : 'abcd'
    }
    response = client.put(ENDPOINT,data=payload,format = 'json')
    response_data = response.json()
    assert response.status_code == 200
    assert response_data == "Update successful"

@pytest.mark.django_db
def test_update_admin_without_payload(client,user):
    client.force_authenticate(user=user)
    admin = CustomUser.objects.create(username = 'student1@gmail.com',password='student',user_type = '3',address='abc')
    ENDPOINT = f'http://127.0.0.1:8000/api/update_admin/{admin.username}' 
    payload = {
        
    }
    response = client.put(ENDPOINT,data=payload,format = 'json')
    response_data = response.json()
    assert response.status_code == 400
     
    
@pytest.mark.django_db
def test_delete_admin(client,user):
    client.force_authenticate(user=user)
    admin = CustomUser.objects.create(username = 'student1@gmail.com',password='student',user_type = '3',address='abc')
    ENDPOINT = f'http://127.0.0.1:8000/api/delete_admin/{admin.username}' 
    response = client.delete(ENDPOINT)
    assert response.status_code == 204
    assert CustomUser.objects.filter(username=admin.username).count() == 0