import uuid
import json

class Projects:
    def __init__(self, SITE):
        self.db_connect = SITE.db_connect
        self.db = SITE.db


    # Удаляет пользователя по id
    def delete(self, id):
        sql = "DELETE FROM projects WHERE id=%s"
        self.db.execute(sql, (id))
        return self.db.fetchone()


    # Возвращает проекты
    def getProjectsList(self, sql_select=False):
        sql_s = sql_select if sql_select else '*'
        sql = f"SELECT {sql_s} FROM projects WHERE status=1"   
        self.db.execute(sql)
        return self.db.fetchall()


    # Возвращает проект по id
    def getProject(self, id, user=False):
        if not user:
            sql = "SELECT * FROM projects WHERE id=%s"
        else:
            sql = '''
            SELECT p.id, p.hash, p.user_id, p.name, p.description, p.date, p.settings, p.status, u.id user_id, u.name user_name, u.email user_email, u.status user_status
            FROM projects p
            JOIN users u
            ON u.id = p.user_id
            WHERE p.id = %s
            ORDER BY p.ordering
            '''
        self.db.execute(sql, (id))
        return self.db.fetchone()


    # Возвращает проект по id
    def getProjectIdByDomain(self, domain):
        sql = "SELECT id FROM projects WHERE domain=%s LIMIT 1"
        self.db.execute(sql, (domain))
        return self.db.fetchone()['id']


    # Возвращает 'title' по домену
    def getIntroByDomain(self, domain):
        sql = "SELECT settings FROM projects WHERE domain=%s LIMIT 1"
        self.db.execute(sql, (domain))
        arr = self.db.fetchone()
        arr['settings'] = json.loads(arr['settings'])
        return {'intro_text': arr['settings']['intro_text'], 'intro_speech': arr['settings']['intro_speech']}


    # Возвращает id проекта по user id
    def getProjectByUserId(self, user_id):
        sql = "SELECT id FROM project WHERE user_id=%s"
        self.db.execute(sql, (user_id))
        return self.db.fetchone()
            
    
    # Максимальное значение 'ordering'
    def getMaxOrdering(self):
        self.db.execute("SELECT MAX(ordering) max_ordering FROM projects")
        mo = self.db.fetchone()
        return 0 if mo is None else mo['max_ordering']


    # Добавляет проект в БД
    def insert(self, data):
        sql = "INSERT INTO projects SET hash = %s, user_id = %s, site = '', name = %s, description = %s, settings = '', ordering = %s, status = %s"
        project_hash = uuid.uuid4().hex
        self.db.execute(sql, (project_hash, data['user_id'], data['name'], data['description'], data['ordering'], data['status']))
        self.db.execute("SELECT MAX(id) max_id FROM projects")
        return self.db.fetchone()['max_id']


    # Обновляет проект в БД
    def update(self, id, name, description, status):
        sql = "UPDATE projects SET name = %s, description = %s, status = %s WHERE id = %s"
        self.db.execute(sql, (name, description, status, id))


    # Обновляет статус
    def setStatus(self, id, status):
        sql = "UPDATE projects SET status = %s WHERE id = %s"
        self.db.execute(sql, (status, id))


    # Устанавливает порядок следования
    def setOrdering(self, id, act):
        projects = self.getProjectsList()
        ordering = 0
        for i, project in enumerate(projects):
            if int(project['id']) == int(id):
                ordering = i

        arr = {}

        if act == 'up':
            if ordering == 0:
                return
            prev_id = projects[ordering-1]['id']
            current_id = projects[ordering]['id']
            arr[ordering - 1] = current_id
            arr[ordering] = prev_id
        else:
            if (ordering >= len(projects) - 1):
                return
            next_id = projects[ordering+1]['id']
            current_id = projects[ordering]['id']
            arr[ordering + 1] = current_id
            arr[ordering] = next_id

        for i in arr:
            sql = "UPDATE projects SET ordering = %s WHERE id = %s"
            self.db.execute(sql, (i+1, arr[i]))
