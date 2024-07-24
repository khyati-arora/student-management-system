from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from .serializers import CustomUserSerializer, StaffSerializer, StaffGetSerializer
from .models import Staffs, CustomUser
from rest_framework.permissions import IsAuthenticated
from .permissions import AdminUser, StaffOrAdminUser


def getUserID(username):
    try:
        user = CustomUser.objects.get(username=username)
        return user.id
    except CustomUser.DoesNotExist:
        return None

def validateUser(data):    
   return all(isinstance(value, str) for value in data.values()) 

def validateStudent(data):
   return type(data['salary']) == str  and type(data['course']) == int

@api_view(['POST'])
@permission_classes([IsAuthenticated, AdminUser])
def create_staff(request):
    if request.method == 'POST':
        data = request.data
        if validateUser(data['basic_details']) == False or validateStudent(data) == False:
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
                            return Response(serializer.data, status=status.HTTP_201_CREATED)
                        else:
                            admin_user.delete()
                            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    return Response({'error': 'Failed to retrieve user ID.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated, StaffOrAdminUser])
def staff_list(request):
    try:
        staffs = Staffs.objects.all()
        serializer = StaffGetSerializer(staffs, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated, StaffOrAdminUser])
def staff_get(request,staff_id):
    try:
        staff= Staffs.objects.get(id = staff_id)
        serializer = StaffGetSerializer(staff)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, AdminUser])
def staff_delete(request, staff_id):
    try:
        staff = Staffs.objects.get(id=staff_id)
        custom_user = staff.basic_details
        staff.delete()
        custom_user.delete()
        return Response({"message": "Delete successful"}, status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist:
        return Response({'error': 'Staff not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([IsAuthenticated, StaffOrAdminUser])
def update_staff(request, staff_id):
    try:
        staff = Staffs.objects.get(id=staff_id)
        custom_user = staff.basic_details
        data = request.data
        flag = False
        if 'username' in data:
            if not isinstance(data.get('username'), str):
                return Response({'username': ['User name must be a string.']}, status=status.HTTP_400_BAD_REQUEST)
            custom_user.username = data['username']
            flag = True
        if 'address' in data:
            if not isinstance(data.get('address'), str):
                return Response({'address': ['Address must be a string.']}, status=status.HTTP_400_BAD_REQUEST)
            custom_user.address = data['address']
            flag = True
        if 'salary' in data:
            if not isinstance(data.get('salary'), str):
                return Response({'salary': ['Salary must be a string.']}, status=status.HTTP_400_BAD_REQUEST)
            staff.salary = data['salary']
            flag = True

        if(flag == False):
            return Response({'message' : 'Data not found'}, status=status.HTTP_400_BAD_REQUEST)    
        
        custom_user.save()
        staff.save()
        return Response({"message": "Updated successfully"}, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'error': 'Staff not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
