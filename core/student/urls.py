from django.urls import path
from .staffViews import create_staff, staff_delete,staff_list,update_staff,staff_get
from .studentViews import create_student,student_list,student_delete,update_student,student_get
from .courseViews import create_course,course_update,course_delete,get_courses,get_course
from .resultViews import create_result,get_result,delete_result,update_result,get_result_id
from .attendanceViews import create_attendance,get_attendance,delete_attendance,update_attendance,get_attendance_course
from .views import create_admin,get_admin,update_admin,delete_admin

urlpatterns = [
    path('api/create_staff', create_staff),
    path('api/create_student', create_student),
    path('api/get_student',student_list),
    path('api/get_staff',staff_list),
    path('api/delete_staff/<int:staff_id>',staff_delete),
    path('api/delete_student/<int:student_id>',student_delete),
    path('api/update_staff/<int:staff_id>',update_staff),
    path('api/create_course',create_course),
    path('api/get_course',get_courses),
    path('api/delete_course/<int:course_id>',course_delete),
    path('api/update_course/<int:course_id>',course_update),
    path('api/update_student/<int:student_id>',update_student),
    path('api/create_result',create_result),
    path('api/get_result',get_result),
    path('api/update_result/<int:course_id>/<int:student_id>',update_result),
    path('api/delete_result/<int:course_id>/<int:student_id>',delete_result),
    path('api/create_attendance',create_attendance),
    path('api/get_attendance/<int:course_id>/<int:student_id>',get_attendance),
    path('api/update_attendance/<int:course_id>/<int:student_id>',update_attendance),
    path('api/delete_attendance/<int:course_id>/<int:student_id>',delete_attendance),
    path('api/create_admin',create_admin),
    path('api/get_staff/<int:staff_id>',staff_get),
    path('api/get_student/<int:student_id>',student_get),
    path('api/get_course/<int:course_id>',get_course),
    path('api/get_result/<int:course_id>/<int:student_id>',get_result_id),
    path('api/get_attendance/<int:course_id>',get_attendance_course),
    path('api/get_admin',get_admin),
    path('api/update_admin/<username>',update_admin),
    path('api/delete_admin/<username>',delete_admin)
]