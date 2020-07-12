from django.http import JsonResponse, HttpResponse
from haystack.views import SearchView
from haystack.query import SearchQuerySet
from users.views import add_address_profile_url
import json


#haystack 分词检索
class UserSearchView(SearchView):
    #我们通过重写extra_context 来定义我们自己的变量，
    #通过看源码，extra_context 默认返回的是空，然后再get_context方法里面，把extra_context
    #返回的内容加到我们self.context字典里
  

    def create_response(self):
        keyword = self.request.GET.get('q', None)  # 关键词为q
        sqs = SearchQuerySet().using("user").filter(text=keyword)
        print(keyword)
        try:
            if not keyword:
                return HttpResponse(json.dumps({'code': 200, 'message': '没有相关信息'}), content_type="application/json")
            else:
                # print(sqs.all().count())
                content_list = []
                for i in sqs.all():
                    set_dict = {
                        'user_id': str(i.object.user_id),
                        'user_name': i.object.user_name,
                        'user_account': i.object.user_account,
                        'user_url': add_address_profile_url(i.object.user_url),
                        'email': i.object.email,
                        'user_gender': i.object.user_gender,
                        'user_phone':i.object.user_phone,
                        'user_credit': i.object.user_credit,
                     }  # 要返回的字段
                    content_list.append(set_dict)
                result = {'code': 200,  'user': content_list}
                return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
        except:
            return HttpResponse(json.dumps({'code': 405, 'information': '执行异常'}), content_type="application/json")