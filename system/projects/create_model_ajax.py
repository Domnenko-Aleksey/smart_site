import json
import numpy as np

import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import Input, Dense, BatchNormalization
# from tensorflow.keras.utils import plot_model, to_categorical
from tensorflow.keras.optimizers import Adam
# from tensorflow.keras.callbacks import ModelCheckpoint, Callback

def create_model_ajax(SITE):
    SITE.debug('PATH: /system/items/create_model_ajax.py')

    project_id = SITE.post['project_id']
    SITE.debug(f'PROJECT ID: {project_id}')

    # Создание модели
    classes_num = SITE.model['items_count']
    x_input = Input(shape=(768), name='input')
    x = Dense(768, activation='relu')(x_input)
    x = BatchNormalization()(x)
    x_output = Dense(classes_num, activation='softmax')(x)
    model = Model(inputs=x_input, outputs=x_output)
    model.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=(0.00001)), metrics=['accuracy'])
    SITE.model['model'] = model

    SITE.model['x'] = np.array(SITE.model['x'])
    SITE.model['y'] = np.array(SITE.model['y'])

    SITE.debug('DATA IS READY, MODEL COMPILE:')
    SITE.debug(SITE.model['x'].shape)
    SITE.debug(SITE.model['y'].shape)  

    answer = {'answer': 'success'}
    return {'ajax': json.dumps(answer)}