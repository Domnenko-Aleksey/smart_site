import requests
import json
import uuid
import numpy as np
import api
import item_html
from Projects import Projects
from Visitors import Visitors
from Items import Items
from Qa import Qa


def get_speech_answer_ajax(SITE):
    SITE.debug('PATH: /api/get_speech_answer_ajax.py')
    SITE.debug('POST')
    SITE.debug(SITE.post)


    # --- Проверка входных полей ---
    if not 'domain' in SITE.post:
        answer = {'answer': 'success', 'message': 'No domain'}
        return json.dumps(answer)

    if not 'speech_text' in SITE.post:
        answer = {'answer': 'success', 'message': 'No speech text'}
        return json.dumps(answer)

    if not 'ss_cid' in SITE.post:
        answer = {'answer': 'success', 'message': 'No ss_cid'}
        return json.dumps(answer)


    # --- Получаем project_id ---
    PROJECTS = Projects(SITE)
    project_id = PROJECTS.getProjectIdByDomain(SITE.post['domain'])


    # --- Получаем BERT-вектор для текста: ---
    question = SITE.post['speech_text']
    param = {'text': question.lower()}
    bert_req = requests.post('http://127.0.0.1:9003/bert_api', data=param)
    if int(bert_req.status_code) != 200:
        return json.dumps({'answer': 'error', 'message': 'No answer of BERT'})
    vector = bert_req.json()['vector']
    vector = np.array(vector).reshape(1, 768)
    if SITE.debug_on:
        print('QUESTION:', question)
        print(f'DOMAIN: {SITE.post["domain"]}, PROJECT_ID: {project_id}')
        print(f'BERT: {vector.shape}')

    predict = SITE.models[project_id](vector)  # SITE.models[project_id] - модель проекта,
    idx = np.argmax(predict)
    SITE.debug(f'IDX: {idx}') 


    # --- Получение ответа ---
    ITEMS = Items(SITE)
    item = ITEMS.getItemByIdx(project_id, idx)


    # --- Получаем посетителя: ---
    VISITORS = Visitors(SITE)  
    if len(SITE.post['ss_cid']) != 32:
        # Устанавливаем новые куки
        ss_cid_new = uuid.uuid4().hex
        visitor_id = VISITORS.insert(ss_cid_new)  # Добавляем посетителя
        SITE.debug(f'НОВОЕ COOCKES: {ss_cid_new}')
    else:
        visitor_id = VISITORS.check(SITE.post['ss_cid'])  # Проверяем посетителя. Если не найден - добавляем
        ss_cid_new = ''


    # --- Вставляем данные вопрос - ответ в БД ---
    QA = Qa(SITE)
    d = {'project_id':project_id, 'visitor_id':visitor_id, 'question':question, 'item_id':item['id']}
    SITE.debug(f'QA INSERT: project_id: {project_id}, visitor_id: {visitor_id}, question: {question}, item_id: {item["id"]}')
    QA.insert(d)
    d = {'project_id':project_id, 'visitor_id':visitor_id, 'item_id':item['id']}
    QA.deleteOld(d)  # Удаляем старые вопросы (> 90 дней)
    SITE.debug(f'ITEM_ID: {item["id"]}, ITEM_NAME: {item["name"]}')


    # --- Item HTML ---
    answer_content = item_html.item_html(SITE, item)


    answer = {
        'answer': 'success', 
        'answer_synthesis': item['content']['synthesis'], 
        'answer_content': answer_content, 
        'ss_cid_new': ss_cid_new
    }
    return json.dumps(answer)
