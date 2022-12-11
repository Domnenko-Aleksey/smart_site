import json

class Favorites:
    def __init__(self, SITE):
        self.db = SITE.db

    # Получаем избранное по 'cid'
    def getFavorites(self, limit=10):
        sql =   "SELECT f.id, f.project_id, f.favorites, f.date_l, p.name project_name FROM favorites f "
        sql +=  "JOIN projects p ON p.id = f.project_id "
        sql +=  "ORDER BY f.id DESC LIMIT %s"
        self.db.execute(sql, (limit))
        return self.db.fetchall()


    def getByProjectId(self, project_id, limit=10):
        sql =   "SELECT id, favorites, date_c, date_l FROM favorites f "
        sql +=  "WHERE project_id = %s ORDER BY date_l DESC LIMIT %s"
        self.db.execute(sql, (project_id, limit))
        return self.db.fetchall()


    # Получаем избранное по 'cid'
    def getFavoritesByProjectIdVisitorId(self, project_id, visitor_id):
        sql = "SELECT id, favorites FROM favorites WHERE project_id = %s AND visitor_id = %s LIMIT 1"
        self.db.execute(sql, (project_id, visitor_id))
        arr = self.db.fetchone()
        if arr and arr['favorites'] != '':
            arr['favorites'] = json.loads(arr['favorites'])
        return arr


    # Устанавливает новый список избранного
    def setFavorites(self, project_id, visitor_id, favorites):
        # Получаем избранное посетителя в БД
        fav = self.getFavoritesByProjectIdVisitorId(project_id, visitor_id)
        if not fav:
            # Добавляем избранное
            self.insert(project_id, visitor_id, favorites)
        else:
            if fav['favorites'] != '':
                # Обновляем избранное
                self.update(fav['id'], favorites)
            else:
                # Удаляем пустой список избранное
                self.delete(fav['id'])


    # Добавляем избранное
    def insert(self, project_id, visitor_id, favorites):
        if favorites != '':
            favorites = json.dumps(favorites)
        sql = "INSERT INTO favorites SET project_id = %s, visitor_id = %s, favorites = %s, date_c = NOW(), date_l = NOW()"
        self.db.execute(sql, (project_id, visitor_id, favorites))


    # Обновляем данные
    def update(self, id, favorites):
        if favorites != '':
            favorites = json.dumps(favorites)
        sql = "UPDATE favorites SET favorites = %s,  date_l = NOW() WHERE id = %s"
        self.db.execute(sql, (favorites, id))


    # Удаляем
    def delete(self, id):
        sql = "DELETE FROM favorites WHERE id = %s"
        self.db.execute(sql, (id))