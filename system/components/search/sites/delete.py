from Search import Search

def delete(SITE):
    SITE.debug('PATH: /system/components/search/sites/delete.py')
    SEARCH = Search(SITE)
    SEARCH.sitesDelete(SITE.p[5])
    SEARCH.pagesDeleteTable(SITE.p[5])
    return {'redirect': '/system/com/search/sites'}