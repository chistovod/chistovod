import os
from zipfile import ZipFile
from lxml import etree
from os.path import expanduser
from zakupki_xml_parser import read_notification
from models import Lot


def parse_file(f):
    for event, xml in etree.iterparse(f):
        if str(xml.tag).endswith('}notificationOK'):
            for lot_dict in read_notification(xml):
                Lot(**lot_dict).save()


def process_file(f, filename):
    # ignoring non-notifications for now #####
    if filename.find('notification') < 0:
        return
        ##########################################

    if filename.endswith('.xml'):
        print "Parsing file", filename
        parse_file(f)


def process_any_file(file):
    if file.endswith('.zip'):
        with ZipFile(file) as zip_file:
            for file_under_zip in zip_file.namelist():
                with zip_file.open(file_under_zip) as f:
                    process_file(f, file + '!' + file_under_zip)
    else:
        with open(file, 'r') as f:
            process_file(f, file)


def process_all_files():
    path = expanduser('~') + '/zakupki.gov.ru'

    for root, subfolders, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            process_any_file(filepath)


if __name__ == "__main__":
    process_all_files()
