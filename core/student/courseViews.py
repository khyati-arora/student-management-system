import logging
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import CourseSerializer, CourseGetSerializer
from .models import Course
from rest_framework.permissions import IsAuthenticated
from .permissions import AdminUser, StaffOrAdminUser
from django.core.exceptions import ObjectDoesNotExist


logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([IsAuthenticated, AdminUser])
def create_course(request):
    logger.info('Create course called')
    data = request.data
    if not isinstance(data.get('course_name'), str):
        logger.warning('Invalid course_name type provided')
        return Response({'course_name': ['Course name must be a string.']}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = CourseSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            logger.info('Course created successfully')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f'Error creating course: {e}')
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    logger.warning('Invalid data provided for creating course')
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_courses(request):
    logger.info('Get courses called')
    try:
        courses = Course.objects.all()
        serializer = CourseGetSerializer(courses, many=True)
        logger.info('Courses retrieved successfully')
        return Response(serializer.data)
    except Exception as e:
        logger.error(f'Error retrieving courses: {e}')
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_course(request, course_id):
    logger.info(f'Get course {course_id} called')
    try:
        course = Course.objects.get(id=course_id)
        serializer = CourseGetSerializer(course)
        logger.info(f'Course {course_id} retrieved successfully')
        return Response(serializer.data)
    except ObjectDoesNotExist:
        logger.warning(f'Course {course_id} not found')
        return Response({'error': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f'Error retrieving course {course_id}: {e}')
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, AdminUser])
def course_delete(request, course_id):
    logger.info(f'Delete course {course_id} called')
    try:
        course = Course.objects.get(id=course_id)
        course.delete()
        logger.info(f'Course {course_id} deleted successfully')
        return Response({"message": "Delete successful"}, status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist:
        logger.warning(f'Course {course_id} not found')
        return Response({'error': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f'Error deleting course {course_id}: {e}')
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([IsAuthenticated, StaffOrAdminUser])
def course_update(request, course_id):
    logger.info(f'Update course {course_id} called')
    try:
        course = Course.objects.get(id=course_id)
        data = request.data
        if 'course_name' in data:
            if not isinstance(data.get('course_name'), str):
                logger.warning(f'Invalid course_name type provided for course {course_id}')
                return Response({'course_name': ['Course name must be a string.']}, status=status.HTTP_400_BAD_REQUEST)
            course.course_name = data['course_name']
            course.save()
            logger.info(f'Course {course_id} updated successfully')
            return Response({"message": "Updated successfully"}, status=status.HTTP_200_OK)
        else:
            logger.warning(f'Missing field course_name for course {course_id}')
            return Response({"message": "Missing field course_name"}, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        logger.warning(f'Course {course_id} not found')
        return Response({'error': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f'Error updating course {course_id}: {e}')
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
