from Users import Users

def insert(SITE):
    SITE.debug('PATH: /system/users/insert.py')
    name = SITE.post['name']
    email = SITE.post['email']
    status = 1 if 'status' in SITE.post else 0
    
    if name == '' or email == '':
        SITE.content = '<h1>Ошибка - не заполнено поле</h1>'
    else:
        USER = Users(SITE)
        u = USER.getUserByEmail(email)
        
        # Проверка того, что пользователь уже зарегистрирован.
        if u:
            SITE.content = '<h1>Пользователь уже зарегистрирован</h1>'
        else:
            USER.insert(name, email, status)
            return {'redirect': '/system/users'}
