import os
from Projects import Projects

def insert(SITE):
    SITE.debug('PATH: /system/projects/insert.py')

    data = {
        'user_id': SITE.p[3],
        'domain': SITE.post['domain'],
        'name': SITE.post['name'].replace('"', '&quot;'),
        'title': SITE.post['title'].replace('"', '&quot;'),
        'description': SITE.post['description'],
        'settings': {
            'intro_text': SITE.post['intro_text'].replace('"', '&quot;'),
            'intro_speech': SITE.post['intro_speech'].replace('"', ''),
        },
        'status': 1 if 'status' in SITE.post else 0
    }

    PROJECT = Projects(SITE)
    data['ordering'] = PROJECT.getMaxOrdering() + 1
    project_id = PROJECT.insert(data)
    
    path = 'files/projects/'+str(project_id)+'/model'

    if not os.path.isdir(path):
        os.makedirs(path, mode=0o755, exist_ok=True)

    return {'redirect': '/system/projects'}
