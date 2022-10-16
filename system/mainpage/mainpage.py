import json
from Qa import Qa
from Favorites import Favorites

def mainpage(SITE):
    # current_datetime = datetime.now()

    SITE.debug('/system/mainpage/mainpage.py')

    SITE.addHeadFile('/lib/DAN/DAN.css')
    SITE.addHeadFile('/lib/DAN/DAN.js')
    SITE.addHeadFile('/system/templates/css/mainpage.css')

    # Запросы и ответы
    QA = Qa(SITE)
    qa = QA.getAll()
    qa_html = ''
    for q in qa:
        qa_html += f'<div><b>{q["project_name"]}</b>, {q["date"]}, <i>{q["question"]}</i> => {q["name"]}</div>'

    # Избранное
    FAVORITES = Favorites(SITE)
    fav = FAVORITES.getFavorites()
    fav_html = ''
    for fv in fav:
        fav_arr = json.loads(fv['favorites'])
        fav_list = fav_arr.values()
        fav_str = '<br>'.join(fav_list)
        fav_html += f'<div><b>{fv["project_name"]}</b>, {fv["date_l"]}, <br>{fav_str}<br></div>'

    SITE.content = f'''
        <h1>Дашбоард</h1>
        <div class="dan_flex_row_start">
            <div class="mp_panel">
                <div class="mp_panel_title">Запросы</div>
                {qa_html}
            </div>
            <div class="mp_panel">
                <div class="mp_panel_title">Избранное</div>
                {fav_html}
            </div>
        </div>
    '''
