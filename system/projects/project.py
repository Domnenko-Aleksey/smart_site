from Projects import Projects
from Sections import Sections


def project(SITE):
    SITE.debug('PATH: /system/projects/project.py')

    SITE.addHeadFile('/system/lib/DAN/DAN.css')
    SITE.addHeadFile('/system/lib/DAN/DAN.js')
    SITE.addHeadFile('/system/lib/DAN/contextmenu/contextmenu.css')
    SITE.addHeadFile('/system/lib/DAN/contextmenu/contextmenu.js')
    SITE.addHeadFile('/system/templates/css/project.css')
    SITE.addHeadFile('/system/templates/js/sections_list.js')

    project_id = int(SITE.p[3])
    
    PROJECT = Projects(SITE)
    project = PROJECT.getProject(project_id, True)

    # Разделы
    SECTIONS = Sections(SITE)
    sections = SECTIONS.getSections(project_id, items_count=True)

    sections_tr_html = ''
    if sections:
        for n, s in enumerate(sections):
            sections_tr_html += f'''
                <tr>
                    <td>{n+1}</td>
                    <td>
                        <svg class="dan_contextmenu_ico contextmenu_menu" title="Действия" data-id="{s['id']}">
                            <use xlink:href="/system/templates/images/sprite.svg#menu"></use>
                        </svg>
                    </td>
                    <td><a href="/system/items/{s["id"]}">{s["name"]} ({s["items_count"]})</></td>
                </tr>'''


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
            <a href="/system/qa/{project['id']}" class="ico_square">
                <svg><use xlink:href="/system/templates/images/sprite.svg#question"></use></svg>
                <div class="ico_square_text">Вопрос - ответ</div>
            </a>
        </div>
        <h3>Разделы</h3>
        <div class="flex_row_start">
            <a href="/system/sections/add/{project['id']}" target="blank" class="ico_rectangle_container">
                <svg><use xlink:href="/system/templates/images/sprite.svg#add"></use></svg>
                <div class="ico_rectangle_text">Добавить раздел</div>
            </a>
        </div>
        <table class="admin_table dan_even_odd">
            <tr>
                <th style="width:50px">№</th>
                <th style="width:50px"></th>
                <th>Раздел</th>
            </tr>
            {sections_tr_html}
        </table>   
    '''