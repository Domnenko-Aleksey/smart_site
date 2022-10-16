class Visitors:
    def __init__(self, SITE):
        self.db = SITE.db


    # Получаем список всех посетителей
    def getVisitors(self, limit=10):
        sql = "SELECT id, data, date_l FROM visitors LIMIT " + str(limit)
        self.db.execute(sql)
        return self.db.fetchone()


    # Добавляем нового посетителя
    def insert(self, cid):
        sql = "INSERT INTO visitors SET cid = %s, data = '', date_c = NOW(), date_l = NOW()"
        self.db.execute(sql, (cid))
        return self.db.lastrowid


    # Проверяем посетителя. Если не найден - добавляем.
    def check(self, cid):
        sql = "SELECT id FROM visitors WHERE cid = %s LIMIT 1"
        self.db.execute(sql, (cid))
        v = self.db.fetchone()

        if not v:
            # Куки есть, а посетителя - нет -> добавляем посетителя
            visitor_id = self.insert(cid) 
        else:
            visitor_id = v['id']
            # Обновляем время посетителя
            sql = "UPDATE visitors SET date_l = NOW() WHERE cid = %s"
            self.db.execute(sql, (cid))
        
        return visitor_id


    # Получаем данные посетителя по кукам
    def getByCid(self, cid):
        sql = "SELECT id FROM visitors WHERE cid = %s"
        self.db.execute(sql, (cid))
        return self.db.fetchone()


    # Получаем данные посетителей проекта 
    '''
    def getByProjectId(self, project_id, limit=10):
        sql = "SELECT cid, date_c, date_l FROM visitors WHERE project_id = %s ORDER BY date_l DESC LIMIT %s"
        self.db.execute(sql, (project_id, limit))
        return self.db.fetchall()
    '''


    # Удаляем посетителя
    def delete(self):
        sql = "DELETE FROM visitors WHERE id=%s"
        self.db.execute(sql, (id))
