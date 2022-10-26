import json

class Sections:
    def __init__(self, SITE):
        self.db = SITE.db


    # Возвращает 'section' по 'id'
    def getSections(self, project_id, items_count=False):
        if not items_count:
            sql = 'SELECT id, project_id, name, ordering FROM sections WHERE project_id = %s ORDER BY ordering'
        else:
            sql =   'SELECT s.id, s.project_id, s.name, s.ordering, COUNT(i.id) items_count '
            sql +=  'FROM sections s '
            sql +=  'LEFT OUTER JOIN items i '
            sql +=  'ON i.section_id = s.id '
            sql +=  'WHERE s.project_id = %s '
            sql +=  'GROUP BY s.id '
            sql +=  'ORDER BY s.ordering'
        self.db.execute(sql, (project_id))
        return self.db.fetchall()


    # Возвращает 'section' по 'id'
    def getSection(self, id):
        sql = 'SELECT id, project_id, name, ordering FROM sections WHERE id = %s'
        self.db.execute(sql, (id))
        return self.db.fetchone()


    # Возвращает список 'sections' по 'project_id'
    def getItemList(self, project_id):
        sql = 'SELECT * FROM sections WHERE project_id = %s ORDER BY ordering'
        self.db.execute(sql, (project_id))
        return self.db.fetchall()


    # Возвращает максимальное значение 'ordering'
    def getMaxOrdering(self, project_id):
        sql = "SELECT MAX(ordering) max_ordering FROM sections WHERE project_id=%s"
        self.db.execute(sql, (project_id))
        mo = self.db.fetchone()
        return 0 if mo['max_ordering'] is None else mo['max_ordering']


    # Добавляет раздел в БД
    def insert(self, data):
        sql = 'INSERT INTO sections SET project_id = %s, name = %s, ordering = %s'
        self.db.execute(sql, (data['project_id'], data['name'], data['ordering']))

        sql = "SELECT MAX(id) max_id FROM sections WHERE project_id = %s"
        self.db.execute(sql, (data['project_id']))
        return self.db.fetchone()['max_id']


    # Обновляет раздел в БД
    def update(self, data):
        sql = '''
        UPDATE sections SET
        name = %s,
        ordering = %s
        WHERE id = %s
        '''
        self.db.execute(sql, (data['name'], data['ordering'], data['id']))


    # Устанавливает порядок следования
    def setOrdering(self, id, act):
        section_arr = self.getSection(id)

        sql = 'SELECT id, ordering FROM sections WHERE project_id = %s ORDER BY ordering'
        self.db.execute(sql, (section_arr['project_id']))
        sections = self.db.fetchall()

        ordering = 0
        for i, item in enumerate(sections):
            if int(item['id']) == int(id):
                ordering = i

        arr = {}
        if act == 'up':
            if ordering == 0:
                return section_arr['project_id']
            prev_id = sections[ordering-1]['id']
            current_id = sections[ordering]['id']
            arr[ordering - 1] = current_id
            arr[ordering] = prev_id
        else:
            if (ordering >= len(sections) - 1):
                return section_arr['project_id']
            next_id = sections[ordering+1]['id']
            current_id = sections[ordering]['id']
            arr[ordering + 1] = current_id
            arr[ordering] = next_id

        for i in arr:
            sql = "UPDATE sections SET ordering = %s WHERE project_id = %s AND id = %s"
            self.db.execute(sql, (i+1, section_arr['project_id'], arr[i]))
        return section_arr['project_id']


    # Удаляет тему
    def delete(self, id):
        sql = "DELETE FROM sections WHERE id=%s"
        self.db.execute(sql, (id))
        return self.db.fetchone()