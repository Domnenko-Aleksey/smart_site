from Items import Items

def edit(SITE):
    SITE.debug('PATH: /system/items/edit.py')

    SITE.addHeadFile('/system/lib/DAN/DAN.css')
    SITE.addHeadFile('/system/lib/DAN/DAN.js')
    SITE.addHeadFile('/system/lib/DAN/bookmarks/bookmarks.css')
    SITE.addHeadFile('/system/lib/DAN/bookmarks/bookmarks.js')
    SITE.addHeadFile('/system/lib/DRAG_DROP/DRAG_DROP.css')
    SITE.addHeadFile('/system/lib/DRAG_DROP/DRAG_DROP.js')
    SITE.addHeadFile('/system/templates/css/edit.css')
    SITE.addHeadFile('/system/templates/css/item_edit.css')
    SITE.addHeadFile('/system/templates/js/item_edit.js')
    SITE.addHeadFile('/system/templates/plugin/css/plugin.css')
    SITE.addHeadFile('/system/lib/ckeditor5/build/ckeditor.js')

    ITEM = Items(SITE)

    if SITE.p[2] == 'add':
        project_id = SITE.p[3]
        title = 'Добавить'
        act = 'insert/'
        item = {
            'name': '',
            'questions': '',
            'content': {
                'answer': '',
                'synthesis': '',
                'question': '',
                'youtube': {
                    'url': '',
                    'ratio': '16x9'
                },
                'text': '',
                'images': []
            },
            'ordering': int(ITEM.getMaxOrdering(project_id)) + 1,
        }
        class_display_none = 'display_none'
        status_checked = ''
        questions_list = ''
        answer_question = ''
        id = ''
    else:
        id = SITE.p[3]
        title = 'Редактировать'
        act = 'update/' + id
        item = ITEM.getItem(id)
        status_checked = 'checked=""' if item['status'] == 1 else '';
        project_id = item['project_id']
        questions_list = ''
        answer_question = item['questions'].split(';')[0] if item['questions'] != '' else 'ДОБАВЬТЕ ВОПРОСЫ!'


        # --- Questions ---
        if item['questions'] != '':
            for q in item['questions'].split(';'):
                questions_list += f'''
                    <div class="da_question_wrap drag_drop_ico" data-target-id="da_questions_list" data-class="da_question_wrap"
                    data-f="ITEM_CONTENT.questions_update_ordering">
                        <div class="da_question_w">
                            <span class="da_question">{q}</span> <span class="da_question_del e_block_panel_ico" data-action="question_delete">&#10006</span>
                        </div>
                    </div>
                '''
        else:
            item['name'] + '?'

        class_display_none = ''


    # --- YouTube ---
    if item['content']['youtube']['ratio'] == '16x9':
        youtube_ratio_padding = 'style="padding-bottom:75%;"'
    else:
        youtube_ratio_padding = '';

    if item['content']['youtube']['url'] != '':
        youtube_url = item['content']['youtube']['url'].replace('watch?v=', 'embed/')
        youtube_url = youtube_url.replace('youtu.be', 'youtube.com/embed')
        youtube_url = youtube_url.split('&')[0]
        youtube_html = f'''
            <div id="da_youtube" class="block_youtube_wrap">
                <div class="dan_youtube" {youtube_ratio_padding}>
                    <iframe id="da_youtube_frame" style="width:560px; height:315px;" src="{youtube_url}" frameborder="0"
                    allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                </div>
            </div>
        '''
    else:
        youtube_html = '';


    # --- Images ---
    images_html = ''
    images_item = ''
    if item['content']['images']:
        images_input = ';'.join(item['content']['images'])
        for i, image in enumerate(item['content']['images']):
            images_item += f'''
 			<div class="e_block_images_wrap" data-block="case">
                <img class="da_image" src="/files/projects/{item['project_id']}/{id}/{image}">
				<div class="e_item_panel">
					<div class="drag_drop_ico" data-id="{image}" data-target-id="da_images_container" data-class="e_block_images_wrap"
                    data-f="ITEM_CONTENT.image_update_ordering" title="Перетащить изображение внутри блока" >
                        <svg><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="/system/templates/images/sprite.svg#cursor_24"></use></svg>
                    </div>
					<div class="e_block_panel_ico" data-id="{image}" data-action="image_delete_ajax" title="Удалить">
                        <svg><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="/system/templates/images/sprite.svg#delete"></use></svg>
                    </div>
				</div>
			</div>
            '''

        images_html = '<div id="da_images_container" class="dan_flex_row_start">' + images_item + '</div>'
    else:
        images_input = ''


    # --- Левый блок ---
    block_left_html = f'<div id="da_block_left" class="da_block_left">{youtube_html}{images_html}</div>'

    # --- Правый блок ---
    block_right_html = f'<div id="da_block_right" class="da_block_right">{item["content"]["text"]}</div>'


    # --- Контент ---
    SITE.content = f'''
        <h1>{title} тему</h1>
        <div class="dan_bookmarks_nav">
            <div class="dan_bookmark_head active" data-id="dan_bookmark_body_topic">Тема</div>
            <div class="dan_bookmark_head" data-id="dan_bookmark_body_questions">Вопросы</div>
            <div class="dan_bookmark_head" data-id="dan_bookmark_body_content">Контент</div>
        </div>
        <form method="post" action="/system/items/{act}" enctype="multipart/form-data">
        <div id="dan_bookmark_body_topic" class="dan_bookmark_body active">
            <div class="dan_flex_row">
                <div class="tc_l">Тема</div>
                <div class="tc_r dan_flex_grow">
                    <input class="dan_input w_400" name="name" type="text" required="" value="{item['name']}" title="Заполните название темы вопроса">
                </div>
            </div>
            <div class="dan_flex_row">
                <div class="tc_l">Порядок следования</div>
                <div class="tc_r dan_flex_grow">
                    <input class="dan_input" name="ordering" type="number" value="{item['ordering']}">
                </div>
            </div>
            <div class="dan_flex_row">
                <div class="tc_l">Статус</div>
                <div class="tc_r dan_flex_grow">
                    <input id="mp_item_status" class="dan_input" name="status" type="checkbox" value="1" {status_checked}>
                    <label for="mp_item_status"></label>
                </div>
            </div>
        </div>
        <div id="dan_bookmark_body_questions" class="dan_bookmark_body">
            <div class="dan_flex_row_start content_cpanel">
                <div id="button_question_add" class="header_ico_square">
                    <svg><use xlink:href="/system/templates/images/sprite.svg#add"></use></svg>
                    <div class="header_ico_square_text">Вопрос</div>
                </div>
                <div id="button_question_add_list" class="header_ico_square">
                    <svg><use xlink:href="/system/templates/images/sprite.svg#add_list"></use></svg>
                    <div class="header_ico_square_text">Cписком</div>
                </div>
            </div>
            <div id="da_questions_list">{questions_list}</div>
        </div>
        <div id="dan_bookmark_body_content" class="dan_bookmark_body">
            <div class="dan_flex_row_start content_cpanel">
                <div id="button_answer" class="header_ico_square">
                    <svg><use xlink:href="/system/templates/images/sprite.svg#audio"></use></svg>
                    <div class="header_ico_square_text">Ответ</div>
                </div>
                <div id="button_youtube" class="header_ico_square">
                    <svg><use xlink:href="/system/templates/images/sprite.svg#youtube"></use></svg>
                    <div class="header_ico_square_text">youtube</div>
                </div>
                <div id="button_images" class="header_ico_square {class_display_none}">
                    <svg><use xlink:href="/system/templates/images/sprite.svg#image"></use></svg>
                    <div class="header_ico_square_text">Изобр.</div>
                </div>
                <div id="button_text" class="header_ico_square">
                    <svg><use xlink:href="/system/templates/images/sprite.svg#text"></use></svg>
                    <div class="header_ico_square_text">Текст</div>
                </div>
                <div id="button_icons" class="header_ico_square">
                    <svg><use xlink:href="/system/templates/images/sprite.svg#star"></use></svg>
                    <div class="header_ico_square_text">Иконки</div>
                </div>
                <div id="button_button" class="header_ico_square">
                    <svg><use xlink:href="/system/templates/images/sprite.svg#button"></use></svg>
                    <div class="header_ico_square_text">Кнопка</div>
                </div>
                <div id="button_form" class="header_ico_square">
                    <svg><use xlink:href="/system/templates/images/sprite.svg#form"></use></svg>
                    <div class="header_ico_square_text">Форма</div>
                </div>
            </div>
            <div id="da_question">{answer_question}</div>
            <div class="da_synthesis dan_flex_row">
                <div id="da_synthesis_icon" class="da_synthesis_icon" title="Копировать ответ">
                    <svg style="width:30px; height:30px; cursor:pointer;"><use xlink:href="/system/templates/images/sprite.svg#audio"></use></svg>
                </div>
                <input id="da_synthesis_input" class="dan_input" name="content_synthesis" value="{item['content']['synthesis']}", placeholder="Ответ голосом">
            </div>
            <div id="da_answer" contenteditable="true">{item['content']['answer']}</div>
            <div id="da_container" class="dan_flex_row da_p_40_0 da_gap_20">{block_left_html}{block_right_html}</div>
        </div>
        <div class="dan_flex_row da_p_40_0">
            <div class="tc_l">
                <input id="da_submit" class="dan_button_green" type="submit" name="submit" value="Сохранить" data-id="{id}">
            </div>
            <div class="tc_r">
                <a href="/system/items/{project_id}" class="dan_button_white">Отменить</a>
            </div>
        </div>
        <input type="hidden" name="project_id" value="{project_id}">
        <input id="content_answer_input" type="hidden" name="content_answer" value="{item['content']['answer']}">
        <input id="content_youtube_url_input" type="hidden" name="content_youtube_url" value="{item['content']['youtube']['url']}">
        <input id="content_youtube_ratio_input" type="hidden" name="content_youtube_ratio" value="{item['content']['youtube']['ratio']}">
        <input id="content_images_input" type="hidden" name="content_images" value="{images_input}">
        <textarea id="content_text_input" style="display:none" name="content_text_input">{item['content']['text']}</textarea>
        <input id="content_question_input" type="hidden" name="content_question_input" value="{item['questions']}">
        </form>
    '''