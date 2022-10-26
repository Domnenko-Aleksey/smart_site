import os
from Sections import Sections

def insert(SITE):
    SITE.debug('PATH: /system/sections/insert.py')

    project_id = SITE.p[3]
    data = {
        'project_id': project_id,
        'name': SITE.post['name'],
        'ordering': SITE.post['ordering']
    }

    SECTIONS = Sections(SITE)
    SECTIONS.insert(data)

    return {'redirect': '/system/projects/project/' + project_id}
