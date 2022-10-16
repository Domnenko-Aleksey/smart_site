import json
from Items import Items
from Projects import Projects

def mainpage(SITE):
    SITE.debug('PATH: /system/items/mainpage.py')

    SITE.addHeadFile('/system/lib/DAN/DAN.css')
    SITE.addHeadFile('/system/lib/DAN/DAN.js')
    SITE.addHeadFile('/system/lib/DAN/contextmenu/contextmenu.css')
    SITE.addHeadFile('/system/lib/DAN/contextmenu/contextmenu.js')
    SITE.addHeadFile('/system/templates/css/list.css')
    SITE.addHeadFile('/system/templates/js/items_list.js')

    project_id=SITE.p[2]

    PROJECT = Projects(SITE)
    projects = PROJECT.getProject(project_id)

    ITEM = Items(SITE)
    items = ITEM.getItemList(project_id)

    tr_html = ''   
    for item in items:
        item['content'] = json.loads(item['content'])
        content = '<span class="content_minus">-</span>' if item['content'] == '' else '<span class="content_plus">+</span>'
        tr_class = 'class="unpub"' if item['status'] == 0 else ''
        tr_html += f'''
         <tr {tr_class}>
            <td>{item['id']}</td>
            <td>{item['idx']}</td>
            <td>
                <svg class="dan_contextmenu_ico contextmenu_menu" title="Действия" data-id="{item['id']}">
                    <use xlink:href="/system/templates/images/sprite.svg#menu"></use>
                </svg>
            </td>
            <td><a href="/system/items/edit/{item['id']}">{item['name']}</a></td>
            <td></td>
            <td>{content}</td>
            <td>{item['date']}</td>
            <td>{item['status']}</td>
        </tr>
        '''

    SITE.content = f'''
        <div class="flex_row_start">
            <a href="/system/items/add/{project_id}" target="blank" class="ico_rectangle_container">
                <svg><use xlink:href="/system/templates/images/sprite.svg#add"></use></svg>
                <div class="ico_rectangle_text">Добавить тему</div>
            </a>
        </div>
        <h1>Темы проекта <b>"{projects['name']}"</b></h1>
        <table class="admin_table dan_even_odd">
            <tr>
                <th style="width:50px">№</th>
                <th style="width:50px">CLS</th>
                <th style="width:50px"></th>
                <th>Тема</th>
                <th style="width:100px">Вопросов</th>
                <th style="width:100px">Контент</th>
                <th style="width:150px">Дата изм.</th>
                <th style="width:100px">Статус</th>
            </tr>
            {tr_html}
        </table>
    '''