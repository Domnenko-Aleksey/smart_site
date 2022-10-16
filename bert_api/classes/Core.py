import json

class Core:
    def __init__(self):
        self.db = False


    # Получаем список разрешённых ip адресов
    def get_allowed_ip(self):
        sql = 'SELECT ip FROM com_search_site WHERE status = 1'
        self.db.execute(sql)
        arr = self.db.fetchall()
        allowed_ip = []
        for a in arr:
            allowed_ip.append(a['ip'])
        return allowed_ip

    
    # Создаёт таблицу со страницами для сайта с указанным site_id
    def create_table_pages(self, site_id):
        sql = f'''CREATE TABLE com_search_pages_{str(site_id)} ( 
            `id` INT UNSIGNED NOT NULL AUTO_INCREMENT, 
            `url` VARCHAR(255) NOT NULL, 
            `vector` VARCHAR(768) NOT NULL, 
            `title` VARCHAR(255) NOT NULL, 
            `description` TEXT NOT NULL, 
            `image` VARCHAR(255) NOT NULL, 
            `price` INT NOT NULL, 
            `data_create` INT NOT NULL, 
            `data_update` INT NOT NULL, 
            PRIMARY KEY (`id`), 
            INDEX (`url`)) 
            ENGINE = InnoDB;
        '''