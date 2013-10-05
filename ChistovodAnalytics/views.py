# Create your views here.
from django.shortcuts import render_to_response
import os
from zipfile import ZipFile
from lxml import etree


def parse(request):
    path = '/home/marat/zakupki.gov.ru/docs/Sankt-Peterburg/notifications'
    files = [f for f in os.listdir(path) if f.endswith('.zip')]
    first = os.path.join(path, files[0])
    with ZipFile(first) as zip_file:
        members = zip_file.namelist()
        with zip_file.open(members[0]) as f:

            #txt = ''.join(f.readlines())

            root = etree.fromstring(f.read())
            t = ''
            for notification in root.iterchildren():
                type = notification.tag.split('}')[1]
                id_ = notification.find('{http://zakupki.gov.ru/oos/export/1}oos:id')
                t += '%s=%s:' % (type, id_)
            return render_to_response('parse.html', {'key': t })