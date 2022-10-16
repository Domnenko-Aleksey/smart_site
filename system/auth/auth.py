import time
from datetime import datetime
import config

def auth(SITE):
    current_datetime = datetime.now()

    SITE.debug(f'===== AUTH ===== {current_datetime}')
    
    # Статус авторизации - 1, если есть сессия
    if 'auth' in SITE.session:
        SITE.debug(f'Авторизация - успешна, {SITE.session}')
        SITE.auth = 1
        return True

    # Если получаем данные с формы входа
    if (SITE.p[1] == 'auth'):
        if (SITE.request.method == 'POST'):
            SITE.debug(f'Проверка пароля {SITE.post}')
            if ('login' in SITE.post and 
                'password' in SITE.post and
                'button' in SITE.post and
                SITE.post['login'] == config.admin_login and 
                SITE.post['password'] == config.admin_pass):
                SITE.debug('Проверка пароля прошла успешно!')
                SITE.session['auth'] = time.time()
                SITE.auth = 1
                return True

    if not SITE.auth:
        # Нет авторизации - выводим фому
        SITE.addHeadFile('/system/lib/DAN/DAN.css')
        SITE.addHeadFile('/system/templates/css/auth.css')

        SITE.title = 'Авторизация'
        SITE.content = '''<form method="post" action="/system/auth">
        <div class="login_form_container">
            <div class="login_form_text">Логин (admin)</div>
            <div><input name="login" class="dan_input" value=""></div>
            <div class="login_form_text">Пароль</div>
            <div><input name="password" class="dan_input" type="password" value=""></div>
            <div><input name="button" class="dan_input login_form_submit" type="submit" value="Вход"></div>
        </div>
        </form>
        '''
