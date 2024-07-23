from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import ResultSerializer
from .models import Results,Course,Students
from rest_framework.permissions import IsAuthenticated
from .permissions import StaffOrAdminUser
from rest_framework.exceptions import NotFound, ValidationError

@api_view(['POST'])
@permission_classes([IsAuthenticated, StaffOrAdminUser])
def create_result(request):
    serializer = ResultSerializer(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_result(request):
    try:
        results = Results.objects.all()
        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_result_id(request,course_id,student_id):
    try:
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise NotFound(detail="Course not found")
        
        try:
            student = Students.objects.get(id=student_id)
        except Students.DoesNotExist:
            raise NotFound(detail="Student not found")
        
        result= Results.objects.get(course_id=course_id,student_id=student_id)
        serializer = ResultSerializer(result)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    

@api_view(['PUT'])
@permission_classes([IsAuthenticated, StaffOrAdminUser])
def update_result(request, course_id, student_id):
    try:

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise NotFound(detail="Course not found")

        # Check if the student exists
        try:
            student = Students.objects.get(id=student_id)
        except Students.DoesNotExist:
            raise NotFound(detail="Student not found")
        
        result = Results.objects.get(course_id=course_id, student_id=student_id)
        data = request.data

        if 'grade' in data:
            result.grade = data['grade']

        result.save()
        return Response({'message': 'Updated successfully'}, status=status.HTTP_200_OK)
    
    except Results.DoesNotExist:
        raise NotFound(detail="Result not found")
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, StaffOrAdminUser])
def delete_result(request, course_id, student_id):
    try:

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise NotFound(detail="Course not found")

        # Check if the student exists
        try:
            student = Students.objects.get(id=student_id)
        except Students.DoesNotExist:
            raise NotFound(detail="Student not found")
        
        result = Results.objects.get(course_id=course_id, student_id=student_id)
        result.delete()
        return Response({'message': 'Deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Results.DoesNotExist:
        raise NotFound(detail="Result not found")
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
