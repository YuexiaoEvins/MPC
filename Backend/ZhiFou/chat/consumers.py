from channels.generic.websocket import AsyncJsonWebsocketConsumer, AsyncWebsocketConsumer
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db import connection,models
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
import math

from .models import Message
import datetime


# 一个客户端就是一个consumer
class ChatConsumer(AsyncJsonWebsocketConsumer):

    # 连接处理函数，客户端建立WebSocket连接时，
    # 将Consumer实例加入组
    # room_group_name 组名
    # channel_name Consumer实例的channel名字
    async def connect(self):
        #将url上from_id、to_id组成房间名，并且按照id从小到大组合
        # self.group_name = self.scope['url_route']['kwargs']['group_name']
        from_id = self.scope['url_route']['kwargs']['from_id']
        to_id = self.scope['url_route']['kwargs']['to_id']
        
        if from_id < to_id:
            self.room_name = from_id+'-'+to_id
        else:
            self.room_name = to_id+'-'+from_id

        self.id = from_id
        self.room_group_name = 'chat_%s' % self.room_name


        #将该用户实例加入到channel
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # 启动WebSocket连接
        await self.accept()

        await self.chat_fristHistories(
        {
            "from_id":from_id,
            "to_id":to_id,
            "histforwho":self.id,
        })

        # 发送第一次聊天记录 
 

    async def receive_json(self, message, **kwargs):

        # # 收到信息时调用,持久化聊天记录
        send_type = message.get('send_type')
        # print(send_type)

        if(send_type == 0):
            await self.chat_histories(
                {
                    "messages":message,
                    "histforwho":self.id,
                },
            )

        else:
            if send_type == 1:
                message_temp = Message(from_id=message['from_id'],to_id=message['to_id'],chat_content=message['content'],chat_send_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                message_temp.save()

                # 信息发送到群组里面,以json格式发送数据
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        #这里"type"的值中.会换成_ 在本Consumer寻找chat_message()这个方法
                        "type": "chat.message",
                        "message_id":message_temp.sequence_id,
                    },
                )
            
            #为后续发送图片视频 扩展用

    async def chat_fristHistories(self, event):
        from_id = event['from_id']
        to_id = event['to_id']
        messages_result = Message.objects.filter(Q(from_id=from_id,to_id=to_id)|Q(from_id=to_id,to_id=from_id))
        messages_count = messages_result.count()
        if messages_count > 10:
            messages = messages_result[(messages_count-10):messages_count]
        else:
            messages = messages_result[:messages_count]

        if self.id == event['histforwho']:
            json_list = []
            if(len(messages)):   
                for message in messages:
                    if str(message.from_id) ==self.id:
                        json_dict = {
                            "sequence_id": message.sequence_id,
                            "from_id": str(message.from_id),
                            "to_id": str(message.to_id),
                            "send_type":0,
                            "is_first_hist":1,
                            "is_end":0,
                            "content": message.chat_content,
                            "create_time": message.chat_send_time.strftime('%Y-%m-%d %H:%M:%S'),
                            "role":1,   
                        }
                        # #发送方是对方
                    else:
                        json_dict = {
                            "sequence_id": message.sequence_id,
                            "from_id": str(message.from_id),
                            "to_id": str(message.to_id),
                            "send_type":0,
                            "is_first_hist":1,
                            "is_end":0,
                            "content": message.chat_content,
                            "create_time": message.chat_send_time.strftime('%Y-%m-%d %H:%M:%S'),
                            "role":0,   

                        }
                    json_list.append(json_dict)
            else:
                json_dict = {
                    "from_id": str(from_id),
                    "to_id": str(to_id),
                    "is_first_hist":1,
                    "send_type":0,
                    "is_end":1,
                }
                json_list.append(json_dict)
            await self.send(json.dumps(json_list,ensure_ascii=False,cls=DjangoJSONEncoder))


    async def chat_histories(self, event):

        if self.id == event['histforwho']:

            from_id = event['messages']['from_id']
            to_id = event['messages']['to_id']
            sequence_id = event['messages']['sequence_id']
            messages_result = Message.objects.filter(Q(from_id=from_id,to_id=to_id)|Q(from_id=to_id,to_id=from_id)).filter(sequence_id__lt=sequence_id).order_by('sequence_id')

            messages_count = messages_result.count()
            if messages_count > 10:
                messages = messages_result[(messages_count-10):messages_count]
            else:
                messages = messages_result[:messages_count]
            
            json_list = []
            if len(messages):
                for message in messages:
                    if str(from_id) ==self.id:
                        json_dict = {
                            "sequence_id": message.sequence_id,
                            "from_id": str(message.from_id),
                            "to_id": str(message.to_id),
                            "send_type":0,
                            "is_first_hist":0,
                            "is_end":0,
                            "content": message.chat_content,
                            "create_time": message.chat_send_time.strftime('%Y-%m-%d %H:%M:%S'),
                            "role":1,   
                        }
                        # #发送方是对方
                    else:
                        json_dict = {
                            "sequence_id": message.sequence_id,
                            "from_id": str(message.from_id),
                            "to_id": str(message.to_id),
                            "send_type":0,
                            "is_first_hist":0,
                            "is_end":0,
                            "content": message.chat_content,
                            "create_time": message.chat_send_time.strftime('%Y-%m-%d %H:%M:%S'),
                            "role":0,   
                        }
                    json_list.append(json_dict)
                self.is_frist_hist = 0
            else:
                #len(messages)==0
                json_dict = {
                        "from_id": str(from_id),
                        "to_id": str(to_id),
                        "is_first_hist":1,
                        "send_type":0,
                        "is_end":1,
                }
                json_list.append(json_dict)
            await self.send(json.dumps(json_list,ensure_ascii=False,cls=DjangoJSONEncoder))


    # 发送一条消息
    async def chat_message(self, event):

        #发送方是自己
        message_temp = Message.objects.get(sequence_id=event['message_id'])

        if str(message_temp.from_id) == self.id:
            message_json = {
                "sequence_id": message_temp.sequence_id,
                "from_id": str(message_temp.from_id),
                "to_id": str(message_temp.to_id),
                "role":1,
                # "is_first_hist":0,
                # "is_end":0,
                "send_type":1,
                "create_time": message_temp.chat_send_time.strftime('%Y-%m-%d %H:%M:%S'),
                "content": message_temp.chat_content,
            }
        else:
            message_json = {
                "sequence_id": message_temp.sequence_id,
                "from_id": str(message_temp.from_id),
                "to_id": str(message_temp.to_id),
                "role":0,
                # "is_first_hist":0,
                # "is_end":0,
                "send_type":1,
                "create_time": message_temp.chat_send_time.strftime('%Y-%m-%d %H:%M:%S'),
                "content": message_temp.chat_content,
            }

        json_list = []
        json_list.append(message_json)
        await self.send(json.dumps(json_list,ensure_ascii=False,cls=DjangoJSONEncoder))


    async def disconnect(self, close_code):
        # 连接关闭时调用
        # 将关闭的连接从群组中移除
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        # 将该客户端移除聊天组连接信息
        # ChatConsumer.session[self.room_group_name].remove(self)
        await self.close()
