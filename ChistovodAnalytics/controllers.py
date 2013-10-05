import os
import re
from zipfile import ZipFile
from lxml import etree
from os.path import expanduser
from zakupki_xml_parser import *
#from models import *

VALID_NOTIFICATIONS = re.compile('\}notification(OK|EF|ZK|PO)$')


def parse_file(f):
    for event, xml in etree.iterparse(f):
        if VALID_NOTIFICATIONS.search(str(xml.tag)):
            for lot_dict in read_notifications(xml):
                #Lot(**lot_dict).save()
                print lot_dict
        elif str(xml.tag).endswith('}organization'):
            cust_dict = read_customer(xml)
            #Customer(**cust_dict).save()
            print cust_dict


def process_file(f, filename):
    # ignoring non-notifications for now #####
    if filename.find('notification') < 0 and filename.find('organization') < 0:
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
