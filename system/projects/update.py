from Projects import Projects

def update(SITE):
    SITE.debug('PATH: /system/projects/update.py')

    data = {}
    data['domain'] = SITE.post['domain']
    data['name'] = SITE.post['name'].replace('"', '&quot;')
    data['title'] = SITE.post['title'].replace('"', '&quot;')
    data['description'] = SITE.post['description']
    data['status'] = 1 if 'status' in SITE.post else 0
   
    data['id'] = SITE.p[3]
    PROJECT = Projects(SITE)
    PROJECT.update(data)
    return {'redirect': '/system/projects'}
