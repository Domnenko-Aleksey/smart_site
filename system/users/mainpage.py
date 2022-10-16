from Users import Users

def mainpage(SITE):
    SITE.debug('PATH: /system/users/mainpage.py')

    SITE.addHeadFile('/system/lib/DAN/DAN.css')
    SITE.addHeadFile('/system/lib/DAN/DAN.js')
    SITE.addHeadFile('/system/lib/DAN/contextmenu/contextmenu.css')
    SITE.addHeadFile('/system/lib/DAN/contextmenu/contextmenu.js')
    SITE.addHeadFile('/system/templates/css/list.css')
    SITE.addHeadFile('/system/templates/js/users_list.js')
    
    USER = Users(SITE)
    users = USER.getUsersList()

    tr_html = ''   
    for u in users:
        tr_class = 'class="unpub"' if u['status'] == 0 else ''
        tr_html += f'''
         <tr {tr_class}>
            <td style="width:50px">{u['id']}</td>
            <td style="width:50px">
                <svg class="dan_contextmenu_ico contextmenu_menu" title="Действия" data-id="{u['id']}">
                    <use xlink:href="/system/templates/images/sprite.svg#menu"></use>
                </svg>
            </td>
            <td><a href="/system/users/edit/{u['id']}">{u['name']}</a></td>
            <td style="width:150px">{u['email']}</td>
            <td style="width:150px">{u['date_reg']}</td>
            <td style="width:150px">{u['date_last']}</td>
            <td style="width:100px">{u['status']}</td>
        </tr>
        '''



    SITE.content = f'''
        <div class="flex_row_start">
            <a href="/system/users/add" target="blank" class="ico_rectangle_container">
                <svg><use xlink:href="/system/templates/images/sprite.svg#add"></use></svg>
                <div class="ico_rectangle_text">Добавить пользователя</div>
            </a>
        </div>
        <h1>Пользователи</h1>
        <table class="admin_table dan_even_odd">
            <tr>
                <th style="width:50px">№</th>
                <th style="width:50px"></th>
                <th>Имя.</th>
                <th style="width:150px">Email</th>
                <th style="width:150px">Последний визит</th>
                <th style="width:150px">Регистрация</th>
                <th style="width:100px">Статус</th>
            </tr>
            {tr_html}
        </table>
    '''