from django.http import JsonResponse

from .models import ClassInfo
from .const import StatusCode

# class append并不在用户界面中使用，而应当是事先指定的
# 该文件可以作为部署前root用户导入成绩的操作
# 也因此，可以在这里增加批量导入等功能。

def class_append(request):
    # class append应该是一个单纯的操作，而不用标识创建者或是所属名
    if request.method == 'POST':
        class_name = request.POST.get('class_name')

        class_info= ClassInfo.objects.filter(**{"class_name": class_name})
        if not class_info:
            class_info = ClassInfo.objects.create(class_name=class_name)
            class_info.save()
            response = {
                'status_code': StatusCode.SUCCESS,
                'status_msg': 'Success',
            }
        else:
            response = {
                'status_code': StatusCode.DUPLICATE_DATA,
                'status_msg': 'Failed: duplicate class!',
            }

        return JsonResponse(response)

    else:
        return JsonResponse({
            'status_code': StatusCode.INVALID_METHOD,
            'status_msg': 'Invalid request method'})

