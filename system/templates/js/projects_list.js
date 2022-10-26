window.addEventListener("DOMContentLoaded", function(){
	var contextmenu_menu = [
		["/system/projects/edit", "dan_contextmenu_edit", "Редактировать"],
		["/system/projects/pub", "dan_contextmenu_pub", "Включить"],
		["/system/projects/unpub", "dan_contextmenu_unpub", "Заблокировать"],
		["/system/projects/up", "dan_contextmenu_up", "Вверх"],
		["/system/projects/down", "dan_contextmenu_down", "Вниз"],
		["#PROJECTS.export_to_pandas", "dan_contextmenu_pandas", "В pandas"],
		["#PROJECTS.get_model", "dan_contextmenu_fit", "Обучить модель"],
		["#PROJECTS.init_model", "dan_contextmenu_init", "Сбросить обучение"],
		["#PROJECTS.load_api_model_ajax", "dan_contextmenu_load", "Загрузить модель в API"],
		["#PROJECTS.check_bert_ajax", "dan_contextmenu_check", "Проверка BERT"],
		["#PROJECTS.delete_modal", "dan_contextmenu_delete", "Удалить"]
	];
	DAN.contextmenu.add("contextmenu_menu", contextmenu_menu, "left");
})


PROJECTS = {
	model: {
		'project_id': false,
		'epochs_count': 0,  // Количество эпох обучения модели
		'epoch_current': 0,  // Текущая эпоха
		'topic_sum': 0,  // Количесто топиков
		'topic_current': 0,  // Текущий топик
	},


	delete_modal(obj){
		let id = obj.dataset.id
		let content =
			'<div style="text-align:center;font-size:20px">Удалить проект</div>' +
			'<div style="text-align:center;margin:20px 0px">' +
				'<input id="modal_checkbox" type="checkbox" name="check"> Подтверждаю удаление' +
			'</div>' +
			'<div class="dan_flex_row">' +
				'<div style="margin-right:5px">' +
					'<input id="modal_submit" class="dan_button_red" type="submit" name="submit" value="Удалить">' +
				'</div>' +
				'<div style="margin-left:5px">' +
					'<input id="modal_cancel" class="dan_button_white" type="submit" name="cancel" value="Отменить">' +
				'</div>' +
			'</div>'
		DAN.modal.add(content, 400)
		DAN.$('modal_cancel').onclick = DAN.modal.del
		DAN.$('modal_submit').onclick = () => {
			let check = DAN.$('modal_checkbox')
			if (!check.checked) {
				alert('Вы не подтвердили удаление пользователя - необходимо поставить галочку')
				return
			} else {
				document.location.href = '/system/projects/delete/' + id
			}
		}
	},


	// Экспорт данных в pandas
	export_to_pandas(obj){
		let id = obj.dataset.id
		let content =
			'<div style="text-align:center;font-size:20px; padding-bottom:20px;">Экспорт данных в pandas</div>' +
			'<div class="dan_flex_row">' +
				'<div style="margin-right:5px">' +
					'<input id="modal_submit" class="dan_button_red" type="submit" name="submit" value="Старт">' +
				'</div>' +
				'<div style="margin-left:5px">' +
					'<input id="modal_cancel" class="dan_button_white" type="submit" name="cancel" value="Отменить">' +
				'</div>' +
			'</div>'
		DAN.modal.add(content, 400)
		DAN.$('modal_cancel').onclick = DAN.modal.del
		DAN.$('modal_submit').onclick = () => {
			let form = new FormData()
			form.append('id', id)
			DAN.ajax('/system/projects/get_pandas_ajax/'+id, form, (data)=>{
				let link_html = '<div style="text-align:center;"><a href="' + data['link'] + '">Датафрейм</a></div>'
				DAN.modal.add(link_html, 300)
			})
			DAN.modal.spinner()
		}
	},


	// Проверка BERT
	check_bert_ajax(obj){
		let form = new FormData()
		DAN.ajax('/system/projects/check_bert_ajax/', form, (data)=>{
			DAN.modal.add(data.content, 320)
		})
		DAN.modal.spinner()
	},


	// Шаг 1. Форма для обучения модели
	get_model(obj) {
		PROJECTS.model.project_id = obj.dataset.id
		let content =
			'<div style="text-align:center;font-size:20px; padding-bottom:20px;">Обучить модель</div>' +
			'<div style="text-align:center;margin:20px 0px">' +
				'<input id="modal_epochs" class="dan_input" type="number" name="epochs" min="10" max="1000" value="500"> эпох обучения' +
			'</div>' +
			'<div class="dan_flex_row">' +
				'<div style="margin-right:5px">' +
					'<input id="modal_submit" class="dan_button_green" type="submit" name="submit" value="Старт">' +
				'</div>' +
				'<div style="margin-left:5px">' +
					'<input id="modal_cancel" class="dan_button_white" type="submit" name="cancel" value="Отменить">' +
				'</div>' +
			'</div>'
		DAN.modal.add(content, 400)
		DAN.$('modal_cancel').onclick = DAN.modal.del
		DAN.$('modal_submit').onclick = PROJECTS.get_model_topic  // Получаем топики из БД.
	},


	// Шаг 2. Получаем список топиков.
	get_model_topic() {
		PROJECTS.model.epochs_count = DAN.$('modal_epochs').value
		let form = new FormData()
		form.append('project_id', PROJECTS.model.project_id)
		form.append('epochs_count', PROJECTS.model.epochs_count)
		DAN.ajax('/system/projects/get_topic_list_ajax/', form, (data) => {
			let content =
			'<h1 style="text-align:center;">' + data.message + '</h1>' +
			'<div class="items_progress_html">' +
				'<span id="items_progress_html">' + 
					'Обработано: <b id="items_progress_current">' + data.item_current + '</b> из <b id="items_progress_count">' + data.items_count + '</b>' +
				'</span>' +
			'</div>' +
			'<div><progress id="items_progress" max="' + data.items_count + '" value="' + data.item_current + '"></progress></div>' + 
			'<div id="items_message"></div>'
			DAN.modal.add(content)
			PROJECTS.get_vectors()
		})
		DAN.modal.spinner()
	},


	// Шаг 3. Получаем BERT вектора.
	get_vectors() {
		let form = new FormData()
		DAN.ajax('/system/projects/get_vectors_ajax/', form, (data) => {
			DAN.$('items_progress_count').innerHTML = data.items_count
			DAN.$('items_progress_current').innerHTML = data.item_current
			DAN.$('items_progress').value = data.item_current
			DAN.$('items_message').innerHTML = data.message
			if (data.finish == '') {
				PROJECTS.get_vectors()
			} else {
				// Закончили сборку датасета - создаём модель
				PROJECTS.create_model()
			}
		})
	},


	// Шаг 4. Создаём модель.
	create_model() {
		let content = '<h1 style="text-align:center;">Создание модели</h1>'
		DAN.modal.add(content)

		let form = new FormData()
		form.append('project_id', PROJECTS.model.project_id)
		DAN.ajax('/system/projects/create_model_ajax/', form, (data) => {
			let content =
			'<h1 style="text-align:center;">Обучение модели</h1>' +
			'<div style="padding:20px 0px; text-align:center;">Точность: <b id="model_accuracy"></b></div>' +
			'<div class="items_progress_html">' +
				'<span id="items_progress_html">' + 
					'Обработано: <b id="items_progress_current">' + PROJECTS.model.epoch_current + '</b> из <b id="items_progress_count">' + PROJECTS.model.epochs_count + '</b>' +
				'</span>' +
			'</div>' +
			'<div><progress id="items_progress" max="' + PROJECTS.model.epochs_count + '" value="' + PROJECTS.model.epoch_current + '"></progress></div>' + 
			'<div id="items_message"></div>'
			DAN.modal.add(content)	
			PROJECTS.fit_model()		
		})
	},


	// Шаг 4. Обучаем модель.
	fit_model() {
		console.log('FIT MODEL')
		let form = new FormData()
		form.append('project_id', PROJECTS.model.project_id)
		DAN.ajax('/system/projects/fit_model_ajax/', form, (data) => {
			console.log(data)
			DAN.$('items_progress_current').innerHTML = data.current_num
			DAN.$('items_progress').value = data.current_num
			DAN.$('model_accuracy').innerHTML = Math.round(data.accuracy * 10000)/10000

			if (data.finish == '') {
				PROJECTS.fit_model()
			} else {
				let content =
				'<h1 style="text-align:center;">Модель обучена</h1>' +
				'<div><img src="/system/files/projects/' + PROJECTS.model.project_id + '/progress.png?' + Math.floor(Math.random() * 100000) + '"></div>'
				DAN.modal.add(content)
			}
		})
	},


	// Сброс процесса обучения модели
	init_model(obj) {
		let form = new FormData()
		form.append('project_id', obj.dataset.id)
		DAN.ajax('/system/projects/init_model_ajax/', form, (data) => {
			let content = '<h1 style="text-align:center;">Процесс обучения модели сброшен</h1>'
			DAN.modal.add(content)			
		})
		DAN.modal.spinner()	
	},


	// Загрузить модель в API
	load_api_model_ajax(obj) {
		let form = new FormData()
		form.append('project_id', obj.dataset.id)
		DAN.ajax('/system/projects/load_api_model_ajax/', form, (data) => {
			let content = '<h1 style="text-align:center;">Модель загружена для проекта ' + obj.dataset.id + '</h1>'
			DAN.modal.add(content)			
		})
		DAN.modal.spinner()	
	}
}