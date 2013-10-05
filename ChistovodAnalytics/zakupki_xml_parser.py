from datetime import datetime
from operator import itemgetter


def strip(s):
    return s.strip()


def get_value(xml, xpath, transform=strip, aggregate=itemgetter(0)):
    return aggregate([transform(x) for x in (xml.xpath(xpath,
                                                       namespaces={'t': 'http://zakupki.gov.ru/oos/types/1'},
                                                       smart_strings=False))])


def dt(date):
    return datetime.strptime(date.strip(), '%Y-%m-%dT%H:%M:%S')


def d(date):
    return datetime.strptime(date.strip(), '%Y-%m-%d')


def read_lot(xml):
    get_xml_value = lambda *args: get_value(xml, *args)
    return {
        'max_price': get_value('./t:customerRequirements/t:customerRequirement/t:maxPrice/text()', float, sum),
        'sid': None,
        'lot_name': None}


def read_notification(xml):
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
        'execution': None}
    lots_xml = get_value(xml, './t:lots', transform=lambda x: x)
    lots = [read_lot(lot_xml) for lot_xml in lots_xml.iterchildren()]

    return [dict(lot.items() + notification.items()) for lot in lots]



def read_contracts(xml):
    get_xml_value = lambda *args: get_value(xml, *args)
    return {
        'id': get_xml_value('./t:id/text()', int),
        'sign_date': get_xml_value('./t:signDate/text()', d),
        'price': get_xml_value('./t:price/text()', float),
        'current_contract_stage': get_xml_value('./t:currentContractStage/text()'),
        'execution': "-".join([get_xml_value('./t:execution/t:year/text()'),
                              get_xml_value('./t:execution/t:month/text()')])
    }


def read_protocol(xml):
    get_xml_value = lambda *args: get_value(xml, *args)

