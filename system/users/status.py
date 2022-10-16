from Users import Users

def status(SITE):
    SITE.debug('PATH: /system/users/status.py')
    status = 1 if SITE.p[2] == 'pub' else 0
    id = SITE.p[3]
    USER = Users(SITE)
    USER.setStatus(id, status)
    return {'redirect': '/system/users'}
