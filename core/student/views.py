import logging
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import CustomUserSerializer, CustomUserGetSerializer
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated
from .permissions import AdminUser

# Initialize the logger
logger = logging.getLogger(__name__)

def allFieldsCheck(data):
   return all(isinstance(value, str) for value in data.values())

@permission_classes([IsAuthenticated, AdminUser])
@api_view(['POST'])
def create_admin(request):
    logger.info('Create admin called')
    data = request.data
    if not allFieldsCheck(data):
        logger.warning('Validation error: invalid input data')
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        logger.info(f'Admin created successfully with username {data.get("username")}')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    logger.warning('Validation error: CustomUser serializer errors')
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated, AdminUser])
@api_view(['GET'])
def get_admin(request):
    logger.info('Get admin called')
    try:
        admin = CustomUser.objects.filter(user_type='3')
        serializer = CustomUserGetSerializer(admin, many=True)
        logger.info('Admin list retrieved successfully')
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f'Error retrieving admin list: {e}')
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@permission_classes([IsAuthenticated, AdminUser])    
@api_view(['PUT'])    
def update_admin(request, username):
    logger.info(f'Update admin called for username {username}')
    try:
        admin = CustomUser.objects.get(username=username)
        data = request.data
        
        if 'address' in data:
            admin.address = data['address']
        else:
            logger.warning('Validation error: address not provided')
            return Response({'message': 'Data not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        admin.save()
        logger.info(f'Admin updated successfully for username {username}')
        return Response("Update successful")
    except CustomUser.DoesNotExist:
        logger.warning(f'Admin with username {username} not found')
        return Response({'error': 'Admin not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f'Error updating admin for username {username}: {e}')
        return Response('Update unsuccessful', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@permission_classes([IsAuthenticated, AdminUser])     
@api_view(['DELETE'])
def delete_admin(request, username):
    logger.info(f'Delete admin called for username {username}')
    try:
        admin = CustomUser.objects.get(username=username)
        admin.delete()
        logger.info(f'Admin deleted successfully for username {username}')
        return Response({"message": "Delete successful"}, status=status.HTTP_204_NO_CONTENT)
    except CustomUser.DoesNotExist:
        logger.warning(f'Admin with username {username} not found')
        return Response({'error': 'Admin not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f'Error deleting admin for username {username}: {e}')
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


     

     

 

    
    



           


