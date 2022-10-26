from aiohttp import web
from projects import mainpage
from projects import project
from projects import edit
from projects import insert
from projects import update
from projects import status
from projects import ordering
from projects import delete
from projects import get_pandas_ajax
from projects import get_topic_list_ajax
from projects import get_vectors_ajax
from projects import create_model_ajax
from projects import check_bert_ajax
from projects import fit_model_ajax
from projects import init_model_ajax
from projects import load_api_model_ajax


def router(SITE):
    SITE.debug('PATH: /system/projects/projects.py (router)')

    # Вызов функций по ключу
    functions = {
        '': mainpage.mainpage,
        'project': project.project,
        'add': edit.edit,
        'edit': edit.edit,
        'insert': insert.insert,
        'update': update.update,
        'pub': status.status,
        'unpub': status.status,
        'up': ordering.ordering,
        'down': ordering.ordering,
        'delete': delete.delete,
        'get_pandas_ajax': get_pandas_ajax.get_pandas_ajax,
        'get_topic_list_ajax': get_topic_list_ajax.get_topic_list_ajax,
        'get_vectors_ajax': get_vectors_ajax.get_vectors_ajax,
        'create_model_ajax': create_model_ajax.create_model_ajax,
        'check_bert_ajax': check_bert_ajax.check_bert_ajax,
        'fit_model_ajax': fit_model_ajax.fit_model_ajax,
        'init_model_ajax': init_model_ajax.init_model_ajax,
        'load_api_model_ajax': load_api_model_ajax.load_api_model_ajax,
    }

    if (SITE.p[2] not in functions):
        raise web.HTTPNotFound()

    # Вызов функции
    return functions[SITE.p[2]](SITE)
