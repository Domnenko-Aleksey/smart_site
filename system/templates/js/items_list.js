window.addEventListener("DOMContentLoaded", function(){
	var contextmenu_menu = [
		["/system/items/edit", "dan_contextmenu_edit", "Редактировать"],
		["/system/items/pub", "dan_contextmenu_pub", "Включить"],
		["/system/items/unpub", "dan_contextmenu_unpub", "Заблокировать"],
		["/system/items/up", "dan_contextmenu_up", "Вверх"],
		["/system/items/down", "dan_contextmenu_down", "Вниз"],
		["#ITEMS.delete_modal", "dan_contextmenu_delete", "Удалить"]
	];
	DAN.contextmenu.add("contextmenu_menu", contextmenu_menu, "left");
})


ITEMS = {
	delete_modal(obj){
		let id = obj.dataset.id
		let content =
			'<div style="text-align:center;font-size:20px">Удалить тему</div>' +
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
				document.location.href = '/system/items/delete/' + id
			}
		}
	}
}