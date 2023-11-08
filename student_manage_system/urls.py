"""student_manage_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mylogin import login
from mylogin import score
from mylogin import classes
from mylogin import checkscore
urlpatterns = [
    path('admin/', admin.site.urls),
    path('test1/', login.test1),
    path('login/', login.login),
    path('register/', login.register),
    path('logout/', login.logout),

    path('class_append/', classes.class_append),
    path('get_score/', score.get_score_by_account),

    path('score/create', score.create_score),
    path('score/delete', score.delete_score),
    path('score/list', score.list_score),
    path('score/modify', score.modify_score),



    path('check_score/list/teacher', checkscore.list_check_score_by_teacher),
    path('check_score/list/student', checkscore.list_check_score_by_student),
    path('check_score/operate', checkscore.operate_check_score),
    path('check_score/create', checkscore.create_check_score),
]
