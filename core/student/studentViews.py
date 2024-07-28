import logging
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import CustomUserSerializer, StudentSerializer, StudentGetSerializer
from .models import Students, CustomUser
from rest_framework.permissions import IsAuthenticated
from .permissions import StaffOrAdminUser
from rest_framework.exceptions import NotFound, ValidationError

# Initialize the logger
logger = logging.getLogger(__name__)

def getUserID(username):
    try:
        user = CustomUser.objects.get(username=username)
        return user.id
    except CustomUser.DoesNotExist:
        logger.warning(f'CustomUser with username {username} does not exist')
        return None

def validateUser(data):
    return all(isinstance(value, str) for value in data.values())

def validateStudent(data):
    return isinstance(data, str)

@api_view(['POST'])
@permission_classes([IsAuthenticated, StaffOrAdminUser])
def create_student(request):
    logger.info('Create student called')
    if request.method == 'POST':
        data = request.data
        logger.debug(f'Received data: {data}')
        if not validateUser(data['basic_details']) or not validateStudent(data['guardian']):
            logger.warning('Validation error: invalid input data')
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            admin_data = request.data.pop('basic_details')
            user_serializer = CustomUserSerializer(data=admin_data)
            
            if user_serializer.is_valid():
                admin_user = user_serializer.save()
                if admin_user:
                    id = getUserID(admin_data['username'])
                    request.data['basic_details'] = id
                    serializer = StudentSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        logger.info(f'Student created successfully with user ID {id}')
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        admin_user.delete()
                        logger.warning('Validation error: student serializer errors')
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                logger.warning('Validation error: CustomUser serializer errors')
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Error creating student: {e}')
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_list(request):
    logger.info('Retrieve student list called')
    try:
        students = Students.objects.all()
        serializer = StudentGetSerializer(students, many=True)
        logger.info('Student list retrieved successfully')
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f'Error retrieving student list: {e}')
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_get(request, student_id):
    logger.info(f'Retrieve student details called for student_id {student_id}')
    try:
        student = Students.objects.get(id=student_id)
        serializer = StudentGetSerializer(student)
        logger.info(f'Student details retrieved successfully for student_id {student_id}')
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Students.DoesNotExist:
        logger.warning(f'Student with id {student_id} not found')
        raise NotFound(detail="Student not found")
    except Exception as e:
        logger.error(f'Error retrieving student details for student_id {student_id}: {e}')
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, StaffOrAdminUser])
def student_delete(request, student_id):
    logger.info(f'Delete student called for student_id {student_id}')
    try:
        student = Students.objects.get(id=student_id)
        custom_user = student.basic_details
        student.delete()
        custom_user.delete()
        logger.info(f'Student and CustomUser deleted successfully for student_id {student_id}')
        return Response({'message': 'Delete successful'}, status=status.HTTP_204_NO_CONTENT)
    except Students.DoesNotExist:
        logger.warning(f'Student with id {student_id} not found')
        raise NotFound(detail="Student not found")
    except Exception as e:
        logger.error(f'Error deleting student for student_id {student_id}: {e}')
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([IsAuthenticated, StaffOrAdminUser])
def update_student(request, student_id):
    logger.info(f'Update student called for student_id {student_id}')
    try:
        student = Students.objects.get(id=student_id)
        custom_user = student.basic_details
        data = request.data
        logger.debug(f'Received data for update: {data}')
        flag = False

        if 'username' in data:
            if not isinstance(data.get('username'), str) or data['username'] == custom_user.username:
                logger.warning('Validation error: invalid username input')
                return Response({'username': ['Invalid input provided']}, status=status.HTTP_400_BAD_REQUEST)
            custom_user.username = data['username']
            flag = True

        if 'address' in data:
            if not isinstance(data.get('address'), str) or data['address'] == custom_user.address:
                logger.warning('Validation error: invalid address input')
                return Response({'address': ['Invalid input provided']}, status=status.HTTP_400_BAD_REQUEST)
            custom_user.address = data['address']
            flag = True

        if 'guardian' in data:
            if not isinstance(data.get('guardian'), str) or data['guardian'] == student.guardian:
                logger.warning('Validation error: invalid guardian input')
                return Response({'guardian': ['Invalid input provided']}, status=status.HTTP_400_BAD_REQUEST)
            student.guardian = data['guardian']
            flag = True

        if not flag:
            logger.warning('Validation error: no valid data found for update')
            return Response({'message': 'Payload missing'}, status=status.HTTP_400_BAD_REQUEST)

        custom_user.save()
        student.save()
        logger.info(f'Student updated successfully for student_id {student_id}')
        return Response({'message': 'Updated successfully'}, status=status.HTTP_200_OK)
    except Students.DoesNotExist:
        logger.warning(f'Student with id {student_id} not found')
        raise NotFound(detail="Student not found")
    except ValidationError as e:
        logger.error(f'Validation error: {e}')
        return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f'Error updating student for student_id {student_id}: {e}')
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_student(request, name):
    logger.info(f'Search student called with name {name}')
    if name:
        students = CustomUser.objects.filter(name__icontains=name, user_type='2')
        serializer = CustomUserSerializer(students, many=True)
        logger.info(f'Students search results retrieved successfully for name {name}')
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        logger.warning('Search name is missing or empty')
        return Response({'message': 'No data found'}, status=status.HTTP_400_BAD_REQUEST)

    
   
    
     

