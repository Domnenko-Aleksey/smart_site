from Items import Items

def ordering(SITE):
    SITE.debug('PATH: /system/items/ordering.py')

    act = SITE.p[2]
    id = SITE.p[3]
    ITEMS = Items(SITE)
    project_id = ITEMS.setOrdering(id, act)
    
    return {'redirect': '/system/items/'+str(project_id)}