import json
import api
import item_html
from Projects import Projects
from Items import Items


def get_id_answer_ajax(SITE):
    SITE.debug('PATH: /api/get_id_answer_ajax.py')
    SITE.debug('POST')
    SITE.debug(SITE.post)

    PROJECTS = Projects(SITE)

    if 'domain' in SITE.post:
        domain = SITE.post['domain']
    else:
        answer = {'answer': 'success', 'message': 'Domain is NaN'}
        return json.dumps(answer)

    # --- Получение ответа ---
    project_id = PROJECTS.getProjectIdByDomain(domain)
    id = SITE.post['id']
    if SITE.debug_on:
        print(f'DOMAIN: {domain}, PROJECT_ID: {project_id}, ID: {id}')

    ITEMS = Items(SITE)
    item = ITEMS.getItem(project_id, id)  

    SITE.debug(f'ITEM_ID: {item["id"]}, ITEM_NAME: {item["name"]}')


    # --- Item HTML ---
    answer_content = item_html.item_html(SITE, item)			

    answer = {'answer': 'success', 'answer_synthesis': item['content']['synthesis'], 'answer_content': answer_content}
    return json.dumps(answer)
