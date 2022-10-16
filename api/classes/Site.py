import pymysql
import pymysql.cursors
import config


class Site:
    # Инициализация при запуске системы
    def __init__(self):
        self.salt = 'DAN_core_salt'  # Соль
        self.debug_on = False
        self.models = {}  # Словарь моделей {'project id': model}
        self.db_connect = False  # Соединение с базой данных, инициализируем ниже
        self.db = False  # con.cursor()
        self.mysql_connect()

    
    # Подключаем базу данных
    def mysql_connect(self):
        con = pymysql.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            db=config.db,
            charset='utf8mb4',
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        self.db_connect = con
        self.db = con.cursor()


    # Инициализация при открытии страниы
    def initial(self):
        self.file = False  # Полученый файл
        self.post = False  # объект post
        self.head = ''  # Материал выводимыей в внутри тега шаблона <head>
        self.tag_title = ''  # Тег title
        self.tag_description = ''  # Метатег descripton
        self.content = ''  # Основное содержимое
        self.modules = {}  # Словарь модулей
        self.headFile = []  # Файлы для вывода в шапке шаблона
        self.auth = 0  # Авторизация 0 => нет; 1 - 9 => администраторы; 10 - 100 => пользователи
        self.session = False
        if not self.db_connect.open:
            # Если соединение с mysql закрыто - открываем его
            self.mysql_connect()


    # Обработка запроса
    def procReq(self, request):
        self.request = request  #  # request aiohttp
        self.p = request.path[1:].split('/')  # Список элементов пути
        i = len(self.p)
        while i < 7:
            self.p.append('')
            i += 1


    # Добавляет файлы для вывода в шапке шаблона
    def addHeadFile(self, path):
        if path in self.headFile:
            return
        self.headFile.append(path)


    # Выводит '<script ...>, <link ...>' в шапке HTML документа
    def getHead(self):
        out = ''
        for file in self.headFile:
            file_list = file.split('.')
            if file_list[-1] == 'js':
                out += '<script src="' + file + '"></script>'
            if file_list[-1] == 'css':
                out += '<link rel="stylesheet" href="' + file + '" />'
        return out

    
    # Выводит текст отладки
    def debug(self, txt):
        if self.debug_on:
            print(txt)
