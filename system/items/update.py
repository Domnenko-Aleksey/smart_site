from Items import Items

def update(SITE):
    print('PATH: /system/items/update.py')

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
            'images': SITE.post['content_images'].split(';') if SITE.post['content_images'] != '' else [],
            'text': SITE.post['content_text_input']
        },
        'status': status,
        'ordering': SITE.post['ordering']
    }

    ITEM = Items(SITE)
    ITEM.update(data)
    
    return {'redirect': '/system/items/' + section_id}
