window.addEventListener("DOMContentLoaded", function(){
	var contextmenu_menu = [
		["/system/com/search/sites/edit", "dan_contextmenu_edit", "Редактировать"],
		["/system/com/search/sites/pub", "dan_contextmenu_pub", "Включить"],
		["/system/com/search/sites/unpub", "dan_contextmenu_unpub", "Заблокировать"],
		["/system/com/search/sites/up", "dan_contextmenu_up", "Вверх"],
		["/system/com/search/sites/down", "dan_contextmenu_down", "Вниз"],
		["#ITEMS.scan_site", "dan_contextmenu_scan_site", "Скан. сайт"],
		["#ITEMS.page_modal", "dan_contextmenu_scan_page", "Скан. страницу"],
		["#ITEMS.test_modal", "dan_contextmenu_search", "Поиск - тест"],
		["#ITEMS.delete_modal", "dan_contextmenu_delete", "Удалить"]
	];
	DAN.contextmenu.add("contextmenu_menu", contextmenu_menu, "left");
})


ITEMS = {
	page_current_num: 0,
	page_count_num: 0,
	site_id: 0,


	delete_modal(obj) {
		let id = obj.dataset.id
		let content =
			'<div style="text-align:center;font-size:20px">Удалить сайт</div>' +
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
				document.location.href = '/system/com/search/sites/delete/' + id
			}
		}
	},


	// Сканировать сайт - модальное окно
	scan_site(obj) {
		let id = obj.dataset.id
		let content =
			'<div style="margin-bottom:30px;text-align:center;font-size:20px">Сканировать сайт</div>' +
			'<div class="dan_flex_row">' +
				'<div style="margin-right:5px">' +
					'<input id="modal_submit" class="dan_button_green" type="submit" name="submit" value="Старт" data-id="' + id + '">' +
				'</div>' +
				'<div style="margin-left:5px">' +
					'<input id="modal_cancel" class="dan_button_white" type="submit" name="cancel" value="Отменить">' +
				'</div>' +
			'</div>'
		DAN.modal.add(content, 400)
		DAN.$('modal_cancel').onclick = DAN.modal.del
		DAN.$('modal_submit').onclick = () => {
			DAN.site_id = DAN.$('modal_submit').dataset.id
			DAN.modal.spinner()

			let form = new FormData()
			form.append('id', DAN.site_id)	
			DAN.ajax('/system/com/search/sites/scan_sitemap_ajax', form, function(data) {
				if (data.message != '') {
					alert(data.message)
					return
				}
				ITEMS.page_count_num = data.page_count_num
				ITEMS.scan_site_pages_count()
			})
		}
	},


	// Получаем количество страниц
	scan_site_pages_count() {
		let content =
			'<div style="margin-bottom:30px;text-align:center;font-size:20px;">Сканирование странц сайта</div>' +
			'<div class="items_progress_html">' +
				'<span id="items_progress_html">' + 
					'Обработано: <b id="items_progress_count">' + ITEMS.page_current_num + '</b> из <b>' + ITEMS.page_count_num + '</b>' +
				'</span>' +
			'</div>' +
			'<div><progress id="items_progress" max="' + ITEMS.page_count_num + '" value="0"></progress></div>' +
			'<div class="modal_center_wrap"><input style="margin-top: 20px;" id="modal_cancel" class="dan_button_green" type="submit" value="Закрыть"></div>' +
			'<div id="items_progress_pages"></div>'
		DAN.modal.add(content, 400)
		DAN.$('modal_cancel').style.display = 'none'
		ITEMS.scan_site_page_url()
	},


	// Сканируем странцу из sitemap
	scan_site_page_url() {
		let form = new FormData()
		form.append('id', DAN.site_id)
		form.append('act', 'sitemap')
		form.append('page_current_num', ITEMS.page_current_num)
		DAN.ajax('/system/com/search/sites/scan_page_ajax', form, function(data) {
			if (data.message != '') {
				alert(data.message)
				return
			}
			DAN.$('items_progress_count').innerHTML = ITEMS.page_current_num
			DAN.$('items_progress').value = ITEMS.page_current_num
			ITEMS.page_current_num += 1
			if (ITEMS.page_current_num <= ITEMS.page_count_num) {
				ITEMS.scan_site_page_url()
			} else {
				DAN.$('modal_cancel').style.display = 'inline'
				DAN.$('modal_cancel').onclick = DAN.modal.del
			}
		})
	},


	// Модальное окно - url страницы
	page_modal(obj) {
		let id = obj.dataset.id
		let content =
			'<div style="margin-bottom:30px;text-align:center;font-size:20px;">Сканирование странцы сайта</div>' +
			'<div style="text-align:center;margin:20px 0px">' +
				'<input id="page_url" class="dan_input w_300" name="url" type="text">' +
			'</div>' +
			'<div class="dan_flex_row">' +
				'<div style="margin-right:5px">' +
					'<input id="modal_submit" class="dan_button_green" type="submit" name="submit" value="Старт" data-id="' + id + '">' +
				'</div>' +
				'<div style="margin-left:5px">' +
					'<input id="modal_cancel" class="dan_button_white" type="submit" name="cancel" value="Отменить">' +
				'</div>' +
			'</div>'
		DAN.modal.add(content, 400)
		DAN.$('modal_cancel').style.display = 'none'
		DAN.$('modal_submit').onclick = ITEMS.scan_page_url	
	},


	// Сканирование url страницы
	scan_page_url() {
		DAN.site_id = DAN.$('modal_submit').dataset.id
		let url = DAN.$('page_url').value

		let form = new FormData()
		form.append('id', DAN.site_id)
		form.append('act', 'url')
		form.append('url', url)
		DAN.ajax('/system/com/search/sites/scan_page_ajax', form, function(data) {
			DAN.modal.add(data.message)
		})
	},


	// Тестирование поиска - модальная форма
	test_modal(obj) {
		let id = obj.dataset.id
		let content =
			'<h1>Тестирование поиска сайта</h1>' +
			'<form method="post" action="/system/com/search/sites/search_test" enctype="multipart/form-data">' +
			'<div style="text-align:center;margin:20px 0px">' +
				'<input class="dan_input w_400" name="text" type="text">' +
			'</div>' +
			'<input name="site_id" type="hidden" value="' + id + '">' +
			'<div class="dan_flex_row">' +
				'<div style="margin-right:5px">' +
					'<input id="modal_submit" class="dan_button_green" type="submit" name="submit" value="Поиск">' +
				'</div>' +
				'<div style="margin-left:5px">' +
					'<input id="modal_cancel" class="dan_button_white" type="submit" name="cancel" value="Отменить">' +
				'</div>' +
			'</div>' +
			'</form>'
		DAN.modal.add(content, 400)
		DAN.$('modal_cancel').onclick = DAN.modal.del
	}
}