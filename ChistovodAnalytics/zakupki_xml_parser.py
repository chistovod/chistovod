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


def read_notification(xml):
    get_xml_value = lambda *args: get_value(xml, *args)
    return {
        'notification_id': get_value(xml, './t:id/text()', int),
        'notification_number': get_xml_value('./t:notificationNumber/text()'),
        'create_date': get_xml_value('./t:createDate/text()', dt),
        'publish_date': get_xml_value('./t:publishDate/text()', dt),
        'order_name': get_xml_value('./t:orderName/text()'),
        'href': get_xml_value('./t:href/text()'),
        'reg_num': get_xml_value('./t:order/t:placer/t:regNum/text()', int),
        'max_price': get_xml_value(
            './t:lots/t:lot/t:customerRequirements/t:customerRequirement/t:maxPrice/text()', float, sum)
    }

def read_protocol(xml):
    get_xml_value = lambda *args: get_value(xml, *args)

