from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import CourseSerializer, CourseGetSerializer
from .models import Course
from rest_framework.permissions import IsAuthenticated
from .permissions import AdminUser, StaffOrAdminUser
from django.core.exceptions import ObjectDoesNotExist

@api_view(['POST'])
@permission_classes([IsAuthenticated, AdminUser])
def create_course(request):
    data = request.data
    if not isinstance(data.get('course_name'), str):
        return Response({'course_name': ['Course name must be a string.']}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = CourseSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_courses(request):
    try:
        courses = Course.objects.all()
        serializer = CourseGetSerializer(courses, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_course(request,course_id):
    try:
        course = Course.objects.get(id = course_id)
        serializer = CourseGetSerializer(course)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, AdminUser])

def course_delete(request, course_id):
    print('delete called')
    try:
        course = Course.objects.get(id=course_id)
        course.delete()
        return Response({"message": "Delete successful"}, status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist:
        return Response({'error': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([IsAuthenticated, StaffOrAdminUser])
def course_update(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        data = request.data
        if 'course_name' in data:
            if not isinstance(data.get('course_name'), str):
                return Response({'course_name': ['Course name must be a string.']}, status=status.HTTP_400_BAD_REQUEST)
            course.course_name = data['course_name']
 
            course.save()
            return Response({"message": "Updated successfully"}, status=status.HTTP_200_OK)
        else : 
            return Response({"message": "Missing field course_name"}, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response({'error': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
