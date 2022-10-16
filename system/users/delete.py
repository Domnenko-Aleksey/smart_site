from Users import Users

def delete(SITE):
    SITE.debug('PATH: /system/users/delete.py')
    id = SITE.p[3]
    USER = Users(SITE)
    USER.delete(id)
    return {'redirect': '/system/users'}