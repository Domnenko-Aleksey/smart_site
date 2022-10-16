class Search:
    def __init__(self, SITE):
        self.db = SITE.db


    # Возвращает список id сайтов для поиска
    def getSitesList(self):
        sql = 'SELECT id FROM com_search_site WHERE status=1'
        self.db.execute(sql)
        return self.db.fetchall()        


    # Возвращает список из [['id', 'vector']] проекта
    def getPagesList(self, site_id):
        site_id = int(site_id)
        sql = f'SELECT id, vector FROM com_search_pages_{site_id}'
        self.db.execute(sql)
        return self.db.fetchall()
 

    # Возвращает список страниц по списку id
    def getPage(self, site_id, id):
        site_id = int(site_id)
        sql = f'SELECT id, url, title, description, image, price FROM com_search_pages_{site_id} WHERE id = %s'
        self.db.execute(sql, (id))
        return self.db.fetchone()