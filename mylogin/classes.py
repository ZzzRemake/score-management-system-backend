from django.http import JsonResponse
from django.core import serializers

from .models import UserInfo, ScoreInfo, ExamInfo, ClassInfo
from .const import SUBJECT_MAJOR, SUBJECT_ALL, StatusCode

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
                'status_code': StatusCode.SUCCESS,
                'status_msg': 'Success',
            }

        except UserInfo.DoesNotExist:
            response = {
                'status_code': StatusCode.NONE_DATA,
                'status_msg': 'Failed: Student does not exist',
            }

        return JsonResponse(response)

    else:
        return JsonResponse({'status_code': StatusCode.INVALID_METHOD, 'status_msg': 'Invalid request method'})

