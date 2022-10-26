import json

class Items:
    def __init__(self, SITE):
        self.db_connect = SITE.db_connect
        self.db = SITE.db


    # Возвращает item по id
    def getItem(self, project_id, id):
        sql = 'SELECT id, project_id, name, questions, content, status, ordering FROM items WHERE project_id = %s AND id = %s AND status = 1'
        self.db.execute(sql, (project_id, id))
        arr = self.db.fetchone()
        arr['content'] = json.loads(arr['content'])
        return arr


    # Возвращает item по id
    def getItemList(self, project_id):
        sql = 'SELECT id, idx, project_id, name, content, date, status, ordering FROM items WHERE project_id = %s'
        self.db.execute(sql, (project_id))
        return self.db.fetchall()


    # Возвращает item по idx  
    def getItemByIdx(self, project_id, idx):
        sql = 'SELECT id, project_id, name, questions, content, status, ordering FROM items WHERE project_id = %s AND idx = %s AND status = 1'
        self.db.execute(sql, (project_id, idx))
        arr = self.db.fetchone()
        arr['content'] = json.loads(arr['content'])
        return arr