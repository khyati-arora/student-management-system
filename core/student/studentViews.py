from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import CustomUserSerializer,  StudentSerializer,  StudentGetSerializer
                          
from .models import Students, CustomUser

from rest_framework.permissions import IsAuthenticated
from .permissions import StaffOrAdminUser
from rest_framework.exceptions import NotFound, ValidationError

def getUserID(username):
    try:
        user = CustomUser.objects.get(username=username)
        return user.id
    except CustomUser.DoesNotExist:
        return None

@api_view(['POST'])
@permission_classes([IsAuthenticated, StaffOrAdminUser])
def create_student(request):
    if request.method == 'POST':
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
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_list(request):
    try:
        students = Students.objects.all()
        serializer = StudentGetSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_get(request,student_id):
    try:
        students = Students.objects.get(id = student_id)
        serializer = StudentGetSerializer(students)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, StaffOrAdminUser])
def student_delete(request, student_id):
    try:
        student = Students.objects.get(id=student_id)
        custom_user = student.basic_details
        student.delete()
        custom_user.delete()
        return Response({'message': 'Delete successful'}, status=status.HTTP_204_NO_CONTENT)
    except Students.DoesNotExist:
        raise NotFound(detail="Student not found")
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([IsAuthenticated, StaffOrAdminUser])
def update_student(request, student_id):
    try:
        student = Students.objects.get(id=student_id)
        custom_user = student.basic_details
        data = request.data
        
        if 'username' in data:
            custom_user.username = data['username']

        if 'address' in data:
            custom_user.address = data['address']

        if 'guardian' in data:
            student.guardian = data['guardian']
        
        custom_user.save()
        student.save()
        return Response({'message': 'Updated successfully'}, status=status.HTTP_200_OK)
    except Students.DoesNotExist:
        raise NotFound(detail="Student not found")
    except ValidationError as e:
        return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
