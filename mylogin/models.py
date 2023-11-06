from django.db import models

# Create your models here.
from django.db import models

class UserInfo(models.Model):
    user_id = models.AutoField(primary_key=True)
    account = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_login = models.BooleanField(default=False)

class ExamInfo(models.Model):
    exam_id = models.AutoField(primary_key=True)
    exam_time = models.DateTimeField()
    exam_name = models.CharField(max_length=50,default='')
    subject = models.CharField(max_length=50)


class ScoreInfo(models.Model):
    score_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='student_scores')
    exam = models.ForeignKey(ExamInfo, on_delete=models.CASCADE, related_name='exam_scores')
    teacher = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='teacher_scores')
    score = models.DecimalField(max_digits=5, decimal_places=2)

class ClassInfo(models.Model):
    student = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='student_classes')
    class_number = models.CharField(max_length=50)

class CheckScoreInfo(models.Model):
    check_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='student_checks')
    exam = models.ForeignKey(ExamInfo, on_delete=models.CASCADE, related_name='exam_checks')
    score = models.ForeignKey(ScoreInfo, on_delete=models.CASCADE, related_name='score_checks')
    is_successful = models.BooleanField()


