import logging
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from .serializers import AttendanceSerializer, AttendanceGetSerializer
from .models import Attendance
from .permissions import StaffOrAdminUser


logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([IsAuthenticated, StaffOrAdminUser])
def create_attendance(request):
        logger.info('Create attendance called')
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save()
                logger.info('Attendance created successfully')
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f'Error creating attendance: {e}')
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        logger.warning('Invalid data provided for creating attendance')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_attendance_course(request, course_id):
    logger.info(f'Get attendance for course {course_id} called')
    try:
        attendance = Attendance.objects.filter(course_id=course_id)
        if attendance.exists():
            serializer = AttendanceGetSerializer(attendance, many=True)
        else:
            logger.warning(f'No attendance records found for course {course_id}')
            return Response({'error': 'No attendance records found.'}, status=status.HTTP_404_NOT_FOUND)
        logger.info(f'Attendance records retrieved for course {course_id}')
        return Response(serializer.data)
    except Exception as e:
        logger.error(f'Error retrieving attendance for course {course_id}: {e}')
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_attendance(request, course_id, student_id):
    logger.info(f'Get attendance for course {course_id} and student {student_id} called')
    try:
        attendance = Attendance.objects.filter(course_id=course_id, student_id=student_id)
        if attendance.exists():
            serializer = AttendanceGetSerializer(attendance, many=True)
        else:
            logger.warning(f'No attendance records found for course {course_id} and student {student_id}')
            return Response({'error': 'No attendance records found.'}, status=status.HTTP_404_NOT_FOUND)
        logger.info(f'Attendance records retrieved for course {course_id} and student {student_id}')
        return Response(serializer.data)
    except Exception as e:
        logger.error(f'Error retrieving attendance for course {course_id} and student {student_id}: {e}')
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([IsAuthenticated, StaffOrAdminUser])
def update_attendance(request, course_id, student_id):
    logger.info(f'Update attendance for course {course_id} and student {student_id} called')
    try:
        attendance = Attendance.objects.get(course_id=course_id, student_id=student_id, date=timezone.now().date())
    except ObjectDoesNotExist:
        logger.warning(f'Attendance record not found for course {course_id} and student {student_id}')
        return Response({'error': 'Attendance record not found.'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    if not isinstance(data.get('status'), str):
        logger.warning(f'Invalid status type provided for course {course_id} and student {student_id}')
        return Response({'message': ['Status must be a string.']}, status=status.HTTP_400_BAD_REQUEST)
    if 'status' in data:
        attendance.status = data['status']
    else:
        logger.warning(f'No status data provided for course {course_id} and student {student_id}')
        return Response({'message': 'Data not sent'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        attendance.save()
        logger.info(f'Attendance updated successfully for course {course_id} and student {student_id}')
        return Response("Updated successfully")
    except Exception as e:
        logger.error(f'Error updating attendance for course {course_id} and student {student_id}: {e}')
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, StaffOrAdminUser])
def delete_attendance(request, course_id, student_id):
    logger.info(f'Delete attendance for course {course_id} and student {student_id} called')
    try:
        attendance = Attendance.objects.get(course_id=course_id, student_id=student_id)
    except ObjectDoesNotExist:
        logger.warning(f'Attendance record not found for course {course_id} and student {student_id}')
        return Response({'error': 'Attendance record not found.'}, status=status.HTTP_404_NOT_FOUND)

    try:
        attendance.delete()
        logger.info(f'Attendance deleted successfully for course {course_id} and student {student_id}')
        return Response("Deleted successfully", status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logger.error(f'Error deleting attendance for course {course_id} and student {student_id}: {e}')
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)