from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .models import *
from .serializers import TeacherSerializer, StudentSerializer, SubjectSerializer, ScheduleSerializer, ResultsSerializer, RegisterUserSerializer, LoginSerializer, UserSerializer
from .permissions import IsStudentReadOnly, IsTeacherReadOnly


class UserRegistrationView(generics.GenericAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        return Response(data, status=status.HTTP_201_CREATED)


class UserLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        serializer = UserSerializer(user)
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        return  Response(data, status=status.HTTP_200_OK)


class UserUpdateView(APIView):
    def put(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        user = User.objects.get(pk=pk)
        if 'password' in request.data:
            user.set_password(request.data['password'])
            user.save()
            return Response('Password updated successfully')
        else:
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    def post(self, request):
        email = request.data.get('email', '')
        user = User.objects.filter(email=email).first()
        if user:
            token_generator = PasswordResetTokenGenerator()
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
            send_mail(
                'Password reset request',
                f'Use this link to reset your password {reset_url}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently = False,
            )
        return Response('Email sent successfully')


class TeacherCreateView(generics.CreateAPIView):
    queryset = TeacherAccount.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = (IsAuthenticated,)


class StudentCreateView(generics.CreateAPIView):
    queryset = StudentAccount.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (IsAuthenticated, )


class StudentListView(generics.ListAPIView):
    queryset = StudentAccount.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (AllowAny, )


class TeacherListView(generics.ListAPIView):
    queryset = TeacherAccount.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = (AllowAny, )


class StudentRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = StudentAccount.objects.all()
    serializer_class = StudentSerializer


class TeacherRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = TeacherAccount.objects.all()
    serializer_class = TeacherSerializer


class SubjectListCreateView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class ScheduleListCreateView(generics.ListCreateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer


class ResultListCreateView(generics.ListCreateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultsSerializer
    permission_classes = [IsTeacherReadOnly | IsStudentReadOnly]



