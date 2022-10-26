import json

class Items:
    def __init__(self, SITE):
        self.db = SITE.db


    # Возвращает item по id
    def getItem(self, id):
        sql = 'SELECT id, project_id, section_id, name, questions, content, status, ordering FROM items WHERE id = %s'
        self.db.execute(sql, (id))
        arr = self.db.fetchone()
        arr['content'] = json.loads(arr['content'])
        return arr


    # Возвращает список items по section_id
    def getListByProjectId(self, project_id, status=False):
        status = 'AND status = ' + str(int(status)) if status else ''  # int - для защиты от внесения строки

        sql = f'SELECT id, name, questions, status, ordering FROM items WHERE project_id = %s {status} ORDER BY ordering'
        self.db.execute(sql, (project_id))
        return self.db.fetchall()


    # Возвращает список items по section_id
    def getListBySectionId(self, section_id, sql_select=False, status=False):
        if not sql_select:
            sql_select = 'id, idx, section_id, name, content, date, status, ordering'
        status = 'AND status = ' + str(int(status)) if status else ''  # int - для защиты от внесения строки

        sql = f'SELECT {sql_select} ordering FROM items WHERE section_id = %s {status} ORDER BY ordering'
        self.db.execute(sql, (section_id))
        return self.db.fetchall()


    # Возвращает item по idx  
    def getItemByIdx(self, project_id, idx):
        sql = 'SELECT id, project_id, name, questions, content, status, ordering FROM items WHERE idx = %s and status = 1'
        self.db.execute(sql, (idx))
        arr = self.db.fetchone()
        arr['content'] = json.loads(arr['content'])
        return arr


    # Возвращает максимальное значение 'ordering'
    def getMaxOrdering(self, project_id):
        sql = "SELECT MAX(ordering) max_ordering FROM items WHERE project_id=%s"
        self.db.execute(sql, (project_id))
        mo = self.db.fetchone()
        return 0 if mo['max_ordering'] is None else mo['max_ordering']


    # Добавляет тему в БД
    def insert(self, data):
        sql = '''
        INSERT INTO items SET
            idx = 0,
            project_id = %s,
            section_id = %s,
            name = %s,
            content = %s,
            questions = %s,
            date = NOW(),
            mode = 0,
            status = %s,
            ordering = %s
        '''
        self.db.execute(sql, (
            data['project_id'], 
            data['section_id'], 
            data['name'], 
            json.dumps(data['content']), 
            data['questions'], 
            data['status'], 
            data['ordering']
        ))

        sql = "SELECT MAX(id) max_id FROM items WHERE project_id = %s"
        self.db.execute(sql, (data['project_id']))
        return self.db.fetchone()['max_id']


    # Обновляет тему в БД
    def update(self, data):
        sql = '''
        UPDATE items SET
        section_id = %s,
        name = %s,
        content = %s,
        questions = %s,
        date = NOW(),
        status = %s,
        ordering = %s
        WHERE id = %s
        '''
        self.db.execute(sql, (
            data['section_id'], 
            data['name'], 
            json.dumps(data['content']), 
            data['questions'], 
            data['status'], 
            data['ordering'], 
            data['id']
        ))


    # Обновляет индексы
    def updateIdx(self, id, idx):
        sql = "UPDATE items SET idx = %s WHERE id = %s"
        self.db.execute(sql, (idx, id))


    # Обновляет статус
    def setStatus(self, id, status):
        sql = "UPDATE items SET status = %s WHERE id = %s"
        self.db.execute(sql, (status, id))


    # Устанавливает порядок следования
    def setOrdering(self, id, act):
        item_arr = self.getItem(id)

        sql = 'SELECT id, ordering FROM items WHERE project_id = %s ORDER BY ordering'
        self.db.execute(sql, (item_arr['project_id']))
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
            sql = "UPDATE items SET ordering = %s WHERE section_id = %s AND id = %s"
            self.db.execute(sql, (i+1, item_arr['section_id'], arr[i]))

        return item_arr['section_id']


    # Удаляет тему
    def delete(self, id):
        sql = "DELETE FROM items WHERE id=%s"
        self.db.execute(sql, (id))
        return self.db.fetchone()