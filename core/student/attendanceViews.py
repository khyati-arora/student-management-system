from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from .serializers import AttendanceSerializer, AttendanceGetSerializer

from .models import Attendance
from .permissions import StaffOrAdminUser


@api_view(['POST'])
@permission_classes([IsAuthenticated, StaffOrAdminUser])
def create_attendance(request):
  
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_attendance_course(request, course_id):
    try:
        attendance = Attendance.objects.filter(course_id=course_id)
        if attendance.exists():
            serializer = AttendanceGetSerializer(attendance, many=True)
        else:
            return Response({'error': 'No attendance records found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_attendance(request, course_id, student_id):
    try:
        attendance = Attendance.objects.filter(course_id=course_id, student_id=student_id, status="Present")
        if attendance.exists():
            serializer = AttendanceGetSerializer(attendance, many=True)
        else:
            return Response({'error': 'No attendance records found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, StaffOrAdminUser])
def update_attendance(request, course_id, student_id):
    
    try:
        attendance = Attendance.objects.get(course_id=course_id, student_id=student_id, date=timezone.now().date())
    except ObjectDoesNotExist:
        return Response({'error': 'Attendance record not found.'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    if not isinstance(data.get('status'), str):
                return Response({'message': ['Status must be a string.']}, status=status.HTTP_400_BAD_REQUEST)
    if 'status' in data:
        attendance.status = data['status']
    else :
        return Response({'message' : 'Data not sent'} , status=status.HTTP_400_BAD_REQUEST)    

    try:
        attendance.save()
        return Response("Updated successfully")
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, StaffOrAdminUser])
def delete_attendance(request, course_id, student_id):
    try:
        attendance = Attendance.objects.get(course_id=course_id, student_id=student_id)
    except ObjectDoesNotExist:
        return Response({'error': 'Attendance record not found.'}, status=status.HTTP_404_NOT_FOUND)

    try:
        attendance.delete()
        return Response("Deleted successfully",status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
