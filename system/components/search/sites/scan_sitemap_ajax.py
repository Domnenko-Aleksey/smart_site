import re
import requests
import xml.etree.ElementTree as ET
import json
from Search import Search

def scan_sitemap_ajax(SITE):
    SITE.debug('PATH: /system/components/search/scan_sitemap_ajax.py')
    id = SITE.post['id']

    SEARCH = Search(SITE)
    site = SEARCH.sitesGetItem(id)

    # Валидность 'sitemap_url'
    try:
        r = requests.get(site['sitemap_url'])
    except:
        answer = {'answer': 'success', 'message': 'Ошибка URL sitemap.xml'}
        return {'ajax': json.dumps(answer)}

    # Если ответ != 200 -> выдаём ошибку
    if int(r.status_code) != 200:
        answer = {'answer': 'success', 'message': 'Ошибка подключения к sitemap.xml'}
        return {'ajax': json.dumps(answer)}

    xml_string = re.sub(' xmlns="[^"]+"', '', r.text, count=1)  # Удаляем пространство имён
    xml = ET.fromstring(xml_string)
    Search.sitemap_xml = xml
    
    answer = {'answer': 'success', 'page_count_num': len(xml), 'message' :''}
    return {'ajax': json.dumps(answer)}