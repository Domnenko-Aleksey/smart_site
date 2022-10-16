from Users import Users

def update(SITE):
    SITE.debug('PATH: /system/users/update.py')
    name = SITE.post['name']
    email = SITE.post['email']
    status = 1 if 'status' in SITE.post else 0
    
    if name == '' or email == '':
        SITE.content = '<h1>Ошибка - не заполнено поле</h1>'
    else:
        id = SITE.p[3]
        USER = Users(SITE)
        USER.update(id, name, email, status)
        return {'redirect': '/system/users'}
