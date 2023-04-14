from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from .models import *

#User = get_user_model()


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'is_teacher', 'is_student', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'name': {'required': True}
        }


#    def validate(self, attrs):
#        user = User.objects.filter(email=attrs['username']).first()
#        if not user or not user.check_password(attrs['password']):
#            raise serializers.ValidationError('Invalid name or password')
#        return attrs

class RegisterUserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['email', 'name', 'is_teacher', 'is_student', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
#        user.set_password(validated_data['password'])
#        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Incorrect user or password')


class TeacherSerializer(ModelSerializer):
    #user = UserSerializer()

    class Meta:
        model = TeacherAccount
        fields = '__all__'

    #def create(self, validated_data):
    #    user_data = validated_data.pop('user')
    #    user = User.objects.create_user(**user_data, is_teacher=True)
    #    teacher = TeacherAccount.objects.create(user=user, **validated_data)
    #    return teacher


class StudentSerializer(ModelSerializer):
    #user = UserSerializer()

    class Meta:
        model = StudentAccount
        fields = '__all__'

    #def create(self, validated_data):
    #    user_data = validated_data.pop('user')
    #    user = User.objects.create_user(**user_data, is_student=True)
    #    student = StudentAccount.objects.create(user=user, **validated_data)
    #    return student


class SubjectSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class ScheduleSerializer(ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class ResultsSerializer(ModelSerializer):
    #first_name = serializers.CharField(source='student.first_name')
    #last_name = serializers.CharField(source='student.last_name')
    #subject_name = serializers.CharField(source='subject.name')
    student = StudentSerializer()
    subject = SubjectSerializer()

    class Meta:
        model = Result
        fields = ('id', 'score', 'student', 'subject')






