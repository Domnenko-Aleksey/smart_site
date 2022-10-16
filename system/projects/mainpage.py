from Projects import Projects

def mainpage(SITE):
    SITE.debug('PATH: /system/projects/mainpage.py')

    SITE.addHeadFile('/lib/DAN/DAN.css')
    SITE.addHeadFile('/lib/DAN/DAN.js')
    SITE.addHeadFile('/lib/DAN/contextmenu/contextmenu.css')
    SITE.addHeadFile('/lib/DAN/contextmenu/contextmenu.js')
    SITE.addHeadFile('/system/templates/css/list.css')
    SITE.addHeadFile('/system/templates/js/projects_list.js')
    
    PROJECT = Projects(SITE)
    projects = PROJECT.getProjectsList(users=True)

    tr_html = ''   
    for p in projects:
        tr_class = 'class="unpub"' if p['status'] == 0 else ''
        user_class = 'class="unpub"' if p['user_status'] == 0 else ''
        tr_html += f'''
         <tr {tr_class}>
            <td>{p['id']}</td>
            <td>
                <svg class="dan_contextmenu_ico contextmenu_menu" title="Действия" data-id="{p['id']}">
                    <use xlink:href="/system/templates/images/sprite.svg#menu"></use>
                </svg>
            </td>
            <td><a href="/system/projects/project/{p['id']}">{p['name']}</a></td>
            <td><a target="_blank" href="https://{p['domain']}">{p['domain']}</a></td>
            <td><a href="/system/users/edit/{p['user_id']}" {user_class}>{p['user_name']} ({p['user_email']})</a></td>
            <td>{p['date']}</td>
            <td>{p['status']}</td>
        </tr>
        '''

    SITE.content = f'''
        <h1>Проекты</h1>
        <table class="admin_table dan_even_odd">
            <tr>
                <th style="width:50px">№</th>
                <th style="width:50px"></th>
                <th>Проект</th>
                <th style="width:250px">Домен</th>
                <th style="width:250px">Пользователь</th>
                <th style="width:150px">Дата изм.</th>
                <th style="width:100px">Статус</th>
            </tr>
            {tr_html}
        </table>
    '''