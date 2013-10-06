# Create your views here.
from django.db import transaction
from django.shortcuts import render_to_response
from controllers import process_all_files
from models import Lot


def parse(request):
    process_all_files()
    return render_to_response('parse.html')


def notificationOK(request):
    return render_to_response('notificationOK.html', {'data': Lot.objects.all()})


def plot(request):
    return render_to_response('plot.html', {'data': Lot.objects.all()})