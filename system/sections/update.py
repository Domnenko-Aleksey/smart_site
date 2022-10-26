from Sections import Sections

def update(SITE):
    SITE.debug('PATH: /system/sections/update.py')

    data = {}
    project_id = SITE.post['project_id']
    data['name'] = SITE.post['name'].replace('"', '&quot;')
    data['ordering'] = SITE.post['ordering']
   
    data['id'] = SITE.p[3]
    SECTIONS = Sections(SITE)
    SECTIONS.update(data)
    return {'redirect': '/system/projects/project/' + project_id}
