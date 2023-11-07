from django.http import JsonResponse
from django.core import serializers

from .models import UserInfo, ScoreInfo, ExamInfo, ClassInfo
from .const import SUBJECT_MAJOR, SUBJECT_ALL, StatusCode


def create_score(request):
    """
    根据所给的全部信息，创建score表项。

    :param request.*: int or str
    :return: JsonResponse(
        'status_code': int
        'status_msg': str
    )
    """
    if request.method == 'POST':
        # 从request获取数据
        try:
            student_id = int(request.POST.get('student_id'))
            exam_id = int(request.POST.get('exam_id'))
            teacher_id = int(request.POST.get('teacher_id'))
            score = int(request.POST.get('score'))
            subject = str(request.POST.get('subject'))
        except ValueError:
            return JsonResponse({
                'status_code': StatusCode.INVALID_TYPE,
                'status_msg': 'Create score failed. Error: invalid type'
            })

        # check data validation
        if subject not in SUBJECT_ALL:
            return JsonResponse({
                'status_code': StatusCode.INVALID_ARGUMENT,
                'status_msg': 'Create score failed. Error: invalid subject.'
            })
        if score < 0 or (subject in SUBJECT_MAJOR and score > 150) or (subject not in SUBJECT_MAJOR and score > 100):
            return JsonResponse({
                'status_code': StatusCode.INVALID_ARGUMENT,
                'status_msg': 'Create score failed. Error: invalid score.'
            })

        # check exist necessary key
        try:
            student = UserInfo.objects.get(role='student', user_id=student_id)
            exam = ExamInfo.objects.get(exam_id=exam_id, subject=subject)
            teacher = UserInfo.objects.get(role='teacher', user_id=teacher_id)
        except UserInfo.DoesNotExist:
            return JsonResponse({
                'status_code': StatusCode.INVALID_ARGUMENT,
                'status_msg': 'Create score failed. Error: invalid student or teacher.'
            })
        except ExamInfo.DoesNotExist:
            return JsonResponse({
                'status_code': StatusCode.INVALID_ARGUMENT,
                'status_msg': 'Create score failed. Error: invalid exam.'
            })

        # check data duplication
        score_origin = ScoreInfo.objects.filter(student_id=student_id, teacher_id=teacher_id, exam_id=exam_id,
                                                score=score, subject=subject)
        if score_origin:
            return JsonResponse({
                'status_code': StatusCode.DUPLICATE_DATA,
                'status_msg': 'Create score failed. Error: duplicate score'
            })

        # create and save data
        score = ScoreInfo(student_id=student_id, teacher_id=teacher_id, exam_id=exam_id,
                          score=score, subject=subject)
        score.save()
        return JsonResponse({
            'status_code': StatusCode.SUCCESS,
            'status_msg': 'Create score success.'
        })
    else:
        # invalid method
        return JsonResponse({
            'status_code': StatusCode.INVALID_METHOD,
            'status_msg': 'Invalid request method.'
        })


def modify_score(request):
    """
    通过score_id找到需要修改的score，填入new_score

    :param request.score_id: str
    :param request.new_score: str
    :return: JsonResponse(
        'status_code': int
        'status_msg': str
    )
    """

    if request.method == "POST":
        try:
            score_id = int(request.POST.get('score_id'))
            new_score = int(request.POST.get('new_score'))
        except ValueError:
            return JsonResponse({
                'status_code': StatusCode.INVALID_TYPE,
                'status_msg': 'Modify score failed. Error: invalid type.'
            })
        try:
            score = ScoreInfo.objects.get(score_id=score_id)
            score.score = new_score
            score.save()
            return JsonResponse({
                'status_code': StatusCode.SUCCESS,
                'status_msg': 'Modify score success.'
            })
        except ScoreInfo.DoesNotExist:
            return JsonResponse({
                'status_code': StatusCode.NONE_DATA,
                'status_msg': 'Modify score failed. Error: score is null.'
            })
    else:
        # invalid method
        return JsonResponse({
            'status_code': StatusCode.INVALID_METHOD,
            'status_msg': 'Invalid request method.'
        })


def delete_score(request):
    """
    按照score_id（主键）删除数据

    :param request.score_id: str
    :return: JsonResponse(
        'status_code': int
        'status_msg': str
    )
    """
    if request.method == "POST":
        try:
            score_id = int(request.POST.get('score_id'))
        except ValueError:
            return JsonResponse({
                'status_code': StatusCode.INVALID_TYPE,
                'status_msg': 'Delete score failed. Error: invalid type.'
            })
        score = ScoreInfo.objects.filter(score_id=score_id)
        if score:
            score.delete()
            return JsonResponse({
                'status_code': StatusCode.SUCCESS,
                'status_msg': 'Delete score success'
            })
        else:
            return JsonResponse({
                'status_code': StatusCode.NONE_DATA,
                'status_msg': 'Delete score failed. Error: score is null.'
            })
    else:
        # invalid method
        return JsonResponse({
            'status_code': StatusCode.INVALID_METHOD,
            'status_msg': 'Invalid request method.'
        })


def list_score(request):
    """
    列出关于user_id（老师）的所有score。

    :param request.user_id: str
    :return: JsonResponse(
        'status_code': int
        'status_msg': str
        'score_info': array of dict.(optional)
    )
    """
    if request.method == "POST":
        try:
            user_id = int(request.POST.get('user_id'))
        except ValueError:
            return JsonResponse({
                'status_code': StatusCode.INVALID_TYPE,
                'status_msg': 'List score failed. Error: invalid type.'
            })
        try:
            teacher = UserInfo.objects.get(user_id=user_id, role='teacher')
        except UserInfo.DoesNotExist:
            return JsonResponse({
                'status_code': StatusCode.INVALID_ARGUMENT,
                'status_msg': 'List score failed. Error: invalid argument.'
            })

        # todo 返回数据需要修改
        # score = (ScoreInfo.objects.filter(teacher_id=user_id)
        #         .values('score_id','score','subject','student_id','exam_id'))
        score = ScoreInfo.objects.filter(teacher_id=user_id)
        return JsonResponse({
            'status_code': StatusCode.SUCCESS,
            'status_msg': 'List score success.',
            'score_info': serializers.serialize('python', score)
        })
    else:
        # invalid method
        return JsonResponse({
            'status_code': StatusCode.INVALID_METHOD,
            'status_msg': 'Invalid request method.'
        })


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
                    'status_code': StatusCode.SUCCESS,
                    'status_msg': 'Success',
                    'exam_info': exam_info_list,
                    'score_info': score_info_list,
                    'class_info': class_info_list,
                }

            else:
                response = {
                    'status_code': StatusCode.INVALID_ARGUMENT,
                    'status_msg': 'Failed',
                }

        except UserInfo.DoesNotExist:
            response = {
                'status_code': StatusCode.NONE_DATA,
                'status_msg': 'Failed',
            }

        return JsonResponse(response)

    else:
        return JsonResponse({'status_code': StatusCode.INVALID_METHOD, 'status_msg': 'Invalid request method'})