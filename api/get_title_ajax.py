import json
from Projects import Projects


def get_title_ajax(SITE):
    SITE.debug('PATH: /api/get_title_ajax.py')
    SITE.debug('POST')
    SITE.debug(SITE.post)

    PROJECTS = Projects(SITE)

    if 'domain' in SITE.post:
        domain = SITE.post['domain']
    else:
        answer = {'answer': 'success', 'message': 'Domain is NaN'}
        return json.dumps(answer)

    # --- Получение ответа ---
    title = PROJECTS.getTitleByDomain(domain)
    if SITE.debug_on:
        print(f'DOMAIN: {domain}, TITLE: {title}')			

    answer = {'answer': 'success', 'title': title}
    return json.dumps(answer)
