from django import forms
from django.forms import ValidationError
from django.shortcuts import render, redirect, HttpResponse
from app01.models import Admin, AsUser
from app01.utils.pagination import Pagination
from app01.utils.bootstrap import BootstrapModelForm
from app01.utils.encrypt import md5
from app01.utils.creat_user import creatUsers


def asuserList(request):
    """用户列表"""

    # 添加测试用户
    # users = creatUsers(30000)
    # users.creat_user()

    # 搜索功能
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["email__contains"] = search_data

    queryset = AsUser.objects.filter(**data_dict)

    # 分页功能
    page_obj = Pagination(request, queryset)

    context = {
        "asuser": page_obj.page_queryset,
        "page_string": page_obj.html(),
        "search_data": search_data,
    }

    return render(request, "asuser_list.html", context)


class asuserAddForm(BootstrapModelForm):
    # password = forms.CharField(min_length=3, label="密码")
    confirm_password = forms.CharField(label="确认密码", widget=forms.PasswordInput)

    class Meta:
        model = AsUser
        fields = ["name", "email", "phone", "password", "confirm_password", "age", "gender"]
        # fields = "__all__"
        widgets = {"password": forms.PasswordInput(render_value=True)}

    # 数据校验
    def clean_name(self):
        in_name = self.cleaned_data["name"]

        exists = AsUser.objects.filter(name=in_name).exists()
        if exists:
            raise ValidationError("昵称已存在")
        return in_name

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


def asuserAdd(request):
    """添加用户"""
    if request.method == "GET":
        form = asuserAddForm
        return render(request, "asuser_add.html", {"form": form})

    form = asuserAddForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/asuser/list/")

    return render(request, "asuser_add.html", {"form": form})


class asuserEditForm(BootstrapModelForm):
    email = forms.EmailField(disabled=True, label="邮箱")
    phone = forms.CharField(disabled=True, label="手机号")
    password = forms.CharField(min_length=3, label="密码")

    class Meta:
        model = AsUser
        fields = ["name", "email", "phone", "password", "age", "gender", "status"]
        # fields = "__all__"

    def clean_name(self):
        in_name = self.cleaned_data["name"]

        exists = AsUser.objects.exclude(id=self.instance.pk).filter(name=in_name).exists()
        if exists:
            raise ValidationError("昵称已存在")
        return in_name


def asuserEdit(request, nid):
    """修改信息"""
    asuser_object = AsUser.objects.filter(id=nid).first()

    if not asuser_object:
        return render(request, "error.html", {"msg": "需要修改的用户不存在"})

    if request.method == "GET":
        form = asuserEditForm(instance=asuser_object)
        return render(request, "asuser_edit.html", {"form": form})

    else:
        form = asuserEditForm(instance=asuser_object, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("/asuser/list/")

    return render(request, "asuser_edit.html", {"form": form})


def asuserDel(request, nid):
    """删除用户"""
    AsUser.objects.filter(id=nid).delete()
    return redirect("/asuser/list/")


def asuserReset(request, nid):
    """重置密码"""
    AsUser.objects.filter(id=nid).update(password=md5('123456'))
    return redirect("/asuser/list/")

def asuserForbidden(request, nid):
    """禁止登录"""
    AsUser.objects.filter(id=nid).update(status=1)
    return redirect("/asuser/list/")