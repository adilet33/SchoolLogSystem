from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

Genders = (
    ('Male', 'Male'),
    ('Female', 'Female')
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_teacher=False, **extra_fields):
        if not email:
            raise ValueError('email does not exist')
        email = self.normalize_email(email)
        user = self.model(email=email, is_teacher=is_teacher, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_teacher', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=100, verbose_name='электронная почта', null=True, blank=True, unique=True)
    name = models.CharField(max_length=100, blank=True, verbose_name='ФИО')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email


class TeacherAccount(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_account')
    first_name = models.CharField(max_length=20, verbose_name='name', null=True)
    last_name = models.CharField(max_length=50, verbose_name='surname', null=True)
    teacher_id = models.CharField(max_length=10, unique=True)
    phone = models.CharField(max_length=20, verbose_name='номер', unique=True)
    gender = models.CharField(max_length=10, choices=Genders)
    #subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, related_name='Subject')
    #profile_img = models.ImageField(upload_to= , verbose_name='фото', null=True, blank=True)

    def __str__(self):
        return self.user.name


class Subject(models.Model):
    name = models.CharField(max_length=50)
    teacher = models.ForeignKey(TeacherAccount, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.subject.name


class StudentAccount(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_account')
    first_name = models.CharField(max_length=20, verbose_name='name', null=True)
    last_name = models.CharField(max_length=50, verbose_name='surname', null=True)
    student_id = models.CharField(max_length=10, unique=True)
    phone = models.CharField(max_length=20, verbose_name='номер', unique=True)
    gender = models.CharField(max_length=10, choices=Genders)
    #profile_img = models.ImageField(upload_to=, verbose_name='фото', null=True, blank=True)

    def __str__(self):
        return self.user.name


class Result(models.Model):
    student = models.ForeignKey(StudentAccount, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.student.user.name} {self.score}"
