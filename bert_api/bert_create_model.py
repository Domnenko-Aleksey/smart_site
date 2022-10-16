import json
from aiohttp import web

import pandas as pd
import numpy as np

import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import Input, Dense, Dropout
from tensorflow.keras.layers import Embedding, Flatten, Input, concatenate, Reshape
from tensorflow.keras.utils import plot_model, to_categorical
from tensorflow.keras.optimizers import Adam, Adadelta
from tensorflow.keras.callbacks import ModelCheckpoint, Callback
import tensorflow_hub as hub
import tensorflow_text as text


# Создаёт комбинированную модель - 'bert_preprocess' + 'bert_encoder'
path = './model/bert_pt_model.h5' 


app = web.Application(client_max_size=1024**100)


async def bert_create_model(request):
    print('===== BERT CREATE MODEL =====')

    # Загрузка модели BERT
    # Мы загрузим две модели, одну для предварительной обработки, а другую для кодирования.
    bert_preprocess = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_multi_cased_preprocess/3")
    bert_encoder = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_multi_cased_L-12_H-768_A-12/4", trainable=True)

    # Инициализация слоёв
    text_input = Input(shape=(), dtype=tf.string, name='text')
    preprocessed_text = bert_preprocess(text_input)
    outputs = bert_encoder(preprocessed_text)

    # Модель
    text_input = Input(shape=(), dtype=tf.string, name='text')
    preprocessed_text = bert_preprocess(text_input)
    outputs = bert_encoder(preprocessed_text)
    x_output = outputs['pooled_output']

    model = Model(inputs=[text_input], outputs = [x_output])
    # model.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=(0.000005)), metrics=['accuracy'])

    model.summary()

    # Тестируем - на вход подаём текст
    question = 'Сколько стоит сайт'
    predict = model.predict([question])
    print('PREDICT SHAPE', predict.shape)

    # Сохраняем модель
    model.save(path)

    print('MODEL SAVED')

    # text = request.post['text']
    answer = {'answer': 'success', 'message': '--- OK ---'}
    return web.HTTPOk(text=json.dumps(answer))


app.add_routes([
    web.get('/bert_create_model{url:.*}', bert_create_model),
    web.post('/bert_create_model{url:.*}', bert_create_model),
])

if __name__ == '__main__':
    web.run_app(app, port=9100)