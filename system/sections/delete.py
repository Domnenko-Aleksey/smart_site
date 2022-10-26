from Sections import Sections

def delete(SITE):
    SITE.debug('PATH: /system/sections/delete.py')

    id = SITE.p[3]
    SECTIONS = Sections(SITE)
    section = SECTIONS.getSection(id)
    project_id = section['project_id']
    SECTIONS.delete(id)

    return {'redirect': '/system/projects/project/'+str(project_id)}