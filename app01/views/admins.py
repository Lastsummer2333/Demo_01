from django import forms
from django.forms import ValidationError
from django.shortcuts import render, redirect, HttpResponse
from app01.models import Admin, AsUser
from app01.utils.pagination import Pagination
from app01.utils.bootstrap import BootstrapModelForm
from app01.utils.encrypt import md5
from app01.utils.creat_user import creatUsers


def adminList(request):
    """管理员列表"""

    # 搜索功能
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["email__contains"] = search_data

    queryset = Admin.objects.filter(**data_dict)

    # 分页功能
    page_obj = Pagination(request, queryset)

    context = {
        "admin": page_obj.page_queryset,
        "page_string": page_obj.html(),
        "search_data": search_data,
    }

    return render(request, "admin_list.html", context)


class adminAddForm(BootstrapModelForm):
    # password = forms.CharField(min_length=3, label="密码")
    confirm_password = forms.CharField(label="确认密码",
                                       widget=forms.PasswordInput,
                                       )

    class Meta:
        model = Admin
        fields = ["AdID", "name", "email", "password", "confirm_password"]
        # fields = "__all__"
        widgets = {"password": forms.PasswordInput(render_value=True)}

    # 数据校验
    # def clean_name(self):
    #     in_name = self.cleaned_data["name"]
    #
    #     exists = AsUser.objects.filter(name=in_name).exists()
    #     if exists:
    #         raise ValidationError("昵称已存在")
    #     return in_name

    def clean_email(self):
        in_email = self.cleaned_data["email"]

        exists = AsUser.objects.filter(email=in_email).exists()
        if exists:
            raise ValidationError("邮箱已存在")
        return in_email

    # 密码加密
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    # 确认密码
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("密码不一致")
        return confirm


def adminAdd(request):
    """添加用户"""
    if request.method == "GET":
        form = adminAddForm
        return render(request, "admin_add.html", {"form": form})

    form = adminAddForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admins/list/")

    return render(request, "admin_add.html", {"form": form})


class adminEditForm(BootstrapModelForm):
    # AdId = forms.IntegerField(disabled=True, label="编号")
    password = forms.CharField(min_length=3, label="密码")

    class Meta:
        model = Admin
        fields = ["name", "email", "password"]
        # fields = "__all__"

    def clean_name(self):
        in_name = self.cleaned_data["name"]

        exists = Admin.objects.exclude(id=self.instance.pk).filter(name=in_name).exists()
        if exists:
            raise ValidationError("昵称已存在")
        return in_name


def adminEdit(request, nid):
    """修改信息"""
    admin_object = Admin.objects.filter(id=nid).first()

    if not admin_object:
        return render(request, "error.html", {"msg": "需要修改的用户不存在"})

    if request.method == "GET":
        form = adminEditForm(instance=admin_object)
        return render(request, "asuser_edit.html", {"form": form})

    else:
        form = adminEditForm(instance=admin_object, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("/admins/list/")

    return render(request, "admin_edit.html", {"form": form})


def adminDel(request, nid):
    """删除用户"""
    Admin.objects.filter(id=nid).delete()
    return redirect("/admins/list/")

