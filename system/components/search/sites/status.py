from Search import Search

def status(SITE):
    SITE.debug('PATH: /system/components/search/sites/status.py')
    status = 1 if SITE.p[4] == 'pub' else 0
    id = SITE.p[5]
    SEARCH = Search(SITE)
    SEARCH.sitesSetStatus(id, status)
    
    return {'redirect': '/system/com/search/sites'}
