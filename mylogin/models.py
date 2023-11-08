from django.db import models

# Create your models here.
from django.db import models

class UserInfo(models.Model):
    user_id = models.AutoField(primary_key=True)
    account = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_login = models.BooleanField(default=False)

class ClassInfo(models.Model):
    class_id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=50)

class StudentInfo(models.Model):
    user_id = models.OneToOneField(UserInfo, on_delete=models.CASCADE, primary_key=True)
    # 学号
    student_id = models.CharField(max_length=50, unique=True)
    student_name = models.CharField(max_length=50)
    class_id = models.ForeignKey(ClassInfo, on_delete=models.CASCADE)

class TeacherInfo(models.Model):
    user_id = models.OneToOneField(UserInfo, on_delete=models.CASCADE, primary_key=True)
    teacher_id = models.CharField(max_length=50, unique=True)
    teacher_name = models.CharField(max_length=50)


class ExamInfo(models.Model):
    exam_id = models.AutoField(primary_key=True)
    exam_time = models.DateTimeField()
    exam_name = models.CharField(max_length=50,default='')


class ScoreInfo(models.Model):
    score_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(StudentInfo, on_delete=models.CASCADE, related_name='student_scores')
    exam = models.ForeignKey(ExamInfo, on_delete=models.CASCADE, related_name='exam_scores')
    teacher = models.ForeignKey(TeacherInfo, on_delete=models.CASCADE, related_name='teacher_scores')
    score = models.DecimalField(max_digits=5, decimal_places=2)
    subject = models.CharField(max_length=50)

class CheckScoreInfo(models.Model):
    check_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(StudentInfo, on_delete=models.CASCADE, related_name='student_checks')
    score = models.ForeignKey(ScoreInfo, on_delete=models.CASCADE, related_name='score_checks')
    reason = models.CharField(max_length=100, default='')
    STATUS_CHOICES = [
        ('wait', 'Wait'),
        ('approve', 'Approve'),
        ('reject', 'Reject'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='wait')


