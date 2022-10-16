import json
import requests
from Search import Search

def search_test(SITE):
    SITE.debug('PATH: /system/components/search/sites/search_test.py')

    SITE.addHeadFile('/system/lib/DAN/DAN.css')
    SITE.addHeadFile('/system/templates/components/search/templates/css/search_test.css')


    site_id = SITE.post['site_id']
    text = SITE.post['text']

    SITE.debug('SITE ID: ' + site_id)
    SITE.debug('TEXT: ' + text)

    SEARCH = Search(SITE)
    site = SEARCH.sitesGetItem(site_id)

    if len(text) > 2:
        # API для поиска
        param = {'site_id': site_id, 'text': text}
        api_req = requests.post('http://127.0.0.1:9007/api/search/get_search', data=param)
        if int(api_req.status_code) != 200:
            return json.dumps({'answer': 'error', 'message': ''})
        content = api_req.json()['content']
    else:
        content = '<div>Слишком короткий запрос</div>'

    SITE.content = f'''
        <h1>Тестирование поиска для сайта {site["site"]}</h1>
        <div>
        <form method="post" action="/system/com/search/sites/search_test" enctype="multipart/form-data">
            <div class="ss_flex_row_v_centr">
                <div style="margin-right:5px">
                    <input class="dan_input w_400" name="text" type="text" value="{text}">
                    <input name="site_id" type="hidden" value="{site_id}">
                </div>
                <div style="margin-right:5px">
                    <input id="modal_submit" class="dan_button_green" type="submit" name="submit" value="Поиск">
                </div>
            </div>
        </form> 
        </div>
        {content}
    '''