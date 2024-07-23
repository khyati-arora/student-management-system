from rest_framework import serializers
from .models import CustomUser, Staffs, Students, Course, Results, Attendance

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'user_type','address','gender','name']
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username = validated_data['username'],
            password=validated_data['password'],
            user_type=validated_data['user_type'],
            address = validated_data['address'],
            gender = validated_data['gender'],
            name = validated_data['name']
            
        )
        return user
    
class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staffs
        fields = ['basic_details', 'salary', 'course']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = ['basic_details','guardian']


class StudentGetSerializer(serializers.ModelSerializer):
    basic_details = CustomUserSerializer()

    class Meta:
        model = Students
        fields = ['id', 'basic_details', 'guardian']

class StaffGetSerializer(serializers.ModelSerializer):
    basic_details = CustomUserSerializer()

    class Meta:
        model = Staffs
        fields = ['id', 'basic_details', 'course_id', "salary"]

class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['course_name']

class CourseGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['id','course_name']

class ResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Results    
        fields = ['student','course','grade']

class AttendanceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Attendance
        fields = ['student','course','status']

class AttendanceGetSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Attendance
        fields = ['student','course','status','date']
