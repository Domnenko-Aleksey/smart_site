import os
from Items import Items

def insert(SITE):
    SITE.debug('PATH: /system/items/insert.py')

    section_id = SITE.post['section_id']

    status = 1 if 'status' in SITE.post else 0
    data = {
        'id': SITE.p[3],
        'project_id': SITE.post['project_id'],
        'section_id': section_id,
        'name': SITE.post['name'],
        'questions': SITE.post['content_question_input'],
        'content': {
            'answer': SITE.post['content_answer'],
            'synthesis': SITE.post['content_synthesis'],
            'youtube': {
                'url': SITE.post['content_youtube_url'],
                'ratio': SITE.post['content_youtube_ratio']
            },
            'images': [],
            'text': SITE.post['content_text_input']
        },
        'status': status,
        'ordering': SITE.post['ordering']
    }

    ITEM = Items(SITE)
    item_id = ITEM.insert(data)
    
    path = '../files/projects/'+str(data['project_id'])+'/'+str(item_id)

    if not os.path.isdir(path):
        os.mkdir(path, mode=0o755)

    return {'redirect': '/system/items/' + section_id}
