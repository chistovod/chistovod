import traceback
from datetime import datetime
from lxml import etree
from zipfile import ZipFile
from io import BytesIO


def retr(ftp, path, filename):
    bio = BytesIO()
    req = '{ftp_method}{path}{dash}{filename}'.format(ftp_method='RETR ', path=path, dash='/', filename=filename)
    resp = ftp.retrbinary(req, callback=lambda more_data: bio.write(more_data))
    print(req, ' STATUS: ', resp)
    return bio


def unzip(binary_zip):  # zipfile path or binary
    with ZipFile(binary_zip) as zf:
        return [zf.read(unzf) for unzf in zf.namelist()]


def extract(ftp, path, filename):
    try:
        zip_binary = retr(ftp, path, filename)
        xml_files = unzip(zip_binary)
    except KeyboardInterrupt:
        traceback.print_exc()
        exit()
    except AttributeError:
        traceback.print_exc()
        exit()
    except:
        traceback.print_exc()
        return None
    return xml_files


def parse_datetime(date):
    return datetime.strptime(date[:19], '%Y-%m-%dT%H:%M:%S')


def parse_date(date):
    return datetime.strptime(date, '%Y-%m-%d')


def recursive_dict(element):
    return etree.QName(element.tag).localname, dict(map(recursive_dict, element)) or element.text
