from Users import Users

def ordering(SITE):
    SITE.debug('PATH: /system/users/ordering.py')

    act = SITE.p[2]
    id = SITE.p[3]
    USER = Users(SITE)
    USER.setOrdering(id, act)
    return {'redirect': '/system/users'}