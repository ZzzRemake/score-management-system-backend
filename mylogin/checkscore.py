from django.http import JsonResponse

from .models import ExamInfo,ScoreInfo, StudentInfo, TeacherInfo, CheckScoreInfo
from .const import StatusCode

def create_check_score(request):
    """
    - user_id (integer, 必需)：学生用户id
    - score_id (integer, 必需)：score_id
    - reason (string, 必需)：申请原因

    根据所给的全部信息，创建申请查分表项。

    :param request.user_id: str
    :return: JsonResponse(
        'status_code': int
        'status_msg': str
    )
    """
    if request.method == 'POST':
        try:
            user_id = int(request.POST.get('user_id'))
            score_id = int(request.POST.get('score_id'))
            reason = str(request.POST.get('reason'))
        except ValueError:
            return JsonResponse({
                'status_code': StatusCode.INVALID_TYPE,
                'status_msg': 'Check score failed. Error: invalid type'
            })

        # check the reason is null
        if reason == '':
            return JsonResponse({
                'status_code': StatusCode.INVALID_ARGUMENT,
                'status_msg': 'Check score failed. Error: reason can not be empty.'
            })

        # check exist necessary key
        try:
            student = StudentInfo.objects.get(user_id=user_id)
            score = ScoreInfo.objects.get(score_id=score_id)
            print(student.student_name, score.student.student_name)
        except StudentInfo.DoesNotExist:
            return JsonResponse({
                'status_code': StatusCode.INVALID_ARGUMENT,
                'status_msg': 'Check score failed. Error: invalid student.'
            })
        except ScoreInfo.DoesNotExist:
            return JsonResponse({
                'status_code': StatusCode.INVALID_ARGUMENT,
                'status_msg': 'Check score failed. Error: invalid score.'
            })
        if score.student != student:
            return JsonResponse({
                'status_code': StatusCode.INVALID_ARGUMENT,
                'status_msg': 'Check score failed. Error: invalid score and student.'
            })
        # create and save data
        check, created = CheckScoreInfo.objects.get_or_create(student_id=user_id,score_id=score_id, reason=reason)

        if created:
            check.save()
        else:
            return JsonResponse({
                'status_code': StatusCode.DUPLICATE_DATA,
                'status_msg': 'Check score failed: duplicate data.'
            })

        return JsonResponse({
            'status_code': StatusCode.SUCCESS,
            'status_msg': 'Check score success.'
        })

    else:
        # invalid method
        return JsonResponse({
            'status_code': StatusCode.INVALID_METHOD,
            'status_msg': 'Invalid request method.'
        })



def list_check_score_by_teacher(request):
    """
    - user_id (integer, 必需)：教师用户id

    以老师身份返回所有和teacher相关的wait状态查分。
    :return JsonResponse(
        'status_code': (integer, 必需)：状态码，0表示成功，其他值表示失败
       'status_msg': (string, 必需)：返回状态描述
        'score_list': (array)
    )
    """
    if request.method == 'POST':
        try:
            user_id = int(request.POST.get('user_id'))
        except Exception:
            return JsonResponse({
                'status_code': StatusCode.INVALID_TYPE,
                'status_msg': 'Approve failed. Error: invalid type.'
            })

        try:
            teacher = TeacherInfo.objects.get(user_id=user_id)
        except TeacherInfo.DoesNotExist:
            return JsonResponse({
                'status_code': StatusCode.INVALID_ARGUMENT,
                'status_msg': 'Approve failed. Error: invalid teacher.'
            })

        checks = CheckScoreInfo.objects.filter(score__teacher=teacher, status="wait").distinct()
        response = {
            'status_code': StatusCode.SUCCESS,
            'status_msg': 'List check_score success',
            'score_list': []
        }
        for check in checks:
            response['score_list'].append({
                'check_id': check.check_id,
                'student': check.student.student_name,
                'exam':check.score.exam.exam_name,
                'score':check.score.score
            })
        return JsonResponse(response)
    else:
        # invalid method
        return JsonResponse({
            'status_code': StatusCode.INVALID_METHOD,
            'status_msg': 'Invalid request method.'
        })

