from django.http import JsonResponse
from django.views import View
from app01.models import KeyWord
from django import forms
from app01.utils import answer
from django.shortcuts import HttpResponse, render
from datetime import datetime
from app01.models import Statistics, KeyWord
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json


class AnswerForm(forms.Form):
    keyword = forms.CharField(label="想说点什么",
                              widget=forms.TextInput(attrs={"class": "form-control"}),
                              required=True)

    def clean_keyword(self):
        keyword = self.cleaned_data.get("keyword")
        return keyword


def AnswerView(request):
    if request.method == "GET":
        form = AnswerForm
        return render(request, "answer_view.html", {"form": form})

    form = AnswerForm(data=request.POST)
    if form.is_valid():
        keyword_obj = KeyWord.objects.filter(**form.cleaned_data).first()
        info = request.session.get("info")
        name = info["name"]
        content = form.cleaned_data.get("keyword")
        send_time = datetime.now()
        browser = request.user_agent.browser.family
        Statistics.objects.create(name=name, content=content, send_time=send_time, browser=browser)

        if not keyword_obj:
            content = form.cleaned_data.get("keyword")
            KeyWord.objects.create(keyword=content, response='')
            form.add_error("keyword", "我想听听其他的话")
            return render(request, "answer_view.html", {"form": form})
        # try:
        #     keyword = KeyWord.objects.get(keyword=keyword_obj.keyword)
        #     return JsonResponse({'code': 0, 'response': keyword.response})
        # except KeyWord.DoesNotExist:
        #     # 如果数据库里没有就调用腾讯云对话机器人接口，进行智能应答
        #     # response = answer.get_tencent_nlp_reply(keyword)
        #     # return JsonResponse({'code': 0, 'response': response}, json_dumps_params={"ensure_ascii": False})
        #     return HttpResponse("Sorry")
        return render(request, "answer.html", {"keyword_obj": keyword_obj})

def chat(request):
    return render(request, "chat.html")