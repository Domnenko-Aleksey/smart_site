from Search import Search

def ordering(SITE):
    SITE.debug('PATH: /system/components/search/sites/ordering.py')

    act = SITE.p[4]
    id = SITE.p[5]
    SEARCH = Search(SITE)
    SEARCH.sitesSetOrdering(id, act)
    
    return {'redirect': '/system/com/search/sites'}