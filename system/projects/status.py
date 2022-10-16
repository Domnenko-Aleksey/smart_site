from Projects import Projects

def status(SITE):
    SITE.debug('PATH: /system/projects/status.py')

    status = 1 if SITE.p[2] == 'pub' else 0
    id = SITE.p[3]
    PROJECTS = Projects(SITE)
    PROJECTS.setStatus(id, status)
    return {'redirect': '/system/projects'}
