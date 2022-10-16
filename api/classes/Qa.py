class Qa:
    def __init__(self, SITE):
        self.db = SITE.db


    # Добавляем новый вопрос
    def insert(self, data):
        sql = "INSERT INTO qa SET project_id = %s, visitor_id = %s, question = %s, item_id = %s, date = NOW()"
        self.db.execute(sql, (data['project_id'], data['visitor_id'], data['question'], data['item_id']))
        return self.db.lastrowid


    def getAll(self, limit=10):
        sql =   "SELECT q.project_id, q.question, q.item_id, q.date, i.name, p.name project_name FROM qa q "
        sql +=  "JOIN projects p ON p.id = q.project_id "
        sql +=  "JOIN items i ON i.id = q.item_id "
        sql +=  "ORDER BY q.date DESC LIMIT %s"
        self.db.execute(sql, (limit))
        return self.db.fetchall()


    def getByProjectId(self, project_id, limit=10):
        sql =   "SELECT q.question, q.item_id, q.date, i.name FROM qa q "
        sql +=  "JOIN items i ON i.id = q.item_id "
        sql +=  "WHERE q.project_id = %s ORDER BY q.date DESC LIMIT %s"
        self.db.execute(sql, (project_id, limit))
        return self.db.fetchall()


    # Удаляем старые записи (старше 90 дней - по умолчанию)
    def deleteOld(self, d, days=90):
        sql = "DELETE FROM qa WHERE date < SUBDATE(NOW(), INTERVAL %s DAY)"
        self.db.execute(sql, (days))