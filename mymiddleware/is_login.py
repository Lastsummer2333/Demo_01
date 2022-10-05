import requests
from django.shortcuts import HttpResponse, redirect, render
from django.utils.deprecation import MiddlewareMixin


class is_Login(MiddlewareMixin):

    def process_request(self, request):

        # 1.排除需要验证登录状态的界面
        url_list = ['/login/', '/regist/']
        url = request.path_info
        if url in url_list:
            return

        # 2.检查用户登录状态
        info = request.session.get("info")
        if not info:
            return render(request, "error.html", {"msg": "请先登录！"})
        return

    def process_response(self, request, response):
        return response
