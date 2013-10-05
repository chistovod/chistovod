from models import NotificationOK
from zipfile import ZipFile
import os
from zakupki_xml_parser import read_notification
from lxml import etree


def parse_and_save_notifications():
    path = '/home/marat/zakupki.gov.ru/docs/Sankt-Peterburg/notifications'
    files = [f for f in os.listdir(path) if f.endswith('.zip')]
    first = os.path.join(path, files[0])

    with ZipFile(first) as zip_file:
        for file_under_zip in zip_file.namelist():
            with zip_file.open(file_under_zip) as f:
                for event, xml in etree.iterparse(f, tag='{http://zakupki.gov.ru/oos/export/1}notificationOK'):
                    if event == 'end':
                        notification = read_notification(xml)
                        NotificationOK(**notification).save()
