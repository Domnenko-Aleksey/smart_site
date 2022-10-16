import socket
import json
from Search import Search


def edit(SITE):
    SITE.debug('PATH: /system/components/search/sites/edit.py')

    SITE.addHeadFile('/system/lib/DAN/DAN.css')
    SITE.addHeadFile('/system/lib/DAN/DAN.js')
    SITE.addHeadFile('/system/templates/css/edit.css')

    SEARCH = Search(SITE)

    if SITE.p[4] == 'add':
        ordering = SEARCH.sitesGetMaxOrdering() + 1
        title = 'Добавить'
        act = 'insert/'
        site = {
            'id': '',
            'site': '',
            'sitemap_url': '',
            'ip': '',
            'count_month': 0,
            'count_total': 0,
            'ordering' : ordering,
        }
        ip_required = ''
        status_checked = ''
    else:
        id = SITE.p[5]
        title = 'Редактировать'
        act = 'update/' + id
        site = SEARCH.sitesGetItem(id)
        if site['ip'] == '':
            site['ip'] = socket.gethostbyname(site['site'])

        ip_required = 'required=""'
        status_checked = 'checked=""' if site['status'] == 1 else ''


  
    SITE.content = f'''
        <h1>{title} сайт</h1>
        <form method="post" action="/system/com/search/sites/{act}" enctype="multipart/form-data">
        <div class="dan_flex_row">
            <div class="tc_l">Сайт</div>
            <div class="tc_r dan_flex_grow">
                <input class="dan_input w_400" name="site" type="text" required="" value="{site['site']}" title="Заполните название сайта">
            </div>
        </div>
        <div class="dan_flex_row">
            <div class="tc_l">Ip адрес</div>
            <div class="tc_r dan_flex_grow">
                <input class="dan_input w_400" name="ip" type="text" {ip_required} value="{site['ip']}">
            </div>
        </div>
        <div class="dan_flex_row">
            <div class="tc_l">Sitemap URL</div>
            <div class="tc_r dan_flex_grow">
                <input class="dan_input w_400" name="sitemap_url" type="text" required="" value="{site['sitemap_url']}" title="URL карты сайта">
            </div>
        </div>
        <div class="dan_flex_row">
            <div class="tc_l">Месячный счётчик</div>
            <div class="tc_r dan_flex_grow">
                <input class="dan_input" name="count_month" type="number" value="{site['count_month']}">
            </div>
        </div>
        <div class="dan_flex_row">
            <div class="tc_l">Итоговый счётчик</div>
            <div class="tc_r dan_flex_grow">
                <input class="dan_input" name="count_total" type="number" value="{site['count_total']}">
            </div>
        </div>
        <div class="dan_flex_row">
            <div class="tc_l">Порядок следования</div>
            <div class="tc_r dan_flex_grow">
                <input class="dan_input" name="ordering" type="number" value="{site['ordering']}">
            </div>
        </div>
        <div class="dan_flex_row">
            <div class="tc_l">Статус</div>
            <div class="tc_r dan_flex_grow">
                <input id="mp_item_status" class="dan_input" name="status" type="checkbox" value="1" {status_checked}>
                <label for="mp_item_status"></label>
            </div>
        </div>
        <div class="dan_flex_row da_p_40_0">
            <div class="tc_l">
                <input id="da_submit" class="dan_button_green" type="submit" name="submit" value="Сохранить">
            </div>
            <div class="tc_r">
                <a href="/system/com/search" class="dan_button_white">Отменить</a>
            </div>
        </div>
        </form>
    '''