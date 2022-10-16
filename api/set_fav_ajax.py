import json
import api
from Projects import Projects
from Visitors import Visitors
from Favorites import Favorites


def set_fav_ajax(SITE):
    SITE.debug('PATH: /api/set_fav_ajax.py')

    if 'domain' not in SITE.post or SITE.post['domain'] == '':
        return

    if 'ss_cid' not in SITE.post or SITE.post['ss_cid'] == '':
        return

    fav_dict = {}
    if SITE.post['ids'] != '':
        id_code_list = SITE.post['ids'].split(',')
        questions_list = SITE.post['questions'].split(',')
        for i, id in enumerate(id_code_list):
            fav_dict[id] = questions_list[i]

    if SITE.debug_on:
        print('POST:', SITE.post)
        print('ITEMS_ID_LIST:', fav_dict)

    # Проект
    PROJECTS = Projects(SITE)
    project_id = PROJECTS.getProjectIdByDomain(SITE.post['domain'])

    # Посетители
    VISITORS = Visitors(SITE)       
    ss_cid = SITE.post['ss_cid']
    visitor_id = VISITORS.check(ss_cid)

    # Избранное
    FAVORITES = Favorites(SITE) 
    FAVORITES.setFavorites(project_id, visitor_id, fav_dict)	

    answer = {'answer': 'success'}
    return json.dumps(answer)
