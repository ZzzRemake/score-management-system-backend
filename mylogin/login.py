from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse

from .const import StatusCode
# from .models import UserInfo
from .models import UserInfo


def test1(request):
    # 处理你的接口逻辑
    data = {'message': 'Hello, this is your API response!'}
    return JsonResponse(data)


# from .models import UserInfo
from .models import UserInfo, ExamInfo, ScoreInfo, ClassInfo


def login(request):
    if request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')
        try:
            user = UserInfo.objects.get(account=account, password=password)
            if user.is_login:
                return JsonResponse({
                    'status_code': StatusCode.DUPLICATE_DATA,
                    'status_msg': 'User already logged in'
                })
            else:
                user.is_login = True
                user.save()
                return JsonResponse({
                    'status_code': StatusCode.SUCCESS,
                    'status_msg': 'Login successful'
                })
        except UserInfo.DoesNotExist:
            return JsonResponse({
                'status_code': StatusCode.INVALID_ARGUMENT,
                'status_msg': 'Account or password is incorrect'
            })
    else:
        return JsonResponse({
            'status_code': StatusCode.INVALID_METHOD,
            'status_msg': 'Invalid request method'
        })


def register(request):
    if request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')
        name = request.POST.get('name')
        role = request.POST.get('role')

        # check repeat register
        user_temp = UserInfo.objects.filter(account=account)
        if user_temp:
            return JsonResponse({
                'status_code': StatusCode.DUPLICATE_DATA,
                'status_msg': 'Registration failed. Error: duplicate register.'
            })

        # todo 有时间搞个邮箱验证码？
        try:
            user = UserInfo.objects.create(account=account, password=password, name=name, role=role,is_login=False)
            return JsonResponse({
                'status_code': StatusCode.SUCCESS,
                'status_msg': 'Registration successful',

            })
        except Exception as e:
            return JsonResponse({
                'status_code': StatusCode.INVALID_ARGUMENT,
                'status_msg': 'Registration failed. Error: {}'.format(str(e))
            })
    else:
        return JsonResponse({
            'status_code': StatusCode.INVALID_METHOD,
            'status_msg': 'Invalid request method'
        })

def logout(request):
    if request.method == 'POST':
        account = request.POST.get('account')
        try:
            user = UserInfo.objects.get(account=account)
            if user.is_login:
                user.is_login = False
                user.save()
                return JsonResponse({
                    'status_code': StatusCode.SUCCESS,
                    'status_msg': 'Logout successful'
                })
            else:
                return JsonResponse({
                    'status_code': StatusCode.NONE_DATA,
                    'status_msg': 'User not logged in'
                })
        except UserInfo.DoesNotExist:
            return JsonResponse({
                'status_code': StatusCode.NONE_DATA,
                'status_msg': 'User does not exist'
            })
    else:
        return JsonResponse({
            'status_code': StatusCode.INVALID_METHOD,
            'status_msg': 'Invalid request method'
        })

