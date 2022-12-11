import json
from Projects import Projects


def get_intro_ajax(SITE):
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
    intro = PROJECTS.getIntroByDomain(domain)
    if SITE.debug_on:
        print(f'DOMAIN: {domain}, INTRO: {intro}')			

    answer = {'answer': 'success', 'intro_text': intro['intro_text'], 'intro_speech': intro['intro_speech']}
    return json.dumps(answer)
