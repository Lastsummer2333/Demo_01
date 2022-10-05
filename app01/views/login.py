from django import forms
from django.forms import ValidationError
from django.shortcuts import render, redirect, HttpResponse
from app01.models import Admin, AsUser
from app01.utils.bootstrap import BootstrapModelForm
from app01.utils.encrypt import md5
import re
from io import BytesIO
from app01.utils.code import check_code


class LoginForm(forms.Form):
    email = forms.EmailField(label="邮箱", widget=forms.TextInput, required=True)
    password = forms.CharField(label="密码", widget=forms.PasswordInput(render_value=True), required=True)
    # code = forms.CharField(label="验证码", widget=forms.TextInput(attrs={"class": "form-control"}))

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


def Login(request):
    if request.method == "GET":
        form = LoginForm
        return render(request, "login.html", {"form": form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        admin_obj = Admin.objects.filter(**form.cleaned_data).first()
        user_obj = AsUser.objects.filter(**form.cleaned_data).first()

        # input_code = LoginForm.cleaned_data.pop('code')
        # code = request.session.get('images_code', "")
        # if code.upper() != input_code.upper():
        #     form.add_error("code", "验证码错误")
        #     return render(request, "login.html", {"form": form})

        if not admin_obj and not user_obj:
            form.add_error("password", "邮箱或密码输入错误")
            return render(request, "login.html", {"form": form})

        elif admin_obj:
            # 网站生成随机字符串；写到用户浏览器的cookie中；再写到session中
            request.session["info"] = {"id": admin_obj.id, "name": admin_obj.name}
            return redirect("/asuser/list/")

        elif user_obj:
            if user_obj.status == 0:
                request.session["info"] = {"id": user_obj.id, "name": user_obj.name}
                return redirect("/answer/")
            form.add_error("password", "很抱歉，您目前不能登录")
    return render(request, "login.html", {"form": form})

# 生成图片验证码
# def images_code(request):
#     # 调用pillow函数，生成图片
#     img, code_str = check_code()
#
#     # 写入到自己的session中，便于后续获取验证码进行校验
#     request.session['images_code'] = code_str
#     # session超过60s失效
#     request.session.set_expiry(60)
#
#     stream = BytesIO()
#     img.save(stream, 'png')
#     stream.getvalue()

    return HttpResponse(stream.getvalue())

def Logout(request):
    """注销"""
    request.session.clear()
    return redirect("/login/")


class RegistForm(BootstrapModelForm):
    confirm_password = forms.CharField(label="确认密码",
                                       widget=forms.PasswordInput,
                                       )

    class Meta:
        model = AsUser
        fields = ["name", "email", "phone", "password", "confirm_password", "age", "gender"]
        # fields = "__all__"
        widgets = {"password": forms.PasswordInput(render_value=True)}

    def clean_phone(self):
        in_phone = self.cleaned_data.get("phone")
        if not re.match(r'^1[3-8]\d{9}$', in_phone):
            raise ValidationError("手机号格式不正确")
        return in_phone

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

    # 密码校验和加密
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        if len(pwd) < 6 or len(pwd) > 20:
            raise ValidationError("密码长度需在6到20位")
        elif pwd.isdigit() or pwd.isalpha():
            raise ValidationError("密码需由数字和字母组成")
        return md5(pwd)

    # 确认密码
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("密码不一致")
        return confirm

def Regist(request):
    """用户注册"""
    if request.method == "GET":
        form = RegistForm
        return render(request, "regist.html", {"form": form})

    form = RegistForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/login/")

    return render(request, "regist.html", {"form": form})
