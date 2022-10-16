import os

import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.models import load_model


class ClsModel:
    def __init__(self, db):
        self.db = db


    # Загружает модель
    def loadModel(self, id=False):
        print('LOAD MODEL')
        if id:
            model_file = f'files/{id}/model.h5'
            if os.path.isfile(model_file):
                return load_model(model_file)
        else:
            models= {}
            sql = "SELECT id FROM projects WHERE status=1"   
            self.db.execute(sql)
            projects = self.db.fetchall()
            for project in projects:
                model_file = f'files/{project["id"]}/model.h5'
                if os.path.isfile(model_file):
                    models[project['id']] = load_model(model_file)
            return models
                
