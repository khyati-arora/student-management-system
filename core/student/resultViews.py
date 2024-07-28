import logging
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import ResultSerializer
from .models import Results, Course, Students
from rest_framework.permissions import IsAuthenticated
from .permissions import StaffOrAdminUser
from rest_framework.exceptions import NotFound, ValidationError

# Initialize the logger
logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([IsAuthenticated, StaffOrAdminUser])
def create_result(request):
    logger.info('Create result called')
    serializer = ResultSerializer(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info('Result created successfully')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        logger.warning(f'Validation error: {serializer.errors}')
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f'Error creating result: {e}')
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_result(request):
    logger.info('Get results called')
    try:
        results = Results.objects.all()
        serializer = ResultSerializer(results, many=True)
        logger.info('Results retrieved successfully')
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f'Error retrieving results: {e}')
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_result_id(request, course_id, student_id):
    logger.info(f'Get result for course {course_id} and student {student_id} called')
    try:
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            logger.warning(f'Course {course_id} not found')
            raise NotFound(detail="Course not found")

        try:
            student = Students.objects.get(id=student_id)
        except Students.DoesNotExist:
            logger.warning(f'Student {student_id} not found')
            raise NotFound(detail="Student not found")

        result = Results.objects.get(course_id=course_id, student_id=student_id)
        serializer = ResultSerializer(result)
        logger.info(f'Result for course {course_id} and student {student_id} retrieved successfully')
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Results.DoesNotExist:
        logger.warning(f'Result for course {course_id} and student {student_id} not found')
        raise NotFound(detail="Result not found")
    except Exception as e:
        logger.error(f'Error retrieving result for course {course_id} and student {student_id}: {e}')
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([IsAuthenticated, StaffOrAdminUser])
def update_result(request, course_id, student_id):
    logger.info(f'Update result for course {course_id} and student {student_id} called')
    try:
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            logger.warning(f'Course {course_id} not found')
            raise NotFound(detail="Course not found")

        try:
            student = Students.objects.get(id=student_id)
        except Students.DoesNotExist:
            logger.warning(f'Student {student_id} not found')
            raise NotFound(detail="Student not found")

        result = Results.objects.get(course_id=course_id, student_id=student_id)
        data = request.data

        if 'grade' in data:
            result.grade = data['grade']
            result.save()
            logger.info(f'Result for course {course_id} and student {student_id} updated successfully')
            return Response({'message': 'Updated successfully'}, status=status.HTTP_200_OK)
        else:
            logger.warning(f'Data not found for updating result for course {course_id} and student {student_id}')
            return Response({'message': 'Data not found'}, status=status.HTTP_400_BAD_REQUEST)

    except Results.DoesNotExist:
        logger.warning(f'Result for course {course_id} and student {student_id} not found')
        raise NotFound(detail="Result not found")
    except Exception as e:
        logger.error(f'Error updating result for course {course_id} and student {student_id}: {e}')
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, StaffOrAdminUser])
def delete_result(request, course_id, student_id):
    logger.info(f'Delete result for course {course_id} and student {student_id} called')
    try:
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            logger.warning(f'Course {course_id} not found')
            raise NotFound(detail="Course not found")

        try:
            student = Students.objects.get(id=student_id)
        except Students.DoesNotExist:
            logger.warning(f'Student {student_id} not found')
            raise NotFound(detail="Student not found")

        result = Results.objects.get(course_id=course_id, student_id=student_id)
        result.delete()
        logger.info(f'Result for course {course_id} and student {student_id} deleted successfully')
        return Response({'message': 'Deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Results.DoesNotExist:
        logger.warning(f'Result for course {course_id} and student {student_id} not found')
        raise NotFound(detail="Result not found")
    except Exception as e:
        logger.error(f'Error deleting result for course {course_id} and student {student_id}: {e}')
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
