from django.db import models

class Admin(models.Model):
    """管理员表"""
    AdID = models.IntegerField(verbose_name="编号")
    name = models.CharField(verbose_name="姓名", max_length=64)
    email = models.EmailField(verbose_name="邮箱", max_length=64)
    password = models.CharField(verbose_name="密码", max_length=128)

    class Meta:
        # db_table = "admin_list"
        verbose_name = "管理员信息"
        verbose_name_plural = verbose_name

class AsUser(models.Model):
    """用户表"""
    name = models.CharField(verbose_name="昵称", max_length=64)
    email = models.EmailField(verbose_name="邮箱", max_length=64)
    phone = models.CharField(verbose_name="手机号", max_length=64)
    password = models.CharField(verbose_name="密码", max_length=128)
    age = models.IntegerField(verbose_name="年龄", default=0, null=True, blank=True)
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices, null=True, blank=True)
    status_choices = (
        (0, "正常"),
        (1, "禁用"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=0)

    class Meta:
        # db_table = "user_list"
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

class KeyWord(models.Model):
    """关键字"""
    keyword = models.CharField(verbose_name="关键字", max_length=100)
    response = models.CharField(verbose_name="应答短语", max_length=100)

    def __str__(self):
        return self.keyword

class Statistics(models.Model):
    """统计信息"""
    name = models.CharField(verbose_name="姓名", max_length=64)
    content = models.CharField(verbose_name="内容", max_length=100)
    send_time = models.DateTimeField(verbose_name="发送时间")
    browser = models.CharField(verbose_name="浏览器", max_length=64)

