from django.shortcuts import HttpResponse
import csv, codecs
from app01.models import AsUser, Statistics
from django.utils.encoding import escape_uri_path


def exportUsers(request):
    response = HttpResponse(content_type='text/csv')
    response.write(codecs.BOM_UTF8)
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % 'users'
    writer = csv.writer(response)
    writer.writerow(['name', 'email', 'phone', 'password', 'age', 'gender'])
    users = AsUser.objects.all().values_list('name', 'email', 'phone', 'password', 'age', 'gender')
    for user in users:
        writer.writerow(user)
    return response


def exportInfo(request):
    response = HttpResponse(content_type='text/csv')
    response.write(codecs.BOM_UTF8)
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % escape_uri_path('statistics')
    writer = csv.writer(response)
    writer.writerow(['name', 'content', 'send_time', 'browser'])
    info = Statistics.objects.all().values_list('name', 'content', 'send_time', 'browser')
    for con in info:
        writer.writerow(con)
    return response
