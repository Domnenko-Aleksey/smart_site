import json
from Projects import Projects
from Favorites import Favorites


def mainpage(SITE):
    SITE.debug('PATH: /system/favorites/favorites.py')

    SITE.addHeadFile('/lib/DAN/DAN.css')
    SITE.addHeadFile('/system/templates/css/favorites.css')

    project_id = int(SITE.p[2])
    
    PROJECT = Projects(SITE)
    project = PROJECT.getProject(project_id, True)

    # Вопрос - ответ
    FAVORITES = Favorites(SITE)
    favorites = FAVORITES.getByProjectId(project_id, 100)
    favorites_tr_html = ''
    if favorites:
        for n, fav in enumerate(favorites):
            fav_arr = json.loads(fav['favorites'])
            fav_list = fav_arr.values()
            fav_str = '<br>'.join(fav_list)
            favorites_tr_html += f'''<tr><td>{n+1}</td><td><div class="fav_str">{fav_str}</div></td><td>{fav['date_l']}</td><td>{fav['date_c']}</td></tr>'''


    SITE.content = f'''
        <h1>{project['name']}</h1>
        <div class="user_name_container">
            <a class="user_name" href="/system/users/edit/{project['user_id']}">{project['user_name']} <span class="user_name_email">{project['user_email']}</span></a>
        </div>
        <div class="dan_flex_row_start">
            <a href="/system/items/{project['id']}" class="ico_square">
                <svg><use xlink:href="/system/templates/images/sprite.svg#content"></use></svg>
                <div class="ico_square_text">Контент</div>
            </a>
            <a href="/system/visitors/{project['id']}" class="ico_square">
                <svg><use xlink:href="/system/templates/images/sprite.svg#users"></use></svg>
                <div class="ico_square_text">Посетители</div>
            </a>
            <a href="/system/favorites/{project['id']}" class="ico_square">
                <svg><use xlink:href="/system/templates/images/sprite.svg#favorite"></use></svg>
                <div class="ico_square_text">Избранное</div>
            </a>
            <a href="/system/favorites/{project['id']}" class="ico_square">
                <svg><use xlink:href="/system/templates/images/sprite.svg#question"></use></svg>
                <div class="ico_square_text">Вопрос - ответ</div>
            </a>
        </div>
        <h3>Вопрос - ответ</h3>
        <table class="admin_table dan_even_odd">
            <tr>
                <th style="width:50px">№</th>
                <th style="width:250px">Избранное</th>
                <th style="width:150px">Последняя</th>
                <th style="width:150px">Создание</th>
            </tr>
            {favorites_tr_html}
        </table>   
    '''