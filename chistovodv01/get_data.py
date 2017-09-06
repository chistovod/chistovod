from ftplib import FTP
from lxml import etree
from chistovodv01.utils import extract, recursive_dict, parse_date
from io import BytesIO

ftp = FTP('ftp.zakupki.gov.ru')
ftp.login(user='fz223free', passwd='fz223free')

region_crawler = {'Altayskii__krai': ''}
protocol_crawler = {'purchaseNoticeOK': '',
                    }

crawler_task = []
reg_path = '/out/published/'
ftp.cwd('{reg_path}'.format(reg_path=reg_path))
region_files = ftp.nlst()
for rfile in region_crawler.keys():  # region_files
    ftp.cwd('{reg_path}{region}'.format(reg_path=reg_path, region=rfile))
    protocol_types = ftp.nlst()
    for protocol in protocol_crawler.keys():  # protocol_types
        protocol_path = '{reg_path}{region}{dash}{protocol}'.format(reg_path=reg_path, region=rfile, dash='/',
                                                                    protocol=protocol)
        ftp.cwd(protocol_path)
        inprotocol_files = ftp.nlst()
        for inp_file in inprotocol_files:  #
            if inp_file.endswith('.xml.zip'):
                crawler_task.append({'file_type': protocol, 'path': protocol_path, 'file_name': inp_file, 'status': 0})
            if inp_file == 'daily':
                daily_path = '{reg_path}{region}{dash}{protocol}{dash}{daily}'.format(reg_path=reg_path, region=rfile,
                                                                                      dash='/', protocol=protocol,
                                                                                      daily='daily')
                ftp.cwd(daily_path)
                daily_files = ftp.nlst()
                for daily_file in daily_files:
                    if daily_file.endswith('.xml.zip'):
                        crawler_task.append(
                            {'file_type': protocol, 'path': daily_path, 'file_name': daily_file, 'status': 0})

# class zakupkiftp(object):
#     def __init__(self):
#         self.ftp = FTP('ftp.zakupki.gov.ru')
#         self.ftp.login(user='fz223free', passwd='fz223free')
#
#     def crawlZakupki(self, region_dit, protocol_dic):
#
#
#
# class zakupkiCrawler(zakupkiftp):
#     pass
#
#
# class zakupliReader(zakupkiftp):
#     pass
#
#
# class ESWritter:
#     pass


xml_files = extract(ftp, crawler_task[-1]['path'], crawler_task[-1]['file_name'])

tag = '{http://zakupki.gov.ru/223fz/purchase/1}purchaseContract'
tag = '{http://zakupki.gov.ru/223fz/purchase/1}purchaseProtocolZK'
tag = '{http://zakupki.gov.ru/223fz/purchase/1}purchaseNoticeOK'
tag = '{http://zakupki.gov.ru/223fz/purchase/1}purchaseProtocolRZOK'


bulk_data = []
for xml_file in xml_files:
    for event, element in etree.iterparse(BytesIO(xml_file), tag=tag):
        doc_type, doc_data = recursive_dict(element)
        print(element)
        # param = {"create": {"_index": "test", "_type": doc_type, "_id": doc_data['body']['item']['guid']}}
        # doc_data['body']['item'].pop('guid')
        # bulk_data.append(param)
        # bulk_data.append(doc_data)
        # print(param)

        iko = doc_data['body']['item']['purchaseNoticeOKData']['customer']['mainInfo']['iko']
        not_dishonest = doc_data['body']['item']['purchaseNoticeOKData']['notDishonest']
        customer = doc_data['body']['item']['purchaseNoticeOKData']['customer']
        PN_reg = doc_data['body']['item']['purchaseNoticeOKData']['registrationNumber']
        lots = doc_data['body']['item']['purchaseNoticeOKData']['lots']
        PN_name = doc_data['body']['item']['purchaseNoticeOKData']['name']
        PN_url = doc_data['body']['item']['purchaseNoticeOKData']['urlOOS']
        PN_code = doc_data['body']['item']['purchaseNoticeOKData']['purchaseCodeName']
        PN_method = doc_data['body']['item']['purchaseNoticeOKData']['purchaseMethodCode']

from collections import defaultdict

        customer = defaultdict(lambda customer: customer)
        customer['purchaseNotifications'] = 1
        {iko: customer}

