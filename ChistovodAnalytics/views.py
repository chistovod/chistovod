# Create your views here.
from django.shortcuts import render_to_response
from controllers import parse_and_save_notifications
from django.core import serializers
from models import NotificationOK


def parse(request):
    parse_and_save_notifications()
    return render_to_response('parse.html')


def notificationOK(request):
    return render_to_response('notificationOK.html', {'data':NotificationOK.objects.all()})