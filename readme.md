# Student Management System 

This is a django web application that allows to manage students, staffs and admins and make the entire process hassle free.

Features : 

Students : 
1. Add student 
2. Get students
3. Get student with a specific id
4. Update student 
5. Delete student

Staff : 
1. Add staff
2. Get staff
3. Get staff with a specific id
4. Update Staff
5. Delete staff

Admin :
1. Add admin
2. Get list of admins
3. Update admin details
4. Delete admin

Courses :
1. Add course
2. Update course
3. Get all courses
4. Delte course

Attendance :
1. View attendance of a student enrolled in a course
2. Add attendance
3. Update attendance
4. Delete attendance

Results :
1. View grade of a student enrolled in a course
2. Update result
3. Add result
4. Delete result

All these features require the user to be authenticated. Some of these also need special permissions like the user needs to be an admin or staff to perform them.

### Project Setup :

Prerequisites : 
1. Python
2. Postgres

Installation steps :

1. Clone the repository :
```
git clone https://github.com/yourusername/student-management-system.git
cd student-management-system
```

2. Create and activate the virtual environment :
```
python -m venv venv
. venv/bin/activate
```

3. Installing required dependencies : 
```
pip install -r requirements.txt
```

4. Configure database :
```
cd core
Create a .env file and set these properties according to your postgres database:

DB_NAME = 'db name'
USERNAME = 'username'
PASSWORD = 'password'
```

5. Create and apply Migrations : 
```
python manage.py makemigrations
python manage.py migrate
```

6. Run the server : 
```
python manage.py runserver
```

### API Endpoints : 

1. **Add staff** : <br>
**ENDPOINT** : /api/create_staff<br>
**METHOD** : POST<br>
**Function** : Adds a new staff to the system 

2. **Get staff list** : <br>
**ENDPOINT** : /api/get_staff<br>
**METHOD** : GET<br>
**Function** : Displays all staff present in the database

3. **Get staff with a specific id** : <br>
**ENDPOINT** : /api/get_staff/{id}<br>
**METHOD** : GET<br>
**Function** : Displays details of a particular staff

4. **Update Staff** : <br>
**ENDPOINT** : /api/update_staff/{id}<br>
**METHOD** : PUT<br>
**Function** : Update details of a particular staff

5. **Delete Staff** : <br>
**ENDPOINT** : /api/delete_staff/{id}<br>
**METHOD** : DELETE<br>
**Function** : Delete details of a particular staff

6. **Add student** : <br>
**ENDPOINT** : /api/create_student<br>
**METHOD** : POST<br>
**Function** : Adds a new student to the system 

7. **Get student list** : <br> 
**ENDPOINT** : /api/get_student<br>
**METHOD** : GET<br>
**Function** : Displays all students present in the database

8. **Get student with a specific id** : <br>
**ENDPOINT** : /api/get_student/{id}<br>
**METHOD** : GET<br>
**Function** : Displays details of a particular student

9. **Update student** : <br>
**ENDPOINT** : /api/update_student/{id}<br>
**METHOD** : PUT<br>
**Function** : Update details of a particular student

10. **Delete student** : <br>
**ENDPOINT** : /api/delete_student/{id}<br>
**METHOD** : DELETE<br>
**Function** : Delete details of a particular student

11. **Add Course** : <br>
**ENDPOINT** : /api/create_course<br>
**METHOD** : POST<br>
**Function** : Adds a new course to the system 

12. **Get courses list** : <br>
**ENDPOINT** : /api/get_course<br>
**METHOD** : GET<br>
**Function** : Displays all courses present in the database

13. **Update course** : <br>
**ENDPOINT** : /api/update_course/{id}<br>
**METHOD** : PUT<br>
**Function** : Update details of a particular course

14. **Delete course** : <br>
**ENDPOINT** : /api/delete_course/{id}<br>
**METHOD** : DELETE<br>
**Function** : Delete details of a particular course

15. **Add result** : <br>
**ENDPOINT** : /api/create_result<br>
**METHOD** : POST<br>
**Function** : Adds a new result of a student in a course to the system 

16. **Get result** : <br>
**ENDPOINT** : /api/get_result/{course_id}/{student_id}<br>
**METHOD** : GET<br>
**Function** : Displays result of a student

17. **Update result** : <br>
**ENDPOINT** : /api/update_result/{course_id}/{student_id}<br>
**METHOD** : PUT<br>
**Function** : Update details of a particular result

18. **Delete result** : <br>
**ENDPOINT** : /api/delete_result/{course_id}/{student_id}<br>
**METHOD** : DELETE<br>
**Function** : Delete details of a particular result

19. **Add attendance** : <br>
**ENDPOINT** : /api/create_attendance<br>
**METHOD** : POST<br>
**Function** : Adds attendance of a student in a course to the system 

20. **Get attendance** : <br>
**ENDPOINT** : /api/get_attendance/{course_id}/{student_id}<br>
**METHOD** : GET<br>
**Function** : Displays attendance details of a student

21. **Update attendance** : <br>
**ENDPOINT** : /api/update_attendance/{course_id}/{student_id}<br>
**METHOD** : PUT<br>
**Function** : Update attendance status of a particular student

22. **Delete Attendance** : <br>
**ENDPOINT** : /api/delete_attendance/{course_id}/{student_id}<br>
**METHOD** : DELETE<br>
**Function** : Delete particular attendance record

23. **Add admin**: <br>
**ENDPOINT** : /api/create_admin<br>
**METHOD** : POST<br>
**Function** : Adds a new admin

24. **Get admin** : <br>
**ENDPOINT** : /api/get_admin<br>
**METHOD** : GET<br>
**Function** : Displays details of all admins

25. **Update admin** : <br>
**ENDPOINT** : /api/update_admin/{id}<br>
**METHOD** : PUT<br>
**Function** : Update details of a particular admin

26. **Delete admin** : <br>
**ENDPOINT** : /api/delete_admin/{id}<br>
**METHOD** : DELETE<br>
**Function** : Delete details of a particular admin


### Testing
To run tests : 
```
pytest
```


















