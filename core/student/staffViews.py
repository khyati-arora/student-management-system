import logging
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from .serializers import CustomUserSerializer, StaffSerializer, StaffGetSerializer
from .models import Staffs, CustomUser
from rest_framework.permissions import IsAuthenticated
from .permissions import AdminUser, StaffOrAdminUser

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
    return isinstance(data['salary'], str) and isinstance(data['course'], int)

@api_view(['POST'])
@permission_classes([IsAuthenticated, AdminUser])
def create_staff(request):
    logger.info('Create staff called')
    if request.method == 'POST':
        data = request.data
        if not validateUser(data['basic_details']) or not validateStudent(data):
            logger.warning('Validation error: invalid input data')
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        admin_data = request.data.pop('basic_details')
        user_serializer = CustomUserSerializer(data=admin_data)
        
        if user_serializer.is_valid():
            try:
                admin_user = user_serializer.save()
                if admin_user:
                    id = getUserID(admin_data['username'])
                    if id:
                        request.data['basic_details'] = id
                        serializer = StaffSerializer(data=request.data)
                        if serializer.is_valid():
                            serializer.save()
                            logger.info(f'Staff created successfully with User ID {id}')
                            return Response(serializer.data, status=status.HTTP_201_CREATED)
                        else:
                            admin_user.delete()
                            logger.warning('Validation error: staff serializer errors')
                            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    logger.error('Failed to retrieve user ID after creating CustomUser')
                    return Response({'error': 'Failed to retrieve user ID.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                logger.error(f'Error creating staff: {e}')
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        logger.warning('Validation error: CustomUser serializer errors')
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated, StaffOrAdminUser])
def staff_list(request):
    logger.info('Retrieve staff list called')
    try:
        staffs = Staffs.objects.all()
        serializer = StaffGetSerializer(staffs, many=True)
        logger.info('Staff list retrieved successfully')
        return Response(serializer.data)
    except Exception as e:
        logger.error(f'Error retrieving staff list: {e}')
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated, StaffOrAdminUser])
def staff_get(request, staff_id):
    logger.info(f'Retrieve staff details called for staff_id {staff_id}')
    try:
        staff = Staffs.objects.get(id=staff_id)
        serializer = StaffGetSerializer(staff)
        logger.info(f'Staff details retrieved successfully for staff_id {staff_id}')
        return Response(serializer.data)
    except ObjectDoesNotExist:
        logger.warning(f'Staff with id {staff_id} not found')
        return Response({'error': 'Staff not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f'Error retrieving staff details for staff_id {staff_id}: {e}')
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, AdminUser])
def staff_delete(request, staff_id):
    logger.info(f'Delete staff called for staff_id {staff_id}')
    try:
        staff = Staffs.objects.get(id=staff_id)
        custom_user = staff.basic_details
        staff.delete()
        custom_user.delete()
        logger.info(f'Staff and CustomUser deleted successfully for staff_id {staff_id}')
        return Response({"message": "Delete successful"}, status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist:
        logger.warning(f'Staff with id {staff_id} not found')
        return Response({'error': 'Staff not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f'Error deleting staff for staff_id {staff_id}: {e}')
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([IsAuthenticated, StaffOrAdminUser])
def update_staff(request, staff_id):
    logger.info(f'Update staff called for staff_id {staff_id}')
    try:
        staff = Staffs.objects.get(id=staff_id)
        custom_user = staff.basic_details
        data = request.data
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
        if 'salary' in data:
            if not isinstance(data.get('salary'), str) or data['salary'] == staff.salary:
                logger.warning('Validation error: invalid salary input')
                return Response({'salary': ['Invalid input provided']}, status=status.HTTP_400_BAD_REQUEST)
            staff.salary = data['salary']
            flag = True

        if not flag:
            logger.warning('Validation error: no valid data found for update')
            return Response({'message': 'Data not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        custom_user.save()
        staff.save()
        logger.info(f'Staff updated successfully for staff_id {staff_id}')
        return Response({"message": "Updated successfully"}, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        logger.warning(f'Staff with id {staff_id} not found')
        return Response({'error': 'Staff not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f'Error updating staff for staff_id {staff_id}: {e}')
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