def list_check_score_by_student(request):
    """
    - user_id (integer, 必需)：学生用户id

    以学生身份返回所有相关查分，无论状态。
    :return JsonResponse(
        'status_code': (integer, 必需)：状态码，0表示成功，其他值表示失败
        'status_msg': (string, 必需)：返回状态描述
        'score_list': (array)
    )
    """
    if request.method == 'POST':
        try:
            user_id = int(request.POST.get('user_id'))
        except Exception:
            return JsonResponse({
                'status_code': StatusCode.INVALID_TYPE,
                'status_msg': 'Approve failed. Error: invalid type.'
            })

        try:
            student = StudentInfo.objects.get(user_id=user_id)
        except StudentInfo.DoesNotExist:
            return JsonResponse({
                'status_code': StatusCode.INVALID_ARGUMENT,
                'status_msg': 'Approve failed. Error: invalid student.'
            })

        checks = CheckScoreInfo.objects.filter(student=student).distinct()
        response = {
            'status_code': StatusCode.SUCCESS,
            'status_msg': 'List check_score success',
            'score_list': []
        }
        for check in checks:
            response['score_list'].append({
                'check_id': check.check_id,
                'exam': check.score.exam.exam_name,
                'score':check.score.score,
                'status':check.status,
            })
        return JsonResponse(response)
    else:
        # invalid method
        return JsonResponse({
            'status_code': StatusCode.INVALID_METHOD,
            'status_msg': 'Invalid request method.'
        })

def operate_check_score(request):
    """
    老师端对所有处于wait状态的查分进行操作。
    仅可将wait的查分转为approve或reject，其他形式不允许。

    """
    if request.method == 'POST':
        try:
            user_id = int(request.POST.get('user_id'))
            check_id = int(request.POST.get('check_id'))
            action = str(request.POST.get('action'))
        except Exception:
            return JsonResponse({
                'status_code': StatusCode.INVALID_TYPE,
                'status_msg': 'Approve failed. Error: invalid type.'
            })

        # check exist necessary key
        try:
            teacher = TeacherInfo.objects.get(user_id=user_id)
            check = CheckScoreInfo.objects.get(check_id=check_id, score__teacher=teacher)
        except TeacherInfo.DoesNotExist:
            return JsonResponse({
                'status_code': StatusCode.INVALID_ARGUMENT,
                'status_msg': 'Approve failed. Error: invalid teacher.'
            })
        except CheckScoreInfo.DoesNotExist:
            return JsonResponse({
                'status_code': StatusCode.INVALID_ARGUMENT,
                'status_msg': 'Approve failed. Error: invalid check.'
            })

        # check the check is not successful
        if check.status != 'wait':
            return JsonResponse({
                'status_code': StatusCode.INVALID_ARGUMENT,
                'status_msg': 'Approve failed. Error: check is already successful.'
            })

        # check the action is invalid or null
        if action != 'approve' and action != 'reject':
            return JsonResponse({
                'status_code': StatusCode.INVALID_ARGUMENT,
                'status_msg': 'Approve failed. Error: invalid action.'
            })

        # approve or reject
        if action == 'approve':
            check.status = 'approve'
            check.save()

            return JsonResponse({
                'status_code': StatusCode.SUCCESS,
                'status_msg': 'Approve success.'
            })
        else:
            check.status = 'reject'
            check.save()
            return JsonResponse({
                'status_code': StatusCode.SUCCESS,
                'status_msg': 'Reject success.'
            })

    else:
        # invalid method
        return JsonResponse({
            'status_code': StatusCode.INVALID_METHOD,
            'status_msg': 'Invalid request method.'
        })