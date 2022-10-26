from Sections import Sections

def ordering(SITE):
    SITE.debug('PATH: /system/sections/ordering.py')

    act = SITE.p[2]
    id = SITE.p[3]
    SECTIONS = Sections(SITE)
    project_id = SECTIONS.setOrdering(id, act)
    
    return {'redirect': '/system/projects/project/'+str(project_id)}