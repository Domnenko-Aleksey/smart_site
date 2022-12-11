window.addEventListener("DOMContentLoaded", function(){
    DAN.$('start_button').onclick = GG.start;
})

GG = {
    data_url: 'http://77.222.58.99:5000/?key=123&act=get_data&days=',
    start() {
		let content =
			'<div class="modal_title">Получить данные</div>' +
			'<div class="dan_flex_row">' +
                '<div class="modal_tc_l">' +
				    'Данные за последние' + 
                '</div>' +
                '<div class="modal_tc_r">' +
                    '<input id="modal_days" class="dan_input" type="number" name="days" min="1" max="1000" value="30"> &nbsp; дней' +
                '</div>' +
            '</div>' +
			'<div class="center">Пример URL запроса:</div>' +
			'<div id="modal_url">' + GG.data_url + '30</div>' +
			'<div class="dan_flex_row">' +
				'<div style="margin-right:5px">' +
					'<input id="modal_submit" class="dan_button_green" type="submit" name="submit" value="Старт">' +
				'</div>' +
				'<div style="margin-left:5px">' +
					'<input id="modal_cancel" class="dan_button_white" type="submit" name="cancel" value="Отменить">' +
				'</div>' +
			'</div>'
		DAN.modal.add(content, 600)
        DAN.$('modal_days').oninput = GG.get_data_url
		DAN.$('modal_cancel').onclick = DAN.modal.del
		DAN.$('modal_submit').onclick = GG.get_data_ajax
    },


    // Получаем URL ссылки для получения данных
    get_data_url() {
        let days = DAN.$('modal_days').value
        let url = GG.data_url + days
        DAN.$('modal_url').innerHTML = url
        return url
    },


    // Получение данных
    get_data_ajax() {
        let url = GG.get_data_url()
		let form = false;
		DAN.ajax(url, form, (data) => {
            console.log(data)
		})
        DAN.modal.spinner()
    }
}