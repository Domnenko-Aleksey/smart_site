import json
from Search import Search

def mainpage(SITE):
    SITE.debug('PATH: /system/components/search/pages/mainpage.py')

    SITE.addHeadFile('/system/lib/DAN/DAN.css')
    SITE.addHeadFile('/system/lib/DAN/DAN.js')
    SITE.addHeadFile('/system/lib/DAN/contextmenu/contextmenu.css')
    SITE.addHeadFile('/system/lib/DAN/contextmenu/contextmenu.js')
    SITE.addHeadFile('/system/templates/css/list.css')
    SITE.addHeadFile('/system/templates/components/search/templates/js/pages_mainpage.js')
    SITE.addHeadFile('/system/templates/components/search/templates/css/mainpage.css')

    SEARCH = Search(SITE)
    site = SEARCH.sitesGetItem(SITE.p[5])
    pages = SEARCH.pagesGetItemList(1)

    tr_html = ''
    for page in pages:
        image = '<img style="width:80%" src="' + page['image'] + '">' if page['image'] != '' else ''
        tr_html += f'''
         <tr>
            <td>{page['id']}</td>
            <td>
                <svg class="dan_contextmenu_ico contextmenu_menu" title="Действия" data-id="{page['id']}">
                    <use xlink:href="/system/templates/images/sprite.svg#menu"></use>
                </svg>
            </td>
            <td>{image}</td>
            <td>{page['title']}</td>
            <td><a target="_blank" href="{page['url']}">{page['url']}</a></td>
            <td>{page['price']}</td>
            <td>{page['date_update']}</td>
        </tr>
        '''

    SITE.content = f'''
        <h1>{site['site']}</h1>
        <table class="admin_table dan_even_odd">
            <tr>
                <th style="width:50px">id</th>
                <th style="width:50px"></th>
                <th style="width:80px"></th>
                <th>Страница</th>
                <th style="width:200px">URL</th>
                <th style="width:100px">Цена</th>
                <th style="width:100px">Дата</th>
            </tr>
            {tr_html}
        </table>
    '''