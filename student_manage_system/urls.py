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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test1/', login.test1),
    path('login/', login.login),
    path('register/', login.register),
    path('score/create', score.create_score),
    path('score/delete', score.delete_score),
    path('score/list', score.list_score),
    path('score/modify', score.modify_score),
    path('logout/', mylogin.logout),
    path('class_apend/',mylogin.class_apend),
    path('get_score/',mylogin.get_score)
]
