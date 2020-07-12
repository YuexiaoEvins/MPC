from django.urls import path

from reply.service import Reply

urlpatterns = [
    path('addReplyToComment', Reply.addReplyToComment),
    path('addReplyToReply', Reply.addReplyToReply),
    path('deleteReply', Reply.deleteReply),
    path('queryReply', Reply.queryReply),
]