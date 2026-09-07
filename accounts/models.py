from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    class Role(models.TextChoices):
        STUDENT = 'STUDENT', 'Alumno'
        TEACHER = 'TEACHER', 'Profesor'
    user = models.OneToOneField(
       User, on_delete=models.CASCADE, related_name='profile'
    )
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.STUDENT,
    )
    birth_date = models.DateField(blank=True, null=True)
    xp=models.IntegerField(default=0)
    level=models.IntegerField(default=1)
    ducky_coins=models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

class Classroom(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='classrooms'
    )
    students = models.ManyToManyField(
        User, related_name='enrolled_classrooms', blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Announcement(models.Model):
    classroom = models.ForeignKey(
        Classroom, on_delete=models.CASCADE, related_name='announcements'
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title