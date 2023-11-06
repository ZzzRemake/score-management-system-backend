from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse

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
                    'status_code': 2,
                    'status_msg': 'User already logged in'
                })
            else:
                user.is_login = True
                user.save()
                return JsonResponse({
                    'status_code': 0,
                    'status_msg': 'Login successful'
                })
        except UserInfo.DoesNotExist:
            return JsonResponse({
                'status_code': 1,
                'status_msg': 'Account or password is incorrect'
            })
    else:
        return JsonResponse({
            'status_code': -1,
            'status_msg': 'Invalid request method'
        })


def register(request):
    if request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')
        name = request.POST.get('name')
        role = request.POST.get('role')

        try:
            user = UserInfo.objects.create(account=account, password=password, name=name, role=role,is_login=False)
            return JsonResponse({
                'status_code': 0,
                'status_msg': 'Registration successful'

            })
        except Exception as e:
            return JsonResponse({
                'status_code': 1,
                'status_msg': 'Registration failed. Error: {}'.format(str(e))
            })
    else:
        return JsonResponse({
            'status_code': 1,
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
                    'status_code': 0,
                    'status_msg': 'Logout successful'
                })
            else:
                return JsonResponse({
                    'status_code': 2,
                    'status_msg': 'User not logged in'
                })
        except UserInfo.DoesNotExist:
            return JsonResponse({
                'status_code': 1,
                'status_msg': 'User does not exist'
            })
    else:
        return JsonResponse({
            'status_code': -1,
            'status_msg': 'Invalid request method'
        })

def class_apend(request):
    if request.method == 'POST':
        account = request.POST.get('account')
        class_number = request.POST.get('class_number')

        try:
            student = UserInfo.objects.get(account=account)
            class_info, created = ClassInfo.objects.get_or_create(student=student, defaults={'class_number': class_number})

            if not created:
                class_info.class_number = class_number
                class_info.save()

            response = {
                'status_code': 0,
                'status_msg': 'Success',
            }

        except UserInfo.DoesNotExist:
            response = {
                'status_code': -1,
                'status_msg': 'Failed: Student does not exist',
            }

        return JsonResponse(response)

    else:
        return JsonResponse({'status_code': -1, 'status_msg': 'Invalid request method'})

def get_score(request):
    if request.method == 'GET':
        account = request.GET.get('account')
        try:
            student = UserInfo.objects.get(account=account)
            scores = ScoreInfo.objects.filter(student=student)
            class_info = ClassInfo.objects.filter(student=student)

            if student:
                exam_info_list = []
                score_info_list = []
                class_info_list = []

                for score in scores:
                    exam_info_list.append({
                        'exam_time': score.exam.exam_time,
                        'subject': score.exam.subject,
                        'exam_name':score.exam.exam_name
                    })

                    score_info_list.append({
                        'score_id': score.score_id,
                        'score': score.score,

                    })

                for class_instance in class_info:
                    class_info_list.append({
                        'class_number': class_instance.class_number,
                    })

                response = {
                    'status_code': 0,
                    'status_msg': 'Success',
                    'exam_info': exam_info_list,
                    'score_info': score_info_list,
                    'class_info': class_info_list,
                }

            else:
                response = {
                    'status_code': -1,
                    'status_msg': 'Failed',
                }

        except UserInfo.DoesNotExist:
            response = {
                'status_code': -1,
                'status_msg': 'Failed',
            }

        return JsonResponse(response)

    else:
        return JsonResponse({'status_code': -1, 'status_msg': 'Invalid request method'})