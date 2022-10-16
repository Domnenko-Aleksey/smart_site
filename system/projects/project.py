from Projects import Projects
from Visitors import Visitors
from Favorites import Favorites
from Qa import Qa


def project(SITE):
    SITE.debug('PATH: /system/projects/project.py')

    SITE.addHeadFile('/lib/DAN/DAN.css')
    SITE.addHeadFile('/system/templates/css/project.css')

    project_id = int(SITE.p[3])
    
    PROJECT = Projects(SITE)
    project = PROJECT.getProject(project_id, True)

    # Вопрос - ответ
    QA = Qa(SITE)
    qa = QA.getByProjectId(project_id)
    qa_tr_html = ''
    if qa:
        for n, q in enumerate(qa):
            qa_tr_html += f'''<tr><td>{n}</td><td>{q['question']}</td><td>{q['name']}</td><td>{q['date']}</td></tr>'''


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
        <h3>Вопрос - ответ</h3>
        <table class="admin_table dan_even_odd">
            <tr>
                <th style="width:50px">№</th>
                <th>Вопрос</th>
                <th style="width:250px">Тема ответа</th>
                <th style="width:150px">Дата</th>
            </tr>
            {qa_tr_html}
        </table>   
    '''