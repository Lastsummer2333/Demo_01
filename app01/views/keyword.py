from django import forms
from django.forms import ValidationError
from django.shortcuts import render, redirect, HttpResponse
from app01.models import Admin, AsUser, KeyWord
from app01.utils.pagination import Pagination
from app01.utils.bootstrap import BootstrapModelForm
from app01.utils.encrypt import md5
from app01.utils.creat_user import creatUsers


def keywordList(request):
    """应答短语列表"""

    # 搜索功能
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["keyword__contains"] = search_data

    queryset = KeyWord.objects.filter(**data_dict)

    # 分页功能
    page_obj = Pagination(request, queryset)

    context = {
        "keyword": page_obj.page_queryset,
        "page_string": page_obj.html(),
        "search_data": search_data,
    }

    return render(request, "keyword_list.html", context)


class keywordAddForm(BootstrapModelForm):

    class Meta:
        model = KeyWord
        fields = ["keyword", "response"]
        fields = "__all__"

    # def clean_email(self):
    #     in_email = self.cleaned_data["email"]
    #
    #     exists = AsUser.objects.filter(email=in_email).exists()
    #     if exists:
    #         raise ValidationError("邮箱已存在")
    #     return in_email
    #
    # # 密码加密
    # def clean_password(self):
    #     pwd = self.cleaned_data.get("password")
    #     return md5(pwd)
    #
    # # 确认密码
    # def clean_confirm_password(self):
    #     pwd = self.cleaned_data.get("password")
    #     confirm = md5(self.cleaned_data.get("confirm_password"))
    #     if confirm != pwd:
    #         raise ValidationError("密码不一致")
    #     return confirm

def keywordAdd(request):
    """添加应答短语"""
    if request.method == "GET":
        form = keywordAddForm
        return render(request, "keyword_add.html", {"form": form})

    form = keywordAddForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/keyword/list/")

    return render(request, "keyword_add.html", {"form": form})


class keywordEditForm(BootstrapModelForm):

    class Meta:
        model = KeyWord
        fields = ["keyword", "response"]
        # fields = "__all__"

    # def clean_name(self):
    #     in_name = self.cleaned_data["name"]
    #
    #     exists = Admin.objects.exclude(id=self.instance.pk).filter(name=in_name).exists()
    #     if exists:
    #         raise ValidationError("昵称已存在")
    #     return in_name


def keywordEdit(request, nid):
    """修改应答短语"""
    keyword_object = KeyWord.objects.filter(id=nid).first()

    if not keyword_object:
        return render(request, "error.html", {"msg": "需要修改的用户不存在"})

    if request.method == "GET":
        form = keywordEditForm(instance=keyword_object)
        return render(request, "keyword_edit.html", {"form": form})

    else:
        form = keywordEditForm(instance=keyword_object, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("/keyword/list/")

    return render(request, "keyword_edit.html", {"form": form})


def keywordDel(request, nid):
    """删除应答短语"""
    KeyWord.objects.filter(id=nid).delete()
    return redirect("/keyword/list/")

