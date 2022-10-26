import json

def init_model_ajax(SITE):
    SITE.debug('PATH: /system/projects/init_model_ajax.py')

    SITE.model_init() 

    answer = {
        'answer': 'success'
    }
    return {'ajax': json.dumps(answer)} 