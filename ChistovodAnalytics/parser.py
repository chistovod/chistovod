import os
from zipfile import ZipFile
from lxml import etree
from zakupki_xml_parser import read_notification
import pprint

path = '/home/marat/zakupki.gov.ru/docs/Sankt-Peterburg/notifications'
files = [f for f in os.listdir(path) if f.endswith('.zip')]
first = os.path.join(path, files[0])
with ZipFile(first) as zip_file:
    members = zip_file.namelist()
    with zip_file.open(members[0]) as f:
        for event, xml in etree.iterparse(f, tag='{http://zakupki.gov.ru/oos/export/1}notificationOK'):
            if event == 'end':
                document = read_notification(xml)
                pprint.pprint(document)