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

def login(request):
    if request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')
        try:
            user = UserInfo.objects.get(account=account, password=password)
            return JsonResponse({
                'status_code': StatusCode.SUCCESS,
                'status_msg': 'Login successful',
                'user_id': user.user_id,
                'role': user.role
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

        try:
            user = UserInfo.objects.create(account=account, password=password, name=name, role=role)
            return JsonResponse({
                'status_code': StatusCode.SUCCESS,
                'status_msg': 'Registration successful',
                'user_id': user.user_id,

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