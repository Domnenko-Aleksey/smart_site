from Items import Items

def status(SITE):
    SITE.debug('PATH: /system/items/status.py')
    status = 1 if SITE.p[2] == 'pub' else 0
    id = SITE.p[3]
    ITEMS = Items(SITE)
    ITEMS.setStatus(id, status)
    
    item = ITEMS.getItem(id)
    
    return {'redirect': '/system/items/'+str(item['section_id'])}
