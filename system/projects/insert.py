import os
from Projects import Projects

def insert(SITE):
    SITE.debug('PATH: /system/projects/insert.py')
    data = {}
    data['user_id'] = SITE.p[3]
    data['domain'] = SITE.post['domain']
    data['name'] = SITE.post['name']
    data['title'] = SITE.post['title']
    data['description'] = SITE.post['description']
    data['status'] = 1 if 'status' in SITE.post else 0

    PROJECT = Projects(SITE)
    data['ordering'] = PROJECT.getMaxOrdering() + 1
    project_id = PROJECT.insert(data)
    
    path = 'files/projects/'+str(project_id)+'/model'

    if not os.path.isdir(path):
        os.makedirs(path, mode=0o755, exist_ok=True)

    return {'redirect': '/system/projects'}
