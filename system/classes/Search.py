import numpy as np
import json
import pickle


class Search:
    def __init__(self, SITE):
        self.db = SITE.db
        self.sitemap_xml = False


    # Возвращает список сайтов
    def sitesGetItemList(self):
        sql = 'SELECT id, site, date_last, count_month, count_total, status FROM com_search_site ORDER BY ordering'
        self.db.execute(sql)
        return self.db.fetchall()

    
    # Возвращает сайт по id
    def sitesGetItem(self, id):
        sql = "SELECT id, site, sitemap_url, ip, count_month, count_total, ordering, status FROM com_search_site WHERE id=%s"
        self.db.execute(sql, (id))
        return self.db.fetchone()


    
    # Возвращает максимальное значение 'ordering'
    def sitesGetMaxOrdering(self):
        sql = "SELECT MAX(ordering) max_ordering FROM com_search_site"
        self.db.execute(sql)
        mo = self.db.fetchone()
        return 0 if mo['max_ordering'] is None else mo['max_ordering']


    # Добавляет сайт в БД
    def sitesInsert(self, data):
        sql = '''
        INSERT INTO com_search_site SET
            site = %s,
            sitemap_url = %s,
            ip = %s,
            date_reg = NOW(),
            date_last = NOW(),
            count_month = %s,
            count_total = %s,
            ordering = %s,
            status = %s
        '''
        self.db.execute(sql, (
            data['site'], 
            data['sitemap_url'], 
            data['ip'],
            data['count_month'], 
            data['count_total'], 
            data['ordering'], 
            data['status']
        ))
        return self.db.lastrowid


    # Обновляет сайт в БД
    def sitesUpdate(self, data):
        sql = '''
        UPDATE com_search_site SET
            site = %s,
            sitemap_url = %s,
            ip = %s,
            count_month = %s,
            count_total = %s,
            ordering = %s,
            status = %s
            WHERE id = %s
        '''
        self.db.execute(sql, (
            data['site'], 
            data['sitemap_url'],
            data['ip'], 
            data['count_month'], 
            data['count_total'],
            data['ordering'], 
            data['status'],
            data['id']
        ))


    # Обновляет статус
    def sitesSetStatus(self, id, status):
        sql = "UPDATE com_search_site SET status = %s WHERE id = %s"
        self.db.execute(sql, (status, id))


    # Устанавливает порядок следования
    def sitesSetOrdering(self, id, act):
        item_arr = self.sitesGetItem(id)

        sql = 'SELECT id, ordering FROM com_search_site ORDER BY ordering'
        self.db.execute(sql)
        items = self.db.fetchall()

        ordering = 0
        for i, item in enumerate(items):
            if int(item['id']) == int(id):
                ordering = i

        arr = {}
        if act == 'up':
            if ordering == 0:
                return
            prev_id = items[ordering-1]['id']
            current_id = items[ordering]['id']
            arr[ordering - 1] = current_id
            arr[ordering] = prev_id
        else:
            if (ordering >= len(items) - 1):
                return
            next_id = items[ordering+1]['id']
            current_id = items[ordering]['id']
            arr[ordering + 1] = current_id
            arr[ordering] = next_id

        for i in arr:
            sql = "UPDATE com_search_site SET ordering = %s WHERE id = %s"
            self.db.execute(sql, (i+1, arr[i]))


    # Удаляет сайт
    def sitesDelete(self, id):
        sql = "DELETE FROM com_search_site WHERE id=%s"
        self.db.execute(sql, (id))
        return self.db.fetchone()


    # ======= СТРАНИЦЫ =======
    # Создаёт отдельную таблицу для отдельного сайта
    def pagesCreateTable(self, site_id):
        sql = f'''CREATE TABLE `com_search_pages_{site_id}` (
            `id` int UNSIGNED NOT NULL,
            `url` varchar(255) NOT NULL,
            `vector` blob NOT NULL,
            `title` varchar(255) NOT NULL,
            `description` text NOT NULL,
            `image` varchar(255) NOT NULL,
            `price` varchar(32) NOT NULL,
            `date_create` date NOT NULL,
            `date_update` date NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
        '''
        self.db.execute(sql)

        sql = f'ALTER TABLE `com_search_pages_{site_id}` ADD PRIMARY KEY (`id`), ADD KEY `url` (`url`)'
        self.db.execute(sql)

        sql = f'ALTER TABLE `com_search_pages_{site_id}` MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT'
        self.db.execute(sql)


    # Удаляет таблицу
    def pagesDeleteTable(self, site_id):
        sql = f'DROP TABLE com_search_pages_{site_id}'
        self.db.execute(sql)


    # Возвращает список страниц сайта
    def pagesGetItemList(self, site_id):
        sql = f"SELECT id, url, title, image, price, date_update FROM com_search_pages_{site_id} LIMIT 100"
        self.db.execute(sql)
        return self.db.fetchall()


    # Устанавливает (insert | update) данные страницы сайта
    def pagesSetData(self, data):
        # Ищем данную странцу в БД
        sql = f"SELECT id FROM com_search_pages_{data['site_id']} WHERE url=%s"
        self.db.execute(sql, (data['url']))
        page = self.db.fetchone()

        if not page:
            self.pagesInsertData(data)
            return('insert')
        else:
            self.pagesUpdateData(data)
            return('update')


    # Добавляем данные страницы в Базу данных
    def pagesInsertData(self, data):
        sql = f'''
        INSERT INTO com_search_pages_{data['site_id']} SET
            url = %s,
            vector = %s,
            title = %s,
            description = %s,
            image = %s,
            price = %s,
            date_create = NOW(),
            date_update = NOW()
        '''

        self.db.execute(sql, (
            data['url'],
            np.array(data['vector']).tobytes(),
            data['title'],
            data['description'],
            data['image'],
            data['price'],
        ))


    # Обновляем данные страницы
    def pagesUpdateData(self, data):
        sql = f'''
        UPDATE com_search_pages_{data["site_id"]} SET
            url = %s,
            vector = %s,
            title = %s,
            description = %s,
            image = %s,
            price = %s,
            date_update = NOW()
        WHERE id = %s
        '''
        self.db.execute(sql, (
            data['url'], 
            np.array(data['vector']).tobytes(),
            data['title'],
            data['description'], 
            data['image'], 
            data['price'],
            data['site_id']
        ))    