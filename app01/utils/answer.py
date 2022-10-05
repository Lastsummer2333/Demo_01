# import configparser
# import json
#
# from django.conf import settings
# from django.core.serializers.json import DjangoJSONEncoder
# from django.db.models.fields.files import ImageFieldFile
# from django.http import JsonResponse
#
# from tencentcloud.common import credential
# from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
# from tencentcloud.common.profile.client_profile import ClientProfile
# from tencentcloud.common.profile.http_profile import HttpProfile
# from tencentcloud.nlp.v20190408 import nlp_client, models
#
# class ExtendedEncoder(DjangoJSONEncoder):
#     def default(self, o):
#         # ImageField图片文件是二进制内容，不能直接转为JSON文本，改为打印它的URL
#         if isinstance(o, ImageFieldFile):
#             try:
#                 return o.url
#             except ValueError:
#                 # 用户未上传头像时，获取path属性会抛异常
#                 return None
#         else:
#             return super().default(o)
#
#
# class LoginRequiredMiddleware:
#     """强制要求所有接口必须登录（除了login、csrftoken等个别接口）"""
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         # 除了login、csrftoken等个别接口，其他接口必须登录
#         if request.path not in ['/users/login', '/users/csrftoken']:
#             if not request.user.is_authenticated:
#                 return JsonResponse({'code': -1, 'message': '请先登录'}, status=401)
#         return self.get_response(request)
#
#
# def get_tencent_nlp_reply(keyword):
#     config = configparser.ConfigParser()
#     config.read(settings.BASE_DIR / 'config.ini')
#     try:
#         cred = credential.Credential(config['tencentcloud']['SecretId'], config['tencentcloud']['SecretKey'])
#         httpProfile = HttpProfile()
#         httpProfile.endpoint = 'nlp.tencentcloudapi.com'
#
#         clientProfile = ClientProfile()
#         clientProfile.httpProfile = httpProfile
#         client = nlp_client.NlpClient(cred, 'ap-guangzhou', clientProfile)
#
#         req = models.ChatBotRequest()
#         params = {
#             "Query": keyword,
#         }
#         req.from_json_string(json.dumps(params))
#
#         # 回应格式为：
#         # {"Reply": "你好，很高兴和你聊天", "Confidence": 1, "RequestId": "51681867-ba31-43b1-9a99-3a62d4405c01"}
#         resp = client.ChatBot(req)
#         response_json = json.loads(resp.to_json_string())
#         return response_json['Reply']
#     except TencentCloudSDKException as err:
#         print(err)