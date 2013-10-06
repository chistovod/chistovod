import os
import re
from zipfile import ZipFile

from os.path import expanduser

from lxml import etree
from django.db import transaction

from zakupki_xml_parser import *

from models import *

VALID_NOTIFICATIONS = re.compile('\}notification(OK|EF|ZK|PO)$')
VALID_PROTOCOLS = re.compile('\}protocol(OK1|EF3|ZK1|ZK5|PO1)$')

VALID_FILE_PREFIXI = ['organization', 'notification', 'protocol', 'contract']
ORDERS = tuple(enumerate(VALID_FILE_PREFIXI))


@transaction.commit_manually
def parse_file(f):
    for event, xml in etree.iterparse(f, huge_tree=True):
        if VALID_NOTIFICATIONS.search(str(xml.tag)):
            try:
                for lot_dict in read_lots_from_notification(xml):
                    try:
                        pass
                        Lot(**lot_dict).save()
                    except Exception, ex:
                        print ex, lot_dict
            except Exception, ex:
                print ex, xml.tag
        elif str(xml.tag).endswith('}organization'):
            cust_dict = read_customer(xml)
            try:
                pass
                Customer(**cust_dict).save()
            except Exception, ex:
                print ex, cust_dict
        elif VALID_PROTOCOLS.search(str(xml.tag)):
            suppliers, contacts, supplier_to_lot = read_suppliers_and_contacts_from_protocols(xml)
            for s, c, sl in zip(suppliers, contacts, supplier_to_lot):
                Supplier(**s).save()
                Contact(**c).save()
                pass
        elif str(xml.tag).endswith('}contract'):
            contract_dict = read_contract(xml)
            if not contract_dict['notification_number']:
                continue
            try:
                pass
                Contract(**contract_dict).save()
            except Exception, ex:
                print ex, contract_dict
    transaction.commit()



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
        if filepath.find('201308') == -1:
            continue
        if filepath.find('237') != -1:
            continue
        if filepath.find('235') != -1:
            return


        process_any_file(filepath)


if __name__ == "__main__":
    process_all_files()
