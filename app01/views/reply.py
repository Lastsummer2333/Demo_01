from django.shortcuts import render, redirect
from app01 import models

def reply_list(request):
    """应答列表"""
    # 去数据库获取所有的关键词和应答短语
    queryset = models.KeyWord.objects.all()
    # 关键词和应答短语列表
    return render(request, 'reply_list.html', {'queryset': queryset})


def reply_add(request):
    """添加应答短语"""
    if request.method == "get":
        return render(request, 'reply_add.html')

    # 用户通过post提交过来的数据
    keyword = request.POST.get("keyword")
    response = request.POST.get("response")

    # 保存到数据库
    models.KeyWord.objects.create(keyword=keyword, response=response)

    # 重定向回应答短语列表
    return redirect('/reply/list/')


def reply_delete(request):
    """删除应答短语"""
    # 获取id
    # http://127.0.0.1:8000/reply/delete/?nid=1
    nid = request.GET.get('nid')

    # 删除
    models.KeyWord.objects.filter(id=nid).delete()

    # 跳转回应答短语列表
    return redirect('/reply/list/')


def reply_edit(request, nid):
    """修改应答短语"""
    if request.method == "GET":
        # 根据nid获取数据
        row_object = models.KeyWord.objects.filter(id=nid).first()
        return render(request, 'reply_edit.html', {"row_object": row_object})

    # 获取用户提交的数据
    keyword = request.POST.get("keyword")
    response = request.POST.get("response")

    # 根据id在数据库中更新
    models.KeyWord.objects.filter(id=nid).update(keyword=keyword, response=response)

    # 重定向回应答短语列表
    return redirect('/reply/list/')
