from django.contrib import admin

# Register your models here.
from .models import (
    ExamInfo,
    UserInfo,
    ClassInfo,
    ScoreInfo,
    CheckScoreInfo,
    StudentInfo,
    TeacherInfo
)
admin.site.register(ExamInfo)
admin.site.register(UserInfo)
admin.site.register(ClassInfo)
admin.site.register(ScoreInfo)
admin.site.register(CheckScoreInfo)
admin.site.register(StudentInfo)
admin.site.register(TeacherInfo)
