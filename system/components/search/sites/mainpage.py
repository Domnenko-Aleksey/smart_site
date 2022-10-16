import json
from Search import Search

def mainpage(SITE):
    SITE.debug('PATH: /system/components/search/sites/mainpage.py')

    SITE.addHeadFile('/system/lib/DAN/DAN.css')
    SITE.addHeadFile('/system/lib/DAN/DAN.js')
    SITE.addHeadFile('/system/lib/DAN/contextmenu/contextmenu.css')
    SITE.addHeadFile('/system/lib/DAN/contextmenu/contextmenu.js')
    SITE.addHeadFile('/system/templates/css/list.css')
    SITE.addHeadFile('/system/templates/components/search/templates/js/sites_mainpage.js')
    SITE.addHeadFile('/system/templates/components/search/templates/css/mainpage.css')

    SEARCH = Search(SITE)
    sites = SEARCH.sitesGetItemList()

    tr_html = ''   
    for site in sites:
        tr_class = 'class="unpub"' if site['status'] == 0 else ''
        tr_html += f'''
         <tr {tr_class}>
            <td>{site['id']}</td>
            <td>
                <svg class="dan_contextmenu_ico contextmenu_menu" title="Действия" data-id="{site['id']}">
                    <use xlink:href="/system/templates/images/sprite.svg#menu"></use>
                </svg>
            </td>
            <td><a href="/system/com/search/pages/list/{site['id']}">{site['site']}</a></td>
            <td>{site['count_month']}</td>
            <td>{site['count_total']}</td>
            <td>{site['date_last']}</td>
        </tr>
        '''

    SITE.content = f'''
        <div class="flex_row_start">
            <a href="/system/com/search/sites/add" target="blank" class="ico_rectangle_container">
                <svg><use xlink:href="/system/templates/images/sprite.svg#add"></use></svg>
                <div class="ico_rectangle_text">Добавить сайт</div>
            </a>
        </div>
        <h1>Поиск для сайтов</h1>
        <table class="admin_table dan_even_odd">
            <tr>
                <th style="width:50px">id</th>
                <th style="width:50px"></th>
                <th>Сайт</th>
                <th style="width:100px">За месяц</th>
                <th style="width:100px">Сумма</th>
                <th style="width:100px">Дата</th>
            </tr>
            {tr_html}
        </table>
    '''