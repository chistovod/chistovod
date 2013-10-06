from datetime import datetime
from operator import itemgetter
import re

DIGITS = re.compile('[^\w]')

identity = lambda x: x


def strip(s):
    return s.strip()


def nullable(aggregate_func=itemgetter(0), null_value=None):
    return lambda lst: aggregate_func(lst) if lst else null_value


def get_value(xml, xpath, transform=strip, aggregate=itemgetter(0)):
    try:
        return aggregate([transform(x) for x in (xml.xpath(xpath,
                                                           namespaces={'t': 'http://zakupki.gov.ru/oos/types/1'},
                                                           smart_strings=False))])
    except:
        print "ERROR:", xml, xpath
        raise


def dt(date):
    return datetime.strptime(date.strip(), '%Y-%m-%dT%H:%M:%S')


def d(date):
    return datetime.strptime(date.strip(), '%Y-%m-%d')


def phone(s):
    return DIGITS.sub('', s)


def read_lot(xml):
    return {
        'max_price': get_value(xml, './t:customerRequirements/t:customerRequirement/t:maxPrice/text()', float, sum),
        'lot_name': get_value(xml, './t:subject/text()'),
        'ordinal_number': get_value(xml, './t:ordinalNumber/text()', int)}


def read_lots_from_notification(xml):
    get_xml_value = lambda *args: get_value(xml, *args)
    notification = {
        'notification_number': get_xml_value('./t:notificationNumber/text()'),
        'create_date': get_xml_value('./t:createDate/text()', dt),
        'publish_date': get_xml_value('./t:publishDate/text()', dt),
        'notification_name': get_xml_value('./t:orderName/text()'),
        'href': get_xml_value('./t:href/text()'),
        'reg_num': get_xml_value('./t:order/t:placer/t:regNum/text()', int),

        'final_price': None,
        'contract_sign_date': None,
        'execution_date': None}

    lots_xml = get_value(xml, './t:lots', transform=identity)
    lots = [read_lot(lot_xml) for lot_xml in lots_xml.iterchildren()]

    return [dict(lot.items() + notification.items()) for lot in lots]


def read_contract(xml):
    get_xml_value = lambda *args: get_value(xml, *args)
    return {
        'id': get_xml_value('./t:id/text()', int),
        'sign_date': get_xml_value('./t:signDate/text()', d),
        'price': get_xml_value('./t:price/text()', float),
        'current_contract_stage': get_xml_value('./t:currentContractStage/text()'),
        'execution': "-".join([get_xml_value('./t:execution/t:year/text()'),
                               get_xml_value('./t:execution/t:month/text()')])
    }


def safe_concat(*nullable_strings):
    """if all values are None than returns None"""
    not_null_strings = [s for s in nullable_strings if s]
    if not_null_strings:
        return ' '.join(not_null_strings)
    return None


def read_suppliers_and_contacts_from_protocols(xml):
    """Returns tuple of [Supplier] and [Contact] and [lot participant]"""
    suppliers = []
    contacts = []
    lot_participants = []
    notification_number = get_value(xml, './t:notificationNumber/text()')
    for protocol_lot_xml in get_value(xml, './t:protocolLots', transform=identity, aggregate=nullable(null_value=[])):
        lot_number = get_value(protocol_lot_xml, './t:lotNumber/text()', int)
        for application_xml in get_value(protocol_lot_xml,
                                         './t:applications',
                                         transform=identity,
                                         aggregate=nullable(null_value=[])):
            for participant_xml in get_value(application_xml, './t:applicationParticipants', transform=identity):
                inn = get_value(participant_xml, './t:inn/text()', int)
                form = get_value(participant_xml, './t:organizationForm/text()', aggregate=nullable())
                name = get_value(participant_xml, './t:organizationName/text()', aggregate=nullable())
                supplier = {
                    'inn': inn,
                    'name': safe_concat(form, name)
                }
                suppliers.append(supplier)
                contact = {
                    'inn': inn,
                    'last_name': get_value(participant_xml, './t:contactInfo/t:lastName/text()'),
                    'first_name': get_value(participant_xml, './t:contactInfo/t:firstName/text()'),
                    'middle_name': get_value(participant_xml, './t:contactInfo/t:middleName/text()'),
                    'email': get_value(participant_xml, './t:contactInfo/t:contactEMail/text()', aggregate=nullable()),
                    'phone': get_value(participant_xml, './t:contactInfo/t:contactPhone/text()', phone,
                                       aggregate=nullable()),
                    'fax': get_value(participant_xml, './t:contactInfo/t:contactFax/text()', phone, aggregate=nullable()),
                }
                contacts.append(contact)
                lot_participant = {
                    'notification_number': notification_number,
                    'lot_number': lot_number,
                    'supplier_inn': inn
                }
                lot_participants.append(lot_participant)

    return suppliers, contacts, lot_participants


def read_customer(xml):
    get_xml_value = lambda *args: get_value(xml, *args)
    return {
        'registration_number': get_xml_value('./t:regNumber/text()', int),
        'inn': get_xml_value('./t:inn/text()', int),
        'okato': get_xml_value('./t:factualAddress/t:OKATO/text()', int),
        'name': get_xml_value('./t:fullName/text()')
    }
