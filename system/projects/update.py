from Projects import Projects

def update(SITE):
    SITE.debug('PATH: /system/projects/update.py')

    data = {
        'domain': SITE.post['domain'],
        'name': SITE.post['name'].replace('"', '&quot;'),
        'title': SITE.post['title'].replace('"', '&quot;'),
        'description': SITE.post['description'],
        'settings': {
            'intro_text': SITE.post['intro_text'].replace('"', '&quot;'),
            'intro_speech': SITE.post['intro_speech'].replace('"', ''),
        },
        'status': 1 if 'status' in SITE.post else 0,
        'id': SITE.p[3]
    }

    PROJECT = Projects(SITE)
    PROJECT.update(data)
    return {'redirect': '/system/projects'}
