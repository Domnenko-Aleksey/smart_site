from Sections import Sections

def edit(SITE):
    SITE.debug('PATH: /system/sections/edit.py')

    SITE.addHeadFile('/lib/DAN/DAN.css')
    SITE.addHeadFile('/lib/DAN/DAN.js')
    SITE.addHeadFile('/system/templates/css/edit.css')

    SECTIONS = Sections(SITE)

    if SITE.p[2] == 'add':
        project_id = SITE.p[3]
        title = 'Добавить'
        act = 'insert/' + project_id
        section = {
            'name': '',
            'ordering': SECTIONS.getMaxOrdering(project_id) + 1
        }
    else:
        section_id = SITE.p[3]
        title = 'Редактировать'
        act = 'update/' + section_id
        section = SECTIONS.getSection(section_id)
        project_id = section['project_id']


    SITE.content = f'''
        <h1>{title} раздел</h1>
        <form method="post" action="/system/sections/{act}" enctype="multipart/form-data">
        <div class="dan_flex_row">
            <div class="tc_l">Наименование раздела</div>
            <div class="tc_r dan_flex_grow">
                <input class="dan_input w_400" name="name" type="text" required="" value="{section['name']}">
            </div>
        </div>
        <div class="dan_flex_row">
            <div class="tc_l">Порядок следования</div>
            <div class="tc_r dan_flex_grow">
                <input class="dan_input" name="ordering" type="number" required="" value="{section['ordering']}">
            </div>
        </div>
        <div class="dan_flex_row m_40_0">
            <div class="tc_l">
                <input class="dan_button_green" type="submit" name="submit" value="Сохранить">
            </div>
            <div class="tc_r">
                <a href="system/projects/project/{project_id}" class="dan_button_white">Отменить</a>
            </div>
        </div>
        <input name="project_id" type="hidden" value="{project_id}">
        </form>
    '''