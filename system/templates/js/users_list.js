window.addEventListener("DOMContentLoaded", function(){
	var contextmenu_menu = [
		["/system/users/edit", "dan_contextmenu_edit", "Редактировать"],
		["/system/projects/add", "dan_contextmenu_add", "Добавить проект"],
		["/system/users/pub", "dan_contextmenu_pub", "Включить"],
		["/system/users/unpub", "dan_contextmenu_unpub", "Заблокировать"],
		["/system/users/up", "dan_contextmenu_up", "Вверх"],
		["/system/users/down", "dan_contextmenu_down", "Вниз"],
		["#USERS.delete_modal", "dan_contextmenu_delete", "Удалить"]
	];
	DAN.contextmenu.add("contextmenu_menu", contextmenu_menu, "left");
})


USERS = {
	delete_modal(obj){
		let id = obj.dataset.id
		let content =
			'<div style="text-align:center;font-size:20px">Удалить пользователя и его проект</div>' +
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
				document.location.href = '/system/users/delete/' + id
			}
		}
	}
}