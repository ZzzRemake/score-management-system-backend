from django.http import JsonResponse

from .models import UserInfo, ScoreInfo, ExamInfo
from .const import SUBJECT_MAJOR, SUBJECT_ALL, StatusCode

def create_score(request):
    if request.method == 'POST':
        # 从request获取数据
        student_id = int(request.POST.get('student_id'))
        exam_id = int(request.POST.get('exam_id'))
        teacher_id = int(request.POST.get('teacher_id'))
        score = int(request.POST.get('score'))
        subject = request.POST.get('subject')

        # check data validation
        if subject not in SUBJECT_ALL:
            return JsonResponse({
                'status_code': StatusCode.INVALID_ARGUMENT,
                'status_msg': 'Create score failed. Error: invalid subject.'
            })
        if score < 0 or (subject in SUBJECT_MAJOR and score > 150) or (subject not in SUBJECT_MAJOR and score >100):
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
                'status_msg': 'Create score success.'
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
    pass

def delete_score(request):
    pass

def list_score(request):
    pass

def query_score(request):
    pass