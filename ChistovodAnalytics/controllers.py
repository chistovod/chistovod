import os
import re
from zipfile import ZipFile

from os.path import expanduser

from lxml import etree

from zakupki_xml_parser import *

#from models import *

VALID_NOTIFICATIONS = re.compile('\}notification(OK|EF|ZK|PO)$')
VALID_PROTOCOLS = re.compile('\}protocol(OK1|EF3|ZK1|ZK5|PO1)$')

VALID_FILE_PREFIXI = ['organization', 'notification', 'protocol', 'contract']
ORDERS = tuple(enumerate(VALID_FILE_PREFIXI))


def parse_file(f):
    for event, xml in etree.iterparse(f, huge_tree=True):
        if VALID_NOTIFICATIONS.search(str(xml.tag)):
            for lot_dict in read_lots_from_notification(xml):
                #Lot(**lot_dict).save()
                print lot_dict
        elif str(xml.tag).endswith('}organization'):
            cust_dict = read_customer(xml)
            #Customer(**cust_dict).save()
            print cust_dict
        elif VALID_PROTOCOLS.search(str(xml.tag)):
            suppliers, contacts, supplier_to_lot = read_suppliers_and_contacts_from_protocols(xml)
            #Supplier
            #Contact
            print suppliers
            print contacts


def process_file(f, filename):

    # process only files with valid prefix
    if all([filename.find(prefix) == -1 for prefix in VALID_FILE_PREFIXI]):
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


def get_file_parse_order(file_name):
    fn = file_name.lower()
    for order, prefix in ORDERS:
        if fn.startswith(prefix):
            return order
    return len(ORDERS)


def os_flat_walk(path):
    for root, subfolders, files in os.walk(path):
        for f in files:
            filepath = os.path.join(root, f)
            yield (filepath, get_file_parse_order(f))


def process_all_files():
    path = os.path.join(expanduser('~'), 'zakupki.gov.ru')
    for filepath, order in sorted(os_flat_walk(path), key=itemgetter(1)):
        process_any_file(filepath)


if __name__ == "__main__":
    process_all_files()
