import json
import uuid
from Projects import Projects
from Visitors import Visitors
from Favorites import Favorites


def get_fav_ajax(SITE):
    SITE.debug('PATH: /api/get_fav_ajax.py')

    if 'domain' in SITE.post:
        domain = SITE.post['domain']
    else:
        answer = {'answer': 'success', 'message': 'Domain is NaN'}
        return json.dumps(answer)

    PROJECTS = Projects(SITE)
    project_id = PROJECTS.getProjectIdByDomain(domain)

    if not project_id:
        answer = {'answer': 'success', 'message': 'Project not found'}
        return json.dumps(answer)

    VISITORS = Visitors(SITE)

    ss_cid = SITE.post['ss_cid']
    SITE.debug(f'COOKIES: {ss_cid}')
 
    if len(ss_cid) != 32:
        # Устанавливаем новые куки
        ss_cid_new = uuid.uuid4().hex
        visitor_id = VISITORS.insert(ss_cid_new)  # Добавляем посетителя
        SITE.debug(f'НОВОЕ COOCKES: {ss_cid_new}')
    else:
        visitor_id = VISITORS.check(ss_cid)  # Проверяем посетителя. Если не найден - добавляем
        ss_cid_new = ''

    FAVORITES = Favorites(SITE) 
    fav = FAVORITES.getFavoritesByProjectIdVisitorId(project_id, visitor_id)

    fav_dict = {}
    if fav:
        for id in fav['favorites']:
            SITE.debug(f'FAVORITES ID: {id}')
            fav_dict[id] = fav['favorites'][id]

    answer = {'answer': 'success', 'ss_cid_new': ss_cid_new, 'favorites': fav_dict}
    return json.dumps(answer)
