from Search import Search

def update(SITE):
    SITE.debug('PATH: /system/components/search/sites/update.py')
    data = {}
    data['site'] = SITE.post['site']
    data['sitemap_url'] = SITE.post['sitemap_url']
    data['count_month'] = int(SITE.post['count_month'])
    data['count_total'] = int(SITE.post['count_total'])
    data['ip'] = SITE.post['ip']
    data['ordering'] = int(SITE.post['ordering'])
    data['status'] = 1 if 'status' in SITE.post else 0
    data['id'] = int(SITE.p[5])

    SEARCH = Search(SITE)
    SEARCH.sitesUpdate(data)

    return {'redirect': '/system/com/search/sites'}