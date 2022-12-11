from Projects import Projects
from Users import Users

def edit(SITE):
    SITE.debug('PATH: /system/projects/edit.py')

    SITE.addHeadFile('/lib/DAN/DAN.css')
    SITE.addHeadFile('/lib/DAN/DAN.js')
    SITE.addHeadFile('/system/templates/css/edit.css')

    if SITE.p[2] == 'add':
        user_id = SITE.p[3]
        title = 'Добавить'
        act = 'insert/' + user_id
        project = {
            'domain': '',
            'name': '',
            'title': '',
            'description': ''
        }
        status_checked = ''
        USER = Users(SITE)
        user = USER.getUser(user_id)
        user_name = user['name']
        user_email = user['email']
    else:
        id = SITE.p[3]
        title = 'Редактировать'
        act = 'update/' + id
        PROJECT = Projects(SITE)
        project = PROJECT.getProject(id, user=True)
        status_checked = 'checked=""' if project['status'] == 1 else '';
        user_name = project['user_name']
        user_email = project['user_email']

    SITE.content = f'''
        <h1>{title} проект</h1>
        <form method="post" action="/system/projects/{act}" enctype="multipart/form-data">
        <div class="dan_flex_row">
            <div class="tc_l">Пользователь</div>
            <div class="tc_r dan_flex_grow">
                <b>{user_name} ({user_email})</b>
            </div>
        </div>
        <div class="dan_flex_row">
            <div class="tc_l">Домен</div>
            <div class="tc_r dan_flex_grow">
                <input class="dan_input w_400" name="domain" type="text" required="" value="{project['domain']}">
            </div>
        </div>
        <div class="dan_flex_row">
            <div class="tc_l">Наименование проекта</div>
            <div class="tc_r dan_flex_grow">
                <input class="dan_input w_400" name="name" type="text" required="" value="{project['name']}">
            </div>
        </div>
        <div class="dan_flex_row">
            <div class="tc_l">Метатег "Title"</div>
            <div class="tc_r dan_flex_grow">
                <input class="dan_input w_400" name="title" type="text" required="" value="{project['title']}">
            </div>
        </div>
        <div class="dan_flex_row">
            <div class="tc_l">Метатег "Description"</div>
            <div class="tc_r dan_flex_grow">
                <textarea class="dan_input w_400" name="description" rows="3">{project['description']}</textarea>
            </div>
        </div>
        <div class="dan_flex_row">
            <div class="tc_l">Вступление - текст</div>
            <div class="tc_r dan_flex_grow">
                <input class="dan_input w_400" name="intro_text" type="text" value="{project['settings']['intro_text']}">
            </div>
        </div>
        <div class="dan_flex_row">
            <div class="tc_l">Вступление - голос</div>
            <div class="tc_r dan_flex_grow">
                <input class="dan_input w_400" name="intro_speech" type="text" value="{project['settings']['intro_speech']}">
            </div>
        </div>
        <div class="dan_flex_row">
            <div class="tc_l">Статус</div>
            <div class="tc_r dan_flex_grow">
                <input id="mp_project_status" class="dan_input" name="status" type="checkbox" value="1" {status_checked}>
                <label for="mp_project_status"></label>
            </div>
        </div>
        <div class="dan_flex_row m_40_0">
            <div class="tc_l">
                <input class="dan_button_green" type="submit" name="submit" value="Сохранить">
            </div>
            <div class="tc_r">
                <a href="/system/projects" class="dan_button_white">Отменить</a>
            </div>
        </div>
        </form>
    '''