from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import TeacherListView, SubjectListCreateView, ScheduleListCreateView, StudentListView, ResultListCreateView,\
 TeacherRetrieveUpdateView, StudentRetrieveUpdateView, UserRegistrationView,  UserLoginView, TeacherCreateView, StudentCreateView, UserUpdateView, PasswordResetView

urlpatterns = [
    path('register', UserRegistrationView.as_view(), name="register"),
    path('login', UserLoginView.as_view(), name="login"),
    path('users/<int:pk>', UserUpdateView.as_view(), name="user-update"),
    path('password_reset', PasswordResetView.as_view(), name="password-reset"),
    path('teachers', TeacherListView.as_view(), name="teacher_list"),
    path('teacher_create', TeacherCreateView.as_view(), name="teacher-create"),
    path('student_create', StudentCreateView.as_view(), name="student-create"),
    path('teacher_update/<int:pk>', TeacherRetrieveUpdateView.as_view(), name="teacher-update"),
    path('student_update/<int:pk>', StudentRetrieveUpdateView.as_view(), name="student-update"),
    path('students', StudentListView.as_view(), name="student_list"),
    path('subjects', SubjectListCreateView.as_view(), name="subjects_list"),
    path('schedule', ScheduleListCreateView.as_view(), name="schedule"),
    path('grades', ResultListCreateView.as_view(), name="grades"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

