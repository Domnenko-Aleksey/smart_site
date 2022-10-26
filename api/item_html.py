import config


def item_html(SITE, item):
    SITE.debug('PATH: /api/item_html.py')


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
                <div class="da_youtube" {youtube_ratio_padding}>
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
    images_1_class = ''
    if item['content']['images']:
        for i, image in enumerate(item['content']['images']):
            images_1_class = 'da_image_big' if i == 0 and youtube_html == '' else ''
            images_item += f'<img class="da_image {images_1_class}" src="{config.site_url}/files/projects/{item["project_id"]}/{item["id"]}/{image}">'

        images_html = '<div id="da_images_container" class="da_flex_row_start">' + images_item + '</div>'


    # --- Левый блок ---
    block_left_html = ''
    if youtube_html != '' or images_html != '':
        block_left_html = f'<div id="da_block_left" class="da_block_left">{youtube_html}{images_html}</div>'


    # --- Правый блок ---
    block_right_html = ''
    if item["content"]["text"] != '':
        block_right_html = f'<div id="da_block_right" class="da_block_right">{item["content"]["text"]}</div>'


    # --- Контент ---
    answer_content  =  '<div id="da_answer" data-id="' + str(item["id"]) + '">' + item["content"]["answer"] + '</div>'
    answer_content +=  '<div class="da_flex_row_start da_gap_20">' + block_left_html + block_right_html + '</div>'

    return answer_content