import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from Tool.decorator import check_request, toBoardUrl, toIp

from django.utils.datetime_safe import datetime
from Tool.page_tool import PageInfo

from article.models import Board, User


# 查询留言信息
from users.utils.token_op import checkToken


@csrf_exempt
@check_request('page', 'token')
@checkToken ("")
def queryMessageBoard(request):
    try:
        json_req = json.loads(request.body)
        page = json_req['page']
        # 分页查询文章信息
        page_info = PageInfo(page, 9)  # 每页十条记录
        board_count = Board.objects.filter(flag=1).count()
        boards = Board.objects.filter(flag=1).order_by("-create_time")[page_info.start():page_info.end()]
        json_list = []
        for board in boards:
            json_dict = {
                "board_url": toBoardUrl(),
                "board_id": board.board_id,
                "content": board.content,
                "create_time": board.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            json_list.append(json_dict)
        christmas = [
            toIp() + '/static/default/Christmas1.gif',
            toIp() + '/static/default/Christmas2.gif',
            toIp() + '/static/default/Christmas3.gif'
        ]
        result = {'code': 200, 'christmas': christmas, 'board_count': board_count, 'board': json_list}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
    except:
        return HttpResponse(json.dumps({'code': 405, 'information': '执行异常！'}), content_type="application/json")


# 新增留言板信息
@csrf_exempt
@check_request('user_id', 'content', 'token')
@checkToken ("")
def addMessageBoard(request):
    try:
        json_req = json.loads(request.body)
        user_id = json_req['user_id']
        content = json_req['content']
        if len(content) > 255:
            result = {'code': 406, 'information': '字数超出范围！'}
            return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
        user = User.objects.get(user_id=user_id)
        board = Board(user_id=user, flag=1, content=content, create_time=datetime.now())
        board.save()
        board_count = Board.objects.filter(flag=1).count()
        json_dict = {
            "board_url": toBoardUrl(),
            "board_id": board.board_id,
            "content": board.content,
            "create_time": board.create_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        result = {'code': 200, 'board_count': board_count, 'board': json_dict}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
    except:
        return HttpResponse(json.dumps({'code': 405, 'information': '执行异常！'}), content_type="application/json")


# 删除留言信息
@csrf_exempt
@check_request('board_id', 'token')
@checkToken ("")
def deleteMessageBoard(request):
    try:
        json_req = json.loads(request.body)
        board_id = json_req['board_id']
        board = Board.objects.filter(board_id=board_id).update(flag=0)
        if board > 0:
            result = {'code': 200}
            return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
    except:
        return HttpResponse(json.dumps({'code': 405, 'information': '执行异常！'}), content_type="application/json")


# 查询用户的已发留言信息
@csrf_exempt
@check_request('page', 'user_id', 'token')
@checkToken ("")
def queryMessageBoardByUserId(request):
    try:
        json_req = json.loads(request.body)
        user_id = json_req['user_id']
        page = json_req['page']
        # 分页查询文章信息
        page_info = PageInfo(page, 9)
        board_count = Board.objects.filter(user_id=user_id, flag=1).count()
        boards = Board.objects.filter(user_id=user_id, flag=1).order_by("-create_time")[page_info.start():page_info.end()]
        json_list = []
        for board in boards:
            json_dict = {
                "board_url": toBoardUrl(),
                "board_id": board.board_id,
                "content": board.content,
                "create_time": board.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            json_list.append(json_dict)
        result = {'code': 200, 'board_count': board_count, 'board': json_list}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
    except:
        return HttpResponse(json.dumps({'code': 405, 'information': '执行异常！'}), content_type="application/json")
