import json

from math import ceil
from django.conf import settings

from django.http import HttpResponse


# 装饰器，检查request参数是否齐全
def check_request(*params):
    def __check_request(func):
        def warpper(request):
            print(params)
            if request.method != 'POST':
                result = {'code': 402, 'information': '请求方式错误！'}
                return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
            for param in params:
                try:
                    json_req = json.loads(request.body)[param]
                    if type(json_req) is str:
                        if json_req.strip() == "":
                            data = {'code': 501, 'information': '空参数异常！', }
                            return HttpResponse(json.dumps(data), content_type="application/json")
                    if type(json_req) is int:
                        if json_req < 0:
                            data = {'code': 501, 'information': '参数不能为负数！', }
                            return HttpResponse(json.dumps(data), content_type="application/json")
                    if (param == 'comment_content')|(param == 'reply_content'):
                        if len(json_req)>100:
                            result = {'code': 501, 'information': '字数超过限制'}
                            return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
                except KeyError:
                    data = {'code': 501, 'information': '缺少参数异常！', }
                    return HttpResponse(json.dumps(data), content_type="application/json")
            # 参数都存在，则继续执行
            return func(request)
        return warpper
    return __check_request


# 校验page
def check_page(page, count):
    if type(page) is not int:
        result = {'code': 405, 'information': '参数类型异常！'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    if page <= 0:
        return 0
    # 每页至少十条记录
    if count > 10:
        if page > ceil(count / 10):
            return ceil(count/10)-1
    return page-1


# 返回order
def check_order(order_type):
    order = "-create_time"
    if order_type == 0:
        order = "-create_time"
    if order_type == 1:
        order = "-page_view"
    if order_type == 2:
        order = "-point_count"
    return order


# 返回服务器IP地址
def toIp():
    return settings.SERVER_ADDRESS


# 返回留言板默认头像
def toBoardUrl():
    return toIp() + '/static/default/messageBoard.jpg'

def toJson(querys, *params):
    i = 0
    json_list = []
    for query in querys:
        json_dict = {}
        for i in range(len(params)):
            if params[i] == "create_time":
                query[i] = query[i].strftime('%Y-%m-%d %H:%M:%S')
            json_dict[params[i]] = query[i]
        i = 0
        json_list.append(json_dict)
    return json_list
