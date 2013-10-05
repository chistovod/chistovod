# Create your views here.
from django.shortcuts import render_to_response
from controllers import parse_and_save_notifications


def parse(request):
    parse_and_save_notifications()
    return render_to_response('parse.html')