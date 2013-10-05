# Create your views here.
from django.shortcuts import render_to_response
import os
from zipfile import ZipFile


def parse(request):
    path = '/home/marat/zakupki.gov.ru/docs/Sankt-Peterburg/notifications'
    files = [f for f in os.listdir(path) if f.endswith('.zip')]
    first = os.path.join(path, files[0])
    with ZipFile(first) as zip_file:
        members = zip_file.namelist()
        with zip_file.open(members[0]) as f:
            txt = f.readlines()
            return render_to_response('parse.html', {'key': txt})