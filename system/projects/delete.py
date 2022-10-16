from Projects import Projects

def delete(SITE):
    SITE.debug('PATH: /system/projects/delete.py')

    id = SITE.p[3]
    PROJECT = Projects(SITE)
    PROJECT.delete(id)

    return {'redirect': '/system/projects'}