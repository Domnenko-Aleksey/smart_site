import os
import json
from pathlib import Path
import shutil

from matplotlib import pyplot as plt

def fit_model_ajax(SITE):
    SITE.debug('PATH: /system/items/fit_model_ajax.py')

    project_id = SITE.post['project_id']
    SITE.debug(f'PROJECT ID: {project_id}')

    history = SITE.model['model'].fit(
        SITE.model['x'],
        SITE.model['y'], 
        epochs = 1,
        batch_size = 32,
        shuffle = True,
        verbose = 1
    )

    SITE.debug(f'EPOCH: {SITE.model["epoch_current"]}')
    SITE.debug(f'HISTORY: {history.history["accuracy"]}')

    SITE.model['history'].append(history.history["accuracy"])
    SITE.model['epoch_current'] += 1

    if SITE.model['epoch_current'] <= SITE.model['epochs_count']:
        finish = ''
    else:
        finish = 'finish'

        # --- Сохраняем модель ---
        dir_og = Path('../api')
        owner = dir_og.owner()
        group = dir_og.group()

        dir_model = '../api/files/' + str(project_id)
        make_dir(dir_model, owner, group) # Создаём директории, если оне не существуют и устанавливаем права для '/api'

        path_model = dir_model + '/model.h5'
        SITE.model['model'].save(path_model)
        shutil.chown(path_model, user=owner, group=group)

        # --- Сохраняем график прогресса ---
        dir_og = Path('files')
        owner = dir_og.owner()
        group = dir_og.group()
        dir_progress = 'files/projects/' + str(project_id)
        make_dir(dir_progress, owner, group)  # Создаём директории, если оне не существуют и устанавливаем права для '/system'
        # Создаём изображение прогресса

        path_progress = dir_progress + '/progress.png'
        if os.path.isfile(path_progress): 
            os.remove(path_progress)
        plt.plot(SITE.model['history'])
        plt.title("Accuracy:")
        plt.ylabel("Acc")
        plt.xlabel("Epoch")
        plt.savefig(path_progress)
        plt.close()
        shutil.chown(path_progress, user=owner, group=group)
        SITE.model_init()  # Сбрасываем настройки

    answer = {
        'answer': 'success', 
        'current_num': SITE.model['epoch_current'],
        'accuracy': history.history["accuracy"],
        'finish': finish
    }
    return {'ajax': json.dumps(answer)}


# Создание и установка прав директории
def make_dir(path, owner, group):
    if not os.path.isdir(path):
        os.makedirs(path, mode=0o755, exist_ok=True)
        path_arr = path.split('/')
        p_cur = ''
        for p in path_arr:
            # Для вложенных директорий меняем пользователя и группу
            p_cur += p + '/'
            shutil.chown(p_cur, user=owner, group=group)    