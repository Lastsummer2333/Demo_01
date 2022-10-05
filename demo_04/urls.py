from django.contrib import admin
from django.urls import path
from app01.views import admins, asuser, login, answer, reply, statistic, keyword
from app01.utils import export

urlpatterns = [
    # path('admin/', admin.site.urls),

    path('sentry-debug/', login.Login),

    path('asuser/list/', asuser.asuserList),

    path('asuser/add/', asuser.asuserAdd),

    path('asuser/<int:nid>/edit/', asuser.asuserEdit),

    path('asuser/<int:nid>/del/', asuser.asuserDel),

    path('asuser/<int:nid>/reset/', asuser.asuserReset),

    path('asuser/<int:nid>/ban/', asuser.asuserForbidden),


    path('admins/list/', admins.adminList),

    path('admins/add/', admins.adminAdd),

    path('admins/<int:nid>/edit/', admins.adminEdit),

    path('admins/<int:nid>/del/', admins.adminDel),


    path('login/', login.Login),

    path('regist/', login.Regist),

    path('logout/', login.Logout),


    path('answer/', answer.AnswerView),

    path('answer/list/', statistic.answerList),

    path('answer/<int:nid>/del/', statistic.answerDel),


    path('keyword/list/', keyword.keywordList),

    path('keyword/add/', keyword.keywordAdd),

    path('keyword/<int:nid>/edit/', keyword.keywordEdit),

    path('keyword/<int:nid>/del/', keyword.keywordDel),


    path('export/users/', export.exportUsers),

    path('export/info/', export.exportInfo),

    path('chat/', answer.chat),

    # path('images/code/', login.images_code),

    # path('reply/list/', reply.reply_list),
    #
    # path('reply/add/', reply.reply_add),
    #
    # path('reply/delete/', reply.reply_delete),
    #
    # path('reply/<int:nid>/edit/', reply.reply_edit),

]
