from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .serializers import CustomUserSerializer
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated
from .permissions import AdminUser

def allFieldsCheck(data):
   return all(isinstance(value, str) for value in data.values()) 

@permission_classes([IsAuthenticated,AdminUser])
@api_view(['POST'])
def create_admin(request):
    data = request.data
    if allFieldsCheck(data)==False:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
         serializer.save()
         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated,AdminUser])
@api_view(['GET'])
def get_admin(request):
    try:
     admin = CustomUser.objects.filter(user_type='3')
     serializer = CustomUserSerializer(admin, many=True)
     return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@permission_classes([IsAuthenticated,AdminUser])    
@api_view(['PUT'])    
def update_admin(request,username):
     try:
        admin = CustomUser.objects.get(username=username)
        data = request.data
        if 'address' in data :
            admin.address = data['address']
        else:
            return Response({'message' : 'Data not found'}, status=status.HTTP_400_BAD_REQUEST)    
        admin.save()
        return Response("Update successful")
     except Exception as e:
         return Response('Update unsucessful')

@permission_classes([IsAuthenticated,AdminUser])     
@api_view(['DELETE'])
def delete_admin(request,username):
    try:
        admin = CustomUser.objects.get(username=username)
        admin.delete()
        return Response({"message": "Delete successful"}, status=status.HTTP_204_NO_CONTENT)
    except CustomUser.DoesNotExist:
        return Response({'error': 'Admin not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

     

     

 

    
    



           


