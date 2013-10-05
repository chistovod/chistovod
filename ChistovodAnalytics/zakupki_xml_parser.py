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


def read_notification(xml):
    get_xml_value = lambda *args: get_value(xml, *args)
    return {
        'notification_id': get_xml_value('./t:id/text()', int),
        'notification_number': get_xml_value('./t:notificationNumber/text()'),
        'create_date': get_xml_value('./t:createDate/text()', dt),
        'publish_date': get_xml_value('./t:publishDate/text()', dt),
        'order_name': get_xml_value('./t:orderName/text()'),
        'href': get_xml_value('./t:href/text()'),
        'reg_num': get_xml_value('./t:order/t:placer/t:regNum/text()', int),
        'max_price': get_xml_value(
            './t:lots/t:lot/t:customerRequirements/t:customerRequirement/t:maxPrice/text()', float, sum)
    }


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

