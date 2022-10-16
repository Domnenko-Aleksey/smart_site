import requests
import json
import re
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from bs4 import Comment
from Search import Search


def scan_page_ajax(SITE):
    SITE.debug('PATH: /system/components/search/sites/scan_page_ajax.py')
    site_id = SITE.post['id']
    act = SITE.post['act']

    SEARCH = Search(SITE)

    if act == 'sitemap':
        # В этом режиме мы получаем URl из sitemap
        page_current_num = int(SITE.post['page_current_num'])

        # Проверяем на окончание процесса - очищаем Search.sitemap_xml после обработки
        if page_current_num >= len(Search.sitemap_xml):
            Search.sitemap_xml = False
            answer = {'answer': 'success', 'message' :''}
            return {'ajax': json.dumps(answer)}

        # Получаем url страницы
        url = Search.sitemap_xml[page_current_num].find('loc').text
    else:
        # В этом режиме ('act' = 'URL') URL получаем из POST
        url = SITE.post['url']


    # --- ПОЛУЧАЕМ REQUEST ---
    try:
        r = requests.get(url)
    except:
        answer = {'answer': 'success', 'message' :'Ошибка sitemap URL: ' + url}
        return {'ajax': json.dumps(answer)}

    # Если ответ != 200 -> выдаём ошибку
    if int(r.status_code) != 200:
        answer = {'answer': 'success', 'message' :'Ошибка доступа к странице: ' + url}
        return {'ajax': json.dumps(answer)}


    # --- BS ---
    pattert = re.compile('[\n\t]')
    soup = BeautifulSoup(r.text, 'html.parser')

    tag_title = soup.title.text if soup.title else ''  # Тег <title>

    node = soup.find('meta', attrs={'name': 'description'})
    tag_description =  pattert.sub(' ', node['content']).strip() if node else ''


    # --- BODY ---
    body = soup.body

    # Удаляем закомментированный текст
    for child in body:
        if isinstance(child, Comment):
            print('--- DELETE ---')
            print(child)
            child.extract()

    # Удаляем стили и скрипты
    [s.extract() for s in body(['style', 'script', 'noindex', 'menu'])]

    # Удаляем меню
    [s.extract() for s in body.findAll(attrs={'class': re.compile('(top)|(menu)|(footer)|(breadcrumb)|(contact)')})]

    node = body.find('h1')
    h1 = node.text if node else ''

    node = body.find('img', attrs={'itemprop': 'image'})
    img = node['src'] if node else ''

    node = body.find(attrs={'itemprop': 'price'})
    price = node.text if node else ''

    node = body.find(attrs={'itemprop': 'priceCurrency'})
    price_currency = node.text if node else ''

    node = body.find(attrs={'itemprop': 'description'})
    item_description = node.text if node else ''

    price_out = ''

    if (len(h1) < 150) and (len(h1) > len(tag_title)):
        title = h1.replace('  ', ' ').strip()
    else:
        title = tag_title.replace('  ', ' ').strip()

    if (len(item_description) < 500) and (len(item_description) > len(tag_description)):
        description = pattert.sub(' ', item_description)
    else:
        description = tag_description

    if price != '':
        price_out = price.strip()
        if price_currency:
            price_out += price_currency.replace(' ', '')



    # Что бы текст не слипался - после каждого тега ставим пробел, почистим далее
    text_arr = body.findAll(text=True)
    text_str = ''
    for t in text_arr:
        text_str += t + '. '

    # Добавляем в текст тайтл и дескрипшн
    # text = tag_title + ' ' + tag_description + ' ' + text_str
    text = title + ' ' + description
    text = clear_text(text)

    if SITE.debug_on:
        print('URL:', url)
        print(f'TAG TITLE ({len(tag_title)}): {tag_title}')
        print(f'TAG DESCRIPTION ({len(tag_description)}): {tag_description}')
        print(f'H1 ({len(h1)}): {h1}')
        print('IMG:', img)
        print(f'ITEM DESCRIPTION ({len(item_description)}): {item_description}')
        print('PRICE:', price)
        print('PRICE CURRENCY:', price_currency)
        print('------------')
        print('TITLE:', title)
        print('DESCRIPTION:', description)
        print('PRICE OUT:', price_out)
        print('TEXT NORM:', text)
        print('------------')

    # Получаем BERT-вектор для текста:
    param = {'text': text}
    bert_req = requests.post('http://127.0.0.1:9003/bert_api', data=param)
    if int(bert_req.status_code) != 200:
        answer = {'answer': 'error', 'message': ''}
        return {'ajax': json.dumps(answer)}

    vector = bert_req.json()['vector']

    SITE.debug(f'BERT: {len(vector)}')
    # SITE.debug(vector)


    # Записываем или обновляем записи в базе данных
    data = {
        'url': url,
        'vector': vector,
        'title': title,
        'description': description,
        'image': img,
        'price': price,
        'site_id': site_id
    }
    set = SEARCH.pagesSetData(data)

    if act == 'sitemap':
        answer = {'answer': 'success', 'message': ''}
    else:
        message = 'Страница добавлена' if set == 'insert' else 'Страница обновлена'
        answer = {'answer': 'success', 'message': message}      
    return {'ajax': json.dumps(answer)}



def clear_text(text):
    # Очищаем текст от переносов, пробелов
    text = re.sub(r'[\n\t]', '', text)
    text = re.sub(r'(\s+\.)+', '', text)
    text = text.replace('..', '.')
    text = text.replace('-.', '-')
    text = text.replace('—.', '-')
    text = text.replace('!.', '!')
    text = text.replace('?.', '?')
    text = text.replace(':.', ':').strip()

    return text