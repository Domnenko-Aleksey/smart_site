from Projects import Projects

def ordering(SITE):
    SITE.debug('PATH: /system/projects/ordering.py')

    act = SITE.p[2]
    id = SITE.p[3]
    PROJECT = Projects(SITE)
    PROJECT.setOrdering(id, act)
    return {'redirect': '/system/projects'}