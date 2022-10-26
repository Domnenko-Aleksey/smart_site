import json
import os
from pathlib import Path
import shutil
import pandas as pd
from Items import Items


def get_pandas_ajax(SITE):
    SITE.debug('PATH: /system/items/get_pandas_ajax.py')

    project_id = SITE.post['id']
    
    ITEM = Items(SITE)
    items = ITEM.getListByProjectId(project_id, status=1)
    
    data_list = []
    for i, item in enumerate(items):
        ITEM.updateIdx(item['id'], i)
        item_questions = item['questions'].split(';')
        for q in item_questions:
            data_list.append([q, i])
            
    df = pd.DataFrame(data_list)
    df.columns = ['question', 'class']

    # Получаем пользователя и владельца группы 
    path = Path('files')
    owner = path.owner()
    group = path.group()

    path = 'files/projects/' + str(project_id)
    if not os.path.isdir(path):
        os.makedirs(path, mode=0o755, exist_ok=True)
        path_arr = path.split('/')
        p_cur = ''
        for p in path_arr:
            # Для вложенных директорий меняем пользователя и группу
            p_cur += p + '/'
            shutil.chown(p_cur, user=owner, group=group)
    
    file_path = path + '/data.csv'
    df.to_csv(file_path)

    shutil.chown(file_path, user=owner, group=group)

    site_path = '/system/files/projects/' + str(project_id) + '/data.csv'
    answer = {'answer': 'success', 'link': site_path}
    return {'ajax': json.dumps(answer)}