from rest_framework.test import APIClient;
import pytest;  
from ..models import CustomUser, Staffs, Course

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user(db):
    user = CustomUser.objects.create(username = 'username',password='password',user_type = '3')
    return user

@pytest.mark.django_db  
def test_get_staff(client,user):  
    ENDPOINT = 'http://127.0.0.1:8000/api/get_staff'
    client.force_authenticate(user=user)
    course = Course.objects.create(course_name = "c")
    user_student = CustomUser.objects.create(username = 'staff@gmail.com',password='staff',user_type = '1')
    Staffs.objects.create(basic_details = user_student, course = course)
    response = client.get(ENDPOINT)
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1

@pytest.mark.django_db  
def test_add_staff(client,user):
     ENDPOINT = 'http://127.0.0.1:8000/api/create_staff' 
     client.force_authenticate(user=user)
     course = Course.objects.create(course_name = "c")
     payload = {
        "basic_details" : {
            "password" : "Khyati",
            "user_type" : "1",
            "address" : "354",
            "gender" : "Female",
            "username" : "khyati2005.arora@gmail.com",
            "name" : "Khyati"
        },
        "course" : course.id,
        "salary" : "30000"
     }  
     response = client.post(ENDPOINT,data=payload,format='json')
     response_data = response.json()
     assert response.status_code == 201
     assert response_data['course'] == course.id

@pytest.mark.django_db  
def test_add_staff_missing_fields(client,user):
     ENDPOINT = 'http://127.0.0.1:8000/api/create_staff' 
     client.force_authenticate(user=user)
     course = Course.objects.create(course_name = "c")
     payload = {
        "basic_details" : {
            "password" : "Khyati",
            "user_type" : "1",
            "address" : "354",
            "gender" : "Female",
            "name" : "Khyati"
            
        },
        "course" : course.id,
        "salary" : "30000"
     }  
     response = client.post(ENDPOINT,data=payload,format='json')
     assert response.status_code == 400

@pytest.mark.django_db  
def test_add_staff_missing_fields(client,user):
     ENDPOINT = 'http://127.0.0.1:8000/api/create_staff' 
     client.force_authenticate(user=user)
     course = Course.objects.create(course_name = "c")
     payload = {
        "basic_details" : {
            "password" : "Khyati",
            "user_type" : "1",
            "address" : 354,
            "gender" : "Female",
            "name" : "Khyati"
            
        },
        "course" : course.id,
        "salary" : "30000"
     }  
     response = client.post(ENDPOINT,data=payload,format='json')
     assert response.status_code == 400     
         
@pytest.mark.django_db  
def test_update_staff(client,user):
    client.force_authenticate(user=user)
    course = Course.objects.create(course_name = "c")
    user_staff = CustomUser.objects.create(username = 'staff@gmail.com',password='staff',user_type = '1')
    staff = Staffs.objects.create(basic_details = user_staff, course = course)
    course1 = Course.objects.create(course_name = "Jdk")
    ENDPOINT = f'http://127.0.0.1:8000/api/update_staff/{staff.id}' 
    payload = {
        "salary" : "50000"
    }

    response = client.put(ENDPOINT,data=payload,format = 'json')
    response_data = response.json()
    assert response.status_code == 200
    assert response_data['message'] == 'Updated successfully' 

@pytest.mark.django_db  
def test_update_staff_invalid(client,user):
    client.force_authenticate(user=user)
    course = Course.objects.create(course_name = "c")
    user_staff = CustomUser.objects.create(username = 'staff@gmail.com',password='staff',user_type = '1')
    staff = Staffs.objects.create(basic_details = user_staff, course = course)
    course1 = Course.objects.create(course_name = "Jdk")
    ENDPOINT = f'http://127.0.0.1:8000/api/update_staff/{staff.id}' 
    payload = {
       
    }

    response = client.put(ENDPOINT,data=payload,format = 'json')
    response_data = response.json()
    assert response.status_code == 400
  
@pytest.mark.django_db  
def test_update_staff_invalid_type(client,user):
    client.force_authenticate(user=user)
    course = Course.objects.create(course_name = "c")
    user_staff = CustomUser.objects.create(username = 'staff@gmail.com',password='staff',user_type = '1')
    staff = Staffs.objects.create(basic_details = user_staff, course = course)
    course1 = Course.objects.create(course_name = "Jdk")
    ENDPOINT = f'http://127.0.0.1:8000/api/update_staff/{staff.id}' 
    payload = {
        "salary" : 50000
    }

    response = client.put(ENDPOINT,data=payload,format = 'json')

    assert response.status_code == 400
    

def test_delete_student(client,user):
    client.force_authenticate(user=user)
    course = Course.objects.create(course_name = "c")
    user_staff = CustomUser.objects.create(username = 'staff@gmail.com',password='staff',user_type = '1')
    staff = Staffs.objects.create(basic_details = user_staff, course = course)
    ENDPOINT = f'http://127.0.0.1:8000/api/delete_staff/{staff.id}' 

    response = client.delete(ENDPOINT)
    assert response.status_code == 204
    assert Staffs.objects.filter(id=staff.id).count() == 0
    assert CustomUser.objects.filter(id=user_staff.id).count() == 0  

