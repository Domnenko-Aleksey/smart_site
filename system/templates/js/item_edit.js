window.addEventListener('DOMContentLoaded', function(){
	ITEM_CONTENT.init()
});

ITEM_CONTENT = {
	editor: false,

	init(){
		DRAG_DROP()
		DAN.$('button_question_add').onclick = this.question_add
		DAN.$('button_question_add_list').onclick = this.question_add_list
		DAN.$('button_answer').onclick = this.answer_edit
		DAN.$('da_synthesis_icon').onclick = this.synthesis_copy
		DAN.$('da_answer').onclick = this.answer_edit
		DAN.$('da_answer').onblur = () => {
			DAN.$('content_answer_input').value = DAN.$('da_answer').innerHTML
		}
		DAN.$('button_images').onclick = this.images_add	
		DAN.$('button_youtube').onclick = this.youtube_edit
		DAN.$('button_text').onclick = () => {
			DAN.$('da_block_right').focus()
		}
		DAN.$('da_block_right').onblur = () => {
			DAN.$('content_text_input').value = ITEM_CONTENT.editor.getData()
		}
		
		// События на иконках
		let icons = document.getElementsByClassName('e_block_panel_ico')
		for (i = 0; i < icons.length; i++) {
			icons[i].onclick = function(){
				ITEM_CONTENT[this.dataset.action](this)
			}
		}

		if (!ITEM_CONTENT.editor) {
			InlineEditor
				.create(DAN.$('da_block_right'))
				.then(newEditor => {ITEM_CONTENT.editor = newEditor;})
				.catch(error => {console.error(error);});
		}
	},


	// ======= ВОПРОСЫ =======
	// Добавить вопрос
	question_add() {
		let content = 
			'<h2>Добавить вопрос</h2>' +
			'<div class="dan_flex_row e_p_5_20">' +
				'<div class="e_str_left e_flex_basis_100">Вопрос (регистрозависимый):</div>' +
				'<div class="e_str_right">' +
					'<div class="e_flex_center_h"><input id="e_block_question" class="dan_input" name="question_add" style="width:100%" value=""></div>' +
				'</div>' +
			'</div>' +
			'<div class="e_modal_wrap_buttons">' +
				'<div>' +
					'<input id="e_modal_submit" class="dan_button_green" type="submit" name="submit" value="Сохранить">' +
				'</div>' +
				'<div>' +
					'<input id="e_modal_cancel" class="dan_button_white" type="submit" name="cancel" value="Отменить">' +
				'</div>' +
			'</div>';
		DAN.modal.add(content, 600)
		DAN.$('e_modal_cancel').onclick = DAN.modal.del
		DAN.$('e_modal_submit').onclick = () => {
			// Вопросы, полученные с HTML
			let question_arr = ITEM_CONTENT.questions_html_to_arr()

			// Вопрос, полученный с формы
			let question = DAN.$('e_block_question').value
			question = question.replace(/[+.;!?]*/g, '')
			question = question.trim()
			question_arr.push(question);

			// Создаёт список вопросов в HTML
			DAN.$('da_questions_list').innerHTML = ''
			let question_unique = new Set(question_arr)  // Уникальные значения массива
			question_unique.forEach(ITEM_CONTENT.insertQuestion)
			DAN.$('content_question_input').value = ITEM_CONTENT.questions_html_to_arr().join(';')

			DAN.modal.del()
			ITEM_CONTENT.init()
		}
	},


	// Добавить вопросы списком
	question_add_list() {
		let content = 
			'<h2>Добавить вопросы списком</h2>' +
			'Каждый вопрос - с новой строки, строки приводятся к нижнему регистру' + 
			'<div style="padding-top:10px;">' +
				'<textarea id="e_block_question" style="width:100%;height:400px;padding:5px 7px;"></textarea>' +
			'</div>' +
			'<div class="e_modal_wrap_buttons">' +
				'<div>' +
					'<input id="e_modal_submit" class="dan_button_green" type="submit" name="submit" value="Сохранить">' +
				'</div>' +
				'<div>' +
					'<input id="e_modal_cancel" class="dan_button_white" type="submit" name="cancel" value="Отменить">' +
				'</div>' +
			'</div>';
		DAN.modal.add(content, 600)
		DAN.$('e_modal_cancel').onclick = DAN.modal.del
		DAN.$('e_modal_submit').onclick = () => {
			// Вопросы, полученные с HTML
			let question_arr_1 = ITEM_CONTENT.questions_html_to_arr()

			// Вопросы, полученные с формы
			let question = DAN.$('e_block_question').value
			question = question.replace(/[+.;!?]*/g, '')
			question = question.trim().toLowerCase()
			question_arr_2 = question.split('\n')
			question_arr = question_arr_1.concat(question_arr_2);

			// Создаёт список вопросов в HTML
			DAN.$('da_questions_list').innerHTML = ''
			let question_unique = new Set(question_arr)  // Уникальные значения массива
			question_unique.forEach(ITEM_CONTENT.insertQuestion)
			DAN.$('content_question_input').value = ITEM_CONTENT.questions_html_to_arr().join(';')

			DAN.modal.del()
			ITEM_CONTENT.init()
		}
	},


	// Добавляет вопросы в html
	insertQuestion(question){
		if (question.length < 4 || question.length > 80)
			return
		question_html = '<div class="da_question_wrap drag_drop_ico" data-target-id="da_questions_list" ' +
		'data-class="da_question_wrap" data-f="ITEM_CONTENT.questions_update_ordering">' +
			'<div class="da_question_w">' + 
				'<span class="da_question">' + question + '</span> ' +
				'<span class="da_question_del e_block_panel_ico" data-action="question_delete">&#10006</span>' + 
			'</div>' + 
		'</div>'
		DAN.$('da_questions_list').insertAdjacentHTML('beforeend', question_html);
	},

	
	// Обновляет порядок следования изображений в скрытом input
	questions_update_ordering(){
		DAN.$('content_question_input').value = ITEM_CONTENT.questions_html_to_arr().join(';')
	},
	

	// Удаляет изображение
	question_delete(obj){
		let node = obj.parentElement.parentElement
		node.remove()
		DAN.$('content_question_input').value = ITEM_CONTENT.questions_html_to_arr().join(';')
	},


	// Получает все вопросы и помещаем из в массив
	questions_html_to_arr(){
		let da_question_arr = document.getElementsByClassName('da_question')
		questions_arr = []
		for (i=0; i<da_question_arr.length; i++) {
			let question = da_question_arr[i].innerHTML
			question = question.replace(/[+.;!?]*/g, '')
			question = question.trim()
			questions_arr.push(question)
		}
		return questions_arr
	},


	// ======= ОТВЕТ =======
	// Редактирование ответа
	answer_edit() {
		let answer_node = DAN.$('da_answer')

		if (answer_node.innerHTML == '')
			answer_node.innerHTML = 'Текст ответа'
	},
	
	
	// Копируем в синтезируемый ответ данные из ответа
	synthesis_copy() {
		let answer = DAN.$('da_answer').innerHTML
		let synthesis_input = DAN.$('da_synthesis_input')
		if (answer == '')
			alert('Ответ пустой, копирование отменено')
		else
			synthesis_input.value = answer
	},


	// Редактирование ссылки на youtube_edit
	youtube_edit() {
		content =
			'<h2>Редактировать ссылку на YouTube</h2>' +
			'<div class="dan_flex_row e_p_5_20">' +
				'<div class="e_str_left e_flex_basis_100">URL:</div>' +
				'<div class="e_str_right">' +
					'<div class="e_flex_center_h"><input id="e_block_video_modal_url" class="dan_input" name="url" style="width:100%" value=""></div>' +
				'</div>' +
			'</div>' +
			'<div class="dan_flex_row e_p_5_20">' +
				'<div class="e_str_left e_flex_basis_100">Формат:</div>' +
				'<div class="e_str_right">' +
					'<div class="e_flex_center_h">' +
						'<select id="e_youtube_modal_ratio" class="dan_input" name="ratio">' +
							'<option id="e_youtube_modal_ratio_16x9" value="16x9">16 x 9</option>' +
							'<option id="e_youtube_modal_ratio_4x3" value="4x3">4 x 3</option>' +
						'</select>' +
					'</div>' +
				'</div>' +
			'</div>' +
			'<div class="e_modal_wrap_buttons">' +
				'<div>' +
					'<input id="e_modal_submit" class="dan_button_green" type="submit" name="submit" value="Сохранить">' +
				'</div>' +
				'<div>' +
					'<input id="e_modal_cancel" class="dan_button_white" type="submit" name="cancel" value="Отменить">' +
				'</div>' +
			'</div>';
		DAN.modal.add(content, 600)
		DAN.$('e_block_video_modal_url').value = DAN.$('content_youtube_url_input').value
		let ratio = DAN.$('content_youtube_ratio_input').value

		if (ratio == '16x9')
			DAN.$('e_youtube_modal_ratio_16x9').selected = 'selected'
		else
			DAN.$('e_youtube_modal_ratio_4x3').selected = 'selected'

		// Кнопки формы
		DAN.$('e_modal_submit').onclick = () => {
			let url = DAN.$('e_block_video_modal_url').value
			DAN.$('content_youtube_url_input').value = url
			DAN.$('content_youtube_ratio_input').value = DAN.$('e_youtube_modal_ratio').value
			DAN.modal.del()

			let youtube_src = url.replace('watch?v=', 'embed/')
			youtube_src = youtube_src.replace('youtu.be', 'youtube.com/embed')
			youtube_src = youtube_src.split('&')[0]
			
			let da_image_arr = document.getElementsByClassName('da_image')
			let e_block_images_wrap_arr = document.getElementsByClassName('e_block_images_wrap')
			
			if (youtube_src) {
				let youtube_frame = DAN.$('da_youtube_frame')
				if (youtube_frame) {
					youtube_frame.src = youtube_src
				} else {
					let youtube_wrap =
						'<div id="da_youtube" class="block_youtube_wrap">' +
							'<div class="dan_youtube">' +
								'<iframe id="da_youtube_frame" style="width:560px; height:315px;" src="' + youtube_src + '" frameborder="0" ' +
								'allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>' +
							'</div>' +
						'</div>'
					let block_left = DAN.$('da_block_left')
					if (block_left) {
						block_left.innerHTML = youtube_wrap + block_left.innerHTML
					}
				}
			} else {
				if (DAN.$('da_youtube'))
					DAN.$('da_youtube').remove()
			}
		}

		DAN.$('e_modal_cancel').onclick = DAN.modal.del
	},


	// Добавяляет изображений
	images_add() {
		let content =
			'<h2>Добавить изображения</h2>' +
			'<div class="dan_flex_row e_p_5_20">' +
				'<div class="e_str_left e_flex_basis_100">Изображения:</div>' +
				'<div class="e_str_right">' +
					'<div class="e_flex_center_h"><input id="e_images_input_file" type="file" name="file" multiple accept="image/*"></div>' +
				'</div>' +
			'</div>' +
			'<div class="e_modal_wrap_buttons">' +
				'<div>' +
					'<input id="e_modal_submit" class="dan_button_green" type="submit" name="submit" value="Сохранить">' +
				'</div>' +
				'<div>' +
					'<input id="e_modal_cancel" class="dan_button_white" type="submit" name="cancel" value="Отменить">' +
				'</div>' +
			'</div>';

		DAN.modal.add(content)

		// Проверка файлов
		let file_input = DAN.$('e_images_input_file')
		file_input.onchange = () => {
			let files = file_input.files
			if (files.length > 0) {
				for (i=0; i < files.length; i++) {
					if (files[i].size > 3000000) {
						alert('Размер изображения ' + files[i] + ' слишком большой')
						return
					}
					if (files[0].type != 'image/jpeg' &&
						files[0].type !=  'image/gif' &&
						files[0].type != 'image/png' &&
						files[0].type != 'image/webp') {
						alert('Неверный формат изображения')
						return
					}
				}
			}
		}

		DAN.$('e_modal_submit').onclick = () => {
			ITEM_CONTENT.images_send_ajax(file_input.files)
		}
		DAN.$('e_modal_cancel').onclick = DAN.modal.del
	},


	// Отправка файлов методом ajax
	images_send_ajax(files) {
		console.log('send ajax', files)
		let id = DAN.$('da_submit').dataset.id

		let num = 0

		if (files.length == 0) {
			DAN.modal.add('<h2>Изображения отсутствуют</h2>', 450)
			return
		}

		let progress_bar =
		'<h2>Обработка изображений</h2>' +
		'<div class="e_progress_html">' +
			'<span>Обработано: <b id="e_ptogress_num">0</b> из <b>' + files.length + '</b></span></div>' +
		'<div><progress id="e_ptogress_bar" max="' + files.length + '" value="0"></progress></div>';
		DAN.modal.add(progress_bar, 450)

		for (i=0; i<files.length; i++) {
			var form = new FormData()
			form.append('id', id)
			form.append('file', files[i])

			DAN.ajax('/system/items/image_upload_ajax/'+id, form, (data)=>{
				// Создаём контейнеры, если они отсутствуют
				if (!DAN.$('da_block_left')) {
					DAN.$('da_container').innerHTML = '<div id="da_block_left" class="da_block_left"></div><div id="da_block_right" class="da_block_right"></div>'
				}

				if (!DAN.$('da_images_container')) {
					DAN.$('da_block_left').innerHTML = '<div id="da_images_container" class="dan_flex_row_start"></div>'
				}
				
				let project_id = data['project_id']
				let file_name = data['file_name']
				let content = 
					'<div class="e_block_images_wrap" data-block="case">' +
						'<img class="da_image" src="/files/projects/' + project_id + '/' + id + '/' + file_name + '">' +
						'<div class="e_item_panel">' +
							'<div class="drag_drop_ico" data-id="' + file_name + '" data-target-id="da_images_container" data-class="e_block_images_wrap" data-f="ITEM_CONTENT.image_update_ordering" title="Перетащить изображение внутри блока">' +
								'<svg><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="/system/templates/images/sprite.svg#cursor_24"></use></svg>' +
							'</div>' +
							'<div class="e_block_panel_ico" data-id="{image}" data-action="image_delete_ajax" title="Удалить">' +
								'<svg><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="/system/templates/images/sprite.svg#delete"></use></svg>' +
							'</div>' +
						'</div>' +
					'</div>'

				DAN.$('da_images_container').insertAdjacentHTML('beforeend', content)					
				DAN.$('e_ptogress_num').innerHTML = num
				DAN.$('e_ptogress_bar').value = num

				DAN.$('content_images_input').value = ITEM_CONTENT.images_to_str()
				ITEM_CONTENT.init()

				num++

				if (num == files.length)
					DAN.modal.del()
			})
		}
	},


	// Обновляет порядок следования изображений в скрытом input
	image_update_ordering(){
		DAN.$('content_images_input').value = ITEM_CONTENT.images_to_str()
	},


	// Удаляет изображение
	image_delete_ajax(obj){
		let id = DAN.$('da_submit').dataset.id
		let name = obj.dataset.id
		let node = obj.parentElement.parentElement
		
		var form = new FormData()
		form.append('id', id)
		form.append('file_name', name)

		DAN.ajax('/system/items/image_delete_ajax/'+id, form, (data)=>{
			DAN.$('content_images_input').value = ITEM_CONTENT.images_to_str()
		})
		node.remove()
	},
	
	
	// Получает все изображения и помещает названия файлов в строку через ';'
	images_to_str(){
		let images_arr = document.getElementsByClassName('da_image')
		let src_arr = []
		for (i=0; i<images_arr.length; i++) {
			let src = images_arr[i].src
			let src_a = src.split('/')
			src_arr.push(src_a[src_a.length - 1])
		}
		return src_arr.join(';')
	}
}
