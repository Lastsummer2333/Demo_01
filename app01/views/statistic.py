from django import forms
from django.forms import ValidationError
from django.shortcuts import render, redirect, HttpResponse
from app01.models import Statistics
from app01.utils.pagination import Pagination
from app01.utils.bootstrap import BootstrapModelForm
from app01.utils.encrypt import md5

def answerList(request):
    """应答短语列表"""

    # 搜索功能
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["content__contains"] = search_data

    queryset = Statistics.objects.filter(**data_dict)

    # 分页功能
    page_obj = Pagination(request, queryset)

    context = {
        "content": page_obj.page_queryset,
        "page_string": page_obj.html(),
        "search_data": search_data,
    }

    return render(request, "answer_list.html", context)

def answerDel(request, nid):
    """删除短语"""
    Statistics.objects.filter(id=nid).delete()
    return redirect("/answer/list/")