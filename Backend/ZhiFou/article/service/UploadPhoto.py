import json
import random

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.datetime_safe import datetime
import cv2

from Tool.decorator import toIp
from article import models


# 上传图片或者视频
#from users.utils.token_op import checkToken


@csrf_exempt
#@checkToken ("")
def uploadPhoto(request):
    if request.method == 'POST':
        # 提交过来的类型为formdata
        article_id = request.POST.get('article_id')
        file_obj = request.FILES.get('photo')
        size = file_obj.size
        if size > 30*1024*1024:  # 限制输入大小为30M
            return HttpResponse(json.dumps({'code': 405, 'information': '上传视频或图片大于30M！'}), content_type="application/json")
        if file_obj.name.split('.')[-1] not in ['jpeg', 'jpg', 'png', 'JPEG', 'JPG', 'PNG', 'mp4', 'MP4', 'gif',
                                                'GIF']:
            result = {"code": '500', 'information': '文件格式错误！'}
            return HttpResponse(json.dumps(result, ensure_ascii=False))
        # 处理图片,判断图片类型
        if file_obj.name.split('.')[-1] in ['jpeg', 'jpg', 'png', 'JPEG', 'JPG', 'PNG', 'gif', 'GIF']:
            photo_name = 'static/images/' + 'img_' + str(random.randint(1, 9999)) + datetime.now().strftime(
                "%Y%m%d%H%M%S") + str(random.randint(1, 99)) + '.' + file_obj.name.split('.')[-1]
            try:
                with open(photo_name, 'wb+') as f:
                    f.write(file_obj.read())
            except Exception as e:
                result = {"code": '500', 'information': '文件写入错误！'}
                return HttpResponse(json.dumps(result, ensure_ascii=False))
            photo_name = '/'+photo_name
            photo = models.Photo(photo_url=photo_name, create_time=datetime.now(), flag=0,
                                 article_id=int(article_id))
            photo.save()
            result = {"code": '200', "flag": 0, "photo_name": toIp()+photo_name}
            return HttpResponse(json.dumps(result, ensure_ascii=False))
        # 处理视频
        if file_obj.name.split('.')[-1] in ['mp4', 'MP4', ]:
            video_name = 'static/videos/' + 'video_' + str(random.randint(1, 9999)) + datetime.now().strftime(
                "%Y%m%d%H%M%S") + str(random.randint(1, 99)) + '.' + file_obj.name.split('.')[-1]
            try:
                with open(video_name, 'wb+') as f:
                    f.write(file_obj.read())
            except Exception:
                result = {"code": '500', 'information': '文件写入错误！'}
                return HttpResponse(json.dumps(result, ensure_ascii=False))
            # 使用opencv 截取视频文件第一帧 pip install opencv-python
            vc = cv2.VideoCapture(video_name)  # 读入视频文件
            if vc.isOpened():  # 判断是否正常打开
                rval, frame = vc.read()
                screenshot_name = 'static/images/' + 'shot_' + str(random.randint(1, 9999)) + \
                                  datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1, 99)) + '.jpg'
                cv2.imwrite(screenshot_name, frame)  # 存储为图像
                cv2.waitKey(1)
                vc.release()
                screenshot_name = '/'+screenshot_name
                shot = models.Photo(photo_url=screenshot_name, create_time=datetime.now(), flag=3,
                                    article_id=int(article_id))
                shot.save()
                video_name = '/'+video_name
                photo = models.Photo(photo_url=video_name, create_time=datetime.now(), flag=1,
                                     article_id=int(article_id))
                photo.save()
                result = {"code": '200', "flag": 1, "photo_name": toIp()+video_name, "shot_name": toIp()+screenshot_name}
                return HttpResponse(json.dumps(result, ensure_ascii=False))
            else:
                result = {"code": '500', 'information': '视频无法正常打开！'}
                return HttpResponse(json.dumps(result, ensure_ascii=False))
    result = {'code': 402}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
