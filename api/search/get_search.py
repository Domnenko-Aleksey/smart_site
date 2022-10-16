# import time
import requests
import json
import numpy as np
from scipy.spatial.distance import cosine
from aiohttp import web
import api
from Search import Search
from nltk.stem import SnowballStemmer

SEARCH = Search(api.SITE)

# --- ПОЛУЧАЕМ РАБОЧИЕ САЙТЫ ---
sites_list = SEARCH.getSitesList()
sites_dict = {}   # Cловарь. Ключи - project_id, значение - vмаасив страниц [[id, vector]]

# --- СОЗДАЁМ СЛОВАРИ САЙТОВ ---
for s in sites_list:
    pages = SEARCH.getPagesList(s['id'])
    pages_list = []
    for p in pages:
        vector = np.frombuffer(p['vector'], dtype=float)
        pages_list.append([p['id'], vector])
    sites_dict[s['id']] = pages_list  # np.array(pages_list, dtype=object)

# --- ДЛЯ СТЕММИНГА ---
snowball = SnowballStemmer(language="russian")


def get_search(SITE):
    SITE.debug('PATH: /api/get_search/get_search.py')

    site_id = SITE.post['site_id']
    text = SITE.post['text']

    # Получаем BERT-вектор для текста:
    param = {'text': text}
    bert_req = requests.post('http://127.0.0.1:9003/bert_api', data=param)
    if int(bert_req.status_code) != 200:
        return json.dumps({'answer': 'error', 'message': ''})
    vector = np.array(bert_req.json()['vector'])

    SITE.debug('SITE ID:' + site_id)
    SITE.debug('TEXT:' + text)
    SITE.debug(f'VECTOR: {vector.shape}')

    '''
    test_list = [
        'создание сайтов в самаре',
        'создание сайтов в самаре создание сайтов в самаре создание сайтов в самаре',
        'участие в хакатоне цифрового прорыва',
        'в самаре создание сайтов',
        'продвижение сайтов',
        'продвижение в соцсетях',
        'создание сайтов',
        'наши координаты',
        'разработка сайтов',
        'съёмка с квадрокоптеров',
        'фото и видеосъёмка',
        'бухгалтерские услуги',
        'король',
        'королева',
        'некий текст в котором стоит крп-5б'
    ]


    test_vextor_list = []
    for text in test_list:
        param = {'text': text}
        bert_req = requests.post('http://127.0.0.1:9003/bert_api', data=param)
        if int(bert_req.status_code) != 200:
            return json.dumps({'answer': 'error', 'message': ''})
        vec = np.array(bert_req.json()['vector'])
        test_vextor_list.append(vec)


    cos_list = []
    for t, v in zip(test_list, test_vextor_list):
        cos = cosine(v, vector)
        cos_list.append([cos, t])


    sorted_list = sorted(cos_list, key=lambda x: x[0])   # сортируем по косинусному расстоянию

    for s in sorted_list:
        print(s)



    '''

    # --- КОСИНУСНОЕ РАССТОЯНИЕ ---
    cos_list = []
    for el in sites_dict[int(site_id)]:
        cos = cosine(el[1], vector)
        cos_list.append([el[0], cos])

    sorted_list = sorted(cos_list, key=lambda x: x[1])   # сортируем по косинусному расстоянию
    print(sorted_list)

    # --- СТЕММИНГ - ЛИСТ ДЛЯ ПОИСКОВОГО ЗАПРОСА ---
    search_stem_list = []
    for t in text.split():
        search_stem_list.append(snowball.stem(t)) 

    SITE.debug('SARCH STEMMING:')
    SITE.debug(search_stem_list)

    content = ''
    for s in sorted_list[0:20]:
        page = SEARCH.getPage(site_id, s[0])

        title_list = page["title"].split()
        description_list = page["description"].split()

        # Стемминг поискового запроса
        for stm in search_stem_list:
            # Тайтл
            for i, ttl in enumerate(title_list):
                if ttl.lower().find(stm.lower()) != -1:
                    title_list[i] = f'<b>{ttl}</b>'
            # Дескрипшн
            for i, dsc in enumerate(title_list):
                if dsc.lower().find(stm.lower()) != -1:
                    description_list[i] = f'<b>{dsc}</b>'

        title = ' '.join(title_list)
        description = ' '.join(description_list)

        img = f'<img class="ss_image" src="{page["image"]}">' if page['image'] else ''
        content +=  '<div class="ss_flex_row">'
        content +=      img
        content +=      '<div>'
        content +=          f'<a target="blank" href="{page["url"]}" class="ss_title">{title}</a>'
        content +=          f'<div class="ss_description">{description}</div>'
        content +=          f'<div class="ss_price">{page["price"]}</div>'
        content +=      '</div>'
        content +=  '</div>'






    answer = {'content': content}
    return json.dumps(answer)