from Users import Users

def edit(SITE):
    SITE.debug('PATH: /system/users/edit.py')

    SITE.addHeadFile('/system/lib/DAN/DAN.css')
    SITE.addHeadFile('/system/lib/DAN/DAN.js')
    SITE.addHeadFile('/system/templates/css/edit.css')

    if SITE.p[2] == 'add':
        title = 'Добавить'
        act = 'insert'
        user = {
            'name': '',
            'email': ''
        }
        status_checked = ''
    else:
        title = 'Редактировать'
        id = SITE.p[3]
        act = 'update/' + id
        USER = Users(SITE)
        user = USER.getUser(id)
        status_checked = 'checked=""' if user['status'] == 1 else '';

    tr_html = ''
    SITE.content = f'''
        <h1>{title} пользователя</h1>
        <form method="post" action="/system/users/{act}" enctype="multipart/form-data">
        <div class="dan_flex_row">
            <div class="tc_l">Наименование</div>
            <div class="tc_r dan_flex_grow">
                <input class="dan_input w_400" name="name" type="text" placeholder="ФИО" required="" value="{user['name']}">
            </div>
        </div>
        <div class="dan_flex_row">
            <div class="tc_l">Email</div>
            <div class="tc_r dan_flex_grow">
                <input class="dan_input w_400" name="email" required="" value="{user['email']}">
            </div>
        </div>
        <div class="dan_flex_row">
            <div class="tc_l">Статус</div>
            <div class="tc_r dan_flex_grow">
                <input id="mp_user_status" class="dan_input" name="status" type="checkbox" value="1" {status_checked}>
                <label for="mp_user_status"></label>
            </div>
        </div>
        <div class="dan_flex_row m_40_0">
            <div class="tc_l">
                <input class="dan_button_green" type="submit" name="submit" value="Сохранить">
            </div>
            <div class="tc_r">
                <a href="/system/users" class="dan_button_white">Отменить</a>
            </div>
        </div>
        </form>
    '''