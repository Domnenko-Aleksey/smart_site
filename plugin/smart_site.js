window.addEventListener('DOMContentLoaded', function(){
	DA.init()
});

DA = {
	domain: 'xn----7sbb0blzeehe.xn--p1ai',
	url_get_title: '/api/get_title_ajax',  // Получаем заголовок / проверка на работу системы
	url_id_answer: '/api/get_id_answer_ajax',  // Получаем ответ для текста
	url_spech_answer: '/api/get_speech_answer_ajax',  // Получаем ответ для текста
	url_fav_get: '/api/get_fav_ajax',  // Получаем данные favorites на ajax
	url_fav_set: '/api/set_fav_ajax',  // Отправка данных favorites на ajax
	title: '',
	first_start: true,
	open_icon: false,  // Иконка "открыть - закрыть"
	right: false,  // Правый блок
	speech_out: false,  // Вывод ответа
	mic_icon: false,  // Иконка микрофона
	check_icon: false,  // Иконка check
	speak_icon: false,  // Иконка динамика
	speak_icon_src: false,
	icons: {
		'arrow': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M13.025 1l-2.847 2.828 6.176 6.176h-16.354v3.992h16.354l-6.176 6.176 2.847 2.828 10.975-11z"/></svg>',
		'audio': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M6 7l8-5v20l-8-5v-10zm-6 10h4v-10h-4v10zm20.264-13.264l-1.497 1.497c1.847 1.783 2.983 4.157 2.983 6.767 0 2.61-1.135 4.984-2.983 6.766l1.498 1.498c2.305-2.153 3.735-5.055 3.735-8.264s-1.43-6.11-3.736-8.264zm-.489 8.264c0-2.084-.915-3.967-2.384-5.391l-1.503 1.503c1.011 1.049 1.637 2.401 1.637 3.888 0 1.488-.623 2.841-1.634 3.891l1.503 1.503c1.468-1.424 2.381-3.309 2.381-5.394z"/></svg>',
		'audio_off': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M22 1.269l-18.455 22.731-1.545-1.269 3.841-4.731h-1.827v-10h4.986v6.091l2.014-2.463v-3.628l5.365-2.981 4.076-5.019 1.545 1.269zm-10.986 15.926v.805l8.986 5v-16.873l-8.986 11.068z"/></svg>',
		'check': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M9 21.035l-9-8.638 2.791-2.87 6.156 5.874 12.21-12.436 2.843 2.817z"/></svg>',
		'microphone': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M16 10c0 2.209-1.791 4-4 4s-4-1.791-4-4v-6c0-2.209 1.791-4 4-4s4 1.791 4 4v6zm4-2v2c0 4.418-3.582 8-8 8s-8-3.582-8-8v-2h2v2c0 3.309 2.691 6 6 6s6-2.691 6-6v-2h2zm-7 13.03v-2.03h-2v2.03c-2.282.139-4 .744-4 1.47 0 .829 2.238 1.5 5 1.5s5-.671 5-1.5c0-.726-1.718-1.331-4-1.47z"/></svg>',
		'pause': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M11 22h-4v-20h4v20zm6-20h-4v20h4v-20z"/></svg>'
	},


	// Инициализация
	init() {
		// Получение заголовка. Если получен ответ - запускаем скрипт
		DA.get_title(function() {
			DA.url_id_answer = 'https://' + DA.domain + DA.url_id_answer
			DA.url_spech_answer = 'https://' + DA.domain + DA.url_spech_answer
			DA.url_fav_get = 'https://' + DA.domain + DA.url_fav_get
			DA.url_fav_set = 'https://' + DA.domain + DA.url_fav_set
	
			let link = DA.load_css()  // Подгружает css файл
			link.onload = () => {
				DA.create_tab()  // Создаёт вкладку
				DA.fav_init()  // Инициализация списка "Избранное"
			}
		});
	},


	// Получение заголовка
	get_title(callback) {
		let form = new FormData()
		form.append('domain', location.host)
		let url = 'https://' + DA.domain + DA.url_get_title
		DA.ajax(url, form, function(data) {
			console.log(data)
			DA.title = data.title
			callback()
		})
	},


	// Загружает стили
	load_css() {
		var head  = document.getElementsByTagName('head')[0];
		var link  = document.createElement('link');
		link.rel  = 'stylesheet';
		link.type = 'text/css';
		link.href = 'https://xn----7sbb0blzeehe.xn--p1ai/plugin/smart_site.css';
		link.media = 'all';
		head.appendChild(link);
		return link
	},


	// Инициализация списка фавориты
	fav_init() {
		DA.check_icon.classList.remove('active')
		let fav_item_arr = document.getElementsByClassName('da_fav_item')
		let fav_del = document.getElementsByClassName('da_fav_del')

		for (i=0; i<fav_item_arr.length; i++) {
			fav_item_arr[i].onclick = function(){
				DA.get_id_answer_ajax(this.id)
			}
			fav_del[i].onclick = function(e){
				this.parentNode.remove()
				e.stopPropagation()
				DA.send_favorites()
			}
		}
	},


	// Создаёт вкладку
	create_tab() {
		let tab =
		'<div id="da">' +
			'<div id="da_left">' +
				'<div id="da_open_icon">' + DA.icons.microphone + '</div>' +
				'<div id="da_speech_container">' +
					'<div class="da_speech_wrap da_w1440">' +
						'<div id="da_mic_icon" class="da_speech_icon">' + DA.icons.microphone + '</div>' +
						'<div id="da_check_icon" class="da_speech_icon">' + DA.icons.check + '</div>' +
						'<div id="da_speak_icon" class="da_speech_icon active">' + DA.icons.audio + '</div>' +
						'<div id="da_speech_out">' + DA.title + '</div>' +
					'</div>' +
				'</div>' +
				'<div class="da_answer_container da_w1440">' +
					'<div id="da_answer_content"></div>' +
				'</div>' +
			'</div>' +
			'<div id="da_right">' +
			'</div>'
		'</div>'
		document.body.insertAdjacentHTML('afterBegin', tab)

		DA.open_icon = document.getElementById('da_open_icon')
		DA.right = document.getElementById('da_right')
		DA.speech_out = document.getElementById('da_speech_out')
		DA.mic_icon = document.getElementById('da_mic_icon')
		DA.check_icon = document.getElementById('da_check_icon')
		DA.speak_icon = document.getElementById('da_speak_icon')

		DA.open_icon.onclick = DA.set_active  // Активная или выключенная вкладка
		DA.mic_icon.onclick = DA.mic_on_off  // Включение / выключение микрофона
		DA.check_icon.onclick = DA.set_favorites  // Добавить / удалить из избранного
		DA.speak_icon.onclick = DA.synth_on_off  // Включить / отключить синтез речи
	},


	// Устанавливает активное состояние вкладки
	set_active() {
		// Первое открытие вкладки
		if (DA.first_start) {
			DA.get_favorites()
			DA.first_start = false
		}
		
		let main_container = document.getElementById('da')
		DA.open_icon.classList.toggle('active')
		main_container.classList.toggle('active')

		let node_open_icon = document.getElementById('da_open_icon')

		if (DA.open_icon.classList.contains('active')) {
			node_open_icon.innerHTML = DA.icons.arrow
			DA.speech.recognize_start()  // Распознавание
		} else {
			node_open_icon.innerHTML = DA.icons.microphone
			DA.speech.recognize_stop()
			DA.speech.synthesis_stop()
		}
	},


	// Включение / выключение микрофона
	mic_on_off() {
		if (DA.mic_icon.classList.contains('active')) {
			DA.speech.sr_on = false
			DA.speech.recognize_stop()
		} else {
			DA.speech.sr_on = true
			DA.speech.recognize_start()			
		}
	},


	// Включение / отключение синтеза речи
	synth_on_off() {
		if (da_speak_icon.classList.contains('active')) {
			DA.speech.synthesis_stop()
		} else {
			DA.speech.synthesis_start()
		}
	},


	// Добавить избранное
	set_favorites() {
		DA.check_icon.classList.add('active')
		let da_answer = document.getElementById('da_answer')
		if (da_answer) {
			let f_id = 'f_' + da_answer.dataset.id

			let fav_items = document.getElementById('da_right').getElementsByClassName('da_fav_item')
			// Проверяем, не добавлен ли ответ ранее в избранное
			for (let i = 0; i < fav_items.length; i++) {
				// Удаляем узел, т.к. добавляем его ниже на первую строку
				if (fav_items[i].id == f_id) {
					fav_items[i].remove()
				}
			}

			let speech_text = DA.speech_out.innerHTML
			let fav_content = DA.set_favorites_html(f_id, speech_text)
			DA.right.insertAdjacentHTML('afterbegin', fav_content)
		}

		DA.send_favorites()
		DA.fav_init()
	},


	// Устанавливает html код для избранного 
	set_favorites_html(f_id, text) {
		return '<div id="' + f_id + '" class="da_fav_item"><span class="da_fav_item_text">' + text + '</span><span class="da_fav_del">&#10006;</span></div>'
	},


	// Отправка списка favorites на ajax, установка кук
	send_favorites() {
		// --- Cookie ---
		let ss_cid = ''
		if (document.cookie.indexOf("ss_cid") != -1) {
			// Куки найдены, ищем значение. Регулярное выражение для поиска
			let re = new RegExp("ss_cid=([a-z0-9]{32})");
			ss_cid = re.exec(document.cookie)[1]
		}

		let form = new FormData()
		let questions = []
		let ids = []
		let fav_container = document.getElementById('da_right')
		let fav_items = fav_container.getElementsByClassName('da_fav_item')
		let fav_items_text = fav_container.getElementsByClassName('da_fav_item_text')
		for (let i = 0; i < fav_items.length; i++) {
			questions.push(fav_items_text[i].innerHTML)
			let id = fav_items[i].id.replace('f_', '')
			ids.push(id);
		}
		form.append('domain', location.host)
		form.append('ss_cid', ss_cid)
		form.append('questions', questions)
		form.append('ids', ids)
		DA.ajax(DA.url_fav_set, form, function(data){
			console.log('--- SET FAV AJAX ---')
		})
	},


	// Получить закладки "избранное"
	get_favorites() {
		// Получаем куки (если есть)
		let ss_cid = ''
		if (document.cookie.indexOf("ss_cid") != -1) {
			// Куки найдены, ищем значение. Регулярное выражение для поиска
			let re = new RegExp("ss_cid=([a-z0-9]{32})");
			ss_cid = re.exec(document.cookie)[1]
		}

		let form = new FormData()
		form.append('domain', location.host)
		form.append('ss_cid', ss_cid)

		DA.ajax(DA.url_fav_get, form, function(data) {
			console.log('--- GET FAV AJAX ---', data)

			// Ставим куки, если data.ss_cid_new - не пустое
			if (data.ss_cid_new != '')
				document.cookie = "ss_cid=" + data.ss_cid_new + "; path=/; expires=Tue, 20 Jan 2030 01:01:01 GMT"

			for (var id in data.favorites) {
				let fav_html = DA.set_favorites_html('f_'+id, data.favorites[id])
				DA.right.insertAdjacentHTML('beforeend', fav_html)
			}
			DA.fav_init()
		})
	},


	// Получаем ответ на ajax
	get_speech_answer_ajax(speech_text, id=false) {
		console.log('SPEECH:', speech_text)
		speech_text = speech_text.charAt(0).toUpperCase() + speech_text.substring(1)  // Первая буква - заглавная
		DA.speech_out.innerHTML = speech_text

		// Получаем куки (если есть)
		let ss_cid = ''
		if (document.cookie.indexOf("ss_cid") != -1) {
			// Куки найдены, ищем значение. Регулярное выражение для поиска
			let re = new RegExp("ss_cid=([a-z0-9]{32})");
			ss_cid = re.exec(document.cookie)[1]
		}

		let form = new FormData()
		form.append('domain', location.host)
		form.append('speech_text', speech_text)
		form.append('ss_cid', ss_cid)

		// Отправка данных на ajax
		DA.ajax(DA.url_spech_answer, form, function(data) {
			// Ставим куки, если data.ss_cid_new - не пустое
			if (data.ss_cid_new != '')
				document.cookie = "ss_cid=" + data.ss_cid_new + "; path=/; expires=Tue, 20 Jan 2030 01:01:01 GMT"
			document.getElementById('da_answer_content').innerHTML = data.answer_content
			DA.check_icon.classList.remove('active')
			DA.show('da_image', 'da_images_container')  // Инициируем show	
			if (DA.speech.sn_on) {
				DA.speech.synthesis_start(data.answer_synthesis)
			}
		})
	},


	// Получаем ответ на ajax
	get_id_answer_ajax(f_id) {
		let form = new FormData()
		let id = f_id.replace('f_', '')
		form.append('domain', location.host)
		form.append('id', id)

		// Отправка данных на ajax
		DA.ajax(DA.url_id_answer, form, function(data){
			document.getElementById('da_answer_content').innerHTML = data.answer_content
			DA.check_icon.classList.remove('active')
			DA.show('da_image', 'da_images_container')  // Инициируем show	
			if (DA.speech.sn_on) {
				DA.speech.synthesis_start(data.answer_synthesis)
			}
		})
	}
}



// --- SPEECH ---
DA.speech = {
    sr: false,  // Объект SpeechRecognition
	sn: false,  // Объект синтеза речи
	sr_on: true,  // Вкл / выкл прослушивани, более высокий приоритет, чем у sr_on
	sn_on: true,  // Вкл / выкл синтеза, более высокий приоритет, чем у sr_on


	// Старт распознавания речи
    recognize_start(){
        if (window.speechSynthesis == undefined) {
            alert('Чтение речи не поддерживается в данном браузере')
			return
        }

		if (!DA.speech.sr) {
			DA.speech.sr = new (window.SpeechRecognition || window.webkitSpeechRecognition || window.mozSpeechRecognition || window.msSpeechRecognition)();
			DA.speech.sr.lang = "ru-RU";
		}
		
		DA.mic_icon.classList.add('active')  // Кнопка микрофона - активная
		DA.speech.sr_on = true
		DA.speech.sr.start()

        DA.speech.sr.onresult = function(event){
            let speech_text = event.results[0][0].transcript;
			DA.get_speech_answer_ajax(speech_text)
        };

        DA.speech.sr.onend = () => {
            if (DA.speech.sr_on)
                DA.speech.sr.start()
        };
    },


    // Голосовое воспроизведение
    synthesis_start(text){
		DA.speech.sr.abort()  // Останавливаем предыдущее воспроизведение
		
		DA.speech.sn_on = true;
		DA.speak_icon.classList.add('active')		
		DA.speak_icon.innerHTML = DA.icons.audio

		DA.speech.sn = window.speechSynthesis
		DA.speech.recognize_stop()

        // voices = window.speechSynthesis.getVoices()
        // console.log(voices)  // Доступные голоса

        // Воспроизведение
        let utterance = new SpeechSynthesisUtterance(text);
        DA.speech.sn.speak(utterance);

		utterance.onend = () => {
			if (DA.open_icon.classList.contains('active'))
				DA.speech.recognize_start()
		}
    },


	// Остановка распознавания
	recognize_stop() {
		DA.speech.sr_on = false
		DA.speech.sr.abort()
		DA.mic_icon.classList.remove('active')  // Кнопка микрофона - пассивная
	},
	
	
	// Остановка распознавания
	recognize_stop() {
		DA.speech.sr_on = false
		DA.speech.sr.abort()
		DA.mic_icon.classList.remove('active')  // Кнопка микрофона - пассивная
	},


	// Остановка синтеза речи
	synthesis_stop() {
		DA.speech.sn_on = false
		if(DA.speech.sn)
			DA.speech.sn.cancel()
		DA.speak_icon.classList.remove('active')
		DA.speak_icon.innerHTML = DA.icons.audio_off				
	}
}


// --- AJAX ---
DA.ajax = function(url, form=false, callback){
	let req = new XMLHttpRequest()

	req.onreadystatechange = ()=>{
		if (req.readyState == 4 && req.status == 200) {
			let data = JSON.parse(req.responseText)
			if (data.answer == 'success')
				callback(data)
			else
				alert(data.message)
		}
	}

	req.open('post', url, true);
	req.send(form)
}


// --- SHOW ---
DA.show = function(_class, _id){
	if (!document.getElementById(_id))
		return

	let obj = new DA_show(_class, _id)
	run (obj)

	function run() {
		for (let i = 0; i < obj.sum; i++) {
			obj.img_arr[i].style.cursor = 'url(https://xn----7sbb0blzeehe.xn--p1ai/smart-site/templates/plugin/images/lupa.png), auto'

			obj.img_arr[i].onclick = (e)=>{
				// Останавливаем распознавание и синтез
				DA.speech.recognize_stop()
				DA.speech.synthesis_stop()

				// Создаём модальное окно
				if (!obj.bg) {
					// Чёрный фон
					obj.bg = document.createElement('div')
					obj.bg.id = 'da_show_black'
					document.body.insertBefore(obj.bg, document.body.children[0])

					obj.bg.onclick = function(){
						obj.del()
						obj.bg = false
						obj.image = false
					}
				}

				obj.output(e.target)
				obj.image.onclick = function(e){		
					e.stopPropagation()
				}				

				document.getElementById('da_show_nav_left').onclick = (e)=>{
					e.stopPropagation()
					obj.stop()
					obj.prev()
				}
				
				document.getElementById('da_show_nav_play').onclick = (e)=>{
					e.stopPropagation()				
			
					play('button')

					function play (_but = false){ // _but == true -> анимация запущена кнопкой, false - автоматом по циклу
						// Кнопка play / stop
						if(_but == 'button'){
							if(!obj.timer){
								document.getElementById('da_show_nav_play').removeChild(document.getElementById('da_show_nav_play').lastChild)
								document.getElementById('da_show_nav_play').insertAdjacentHTML('afterbegin', '<svg class="da_show_nav"><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="https://xn----7sbb0blzeehe.xn--p1ai/smart-site/templates/plugin/svg/sprite.svg#pause"></use></svg>')
							}
							else{						
								obj.stop()
								return
							}
						}

						obj.next()
						obj.timer = setTimeout(function(){
							requestAnimationFrame(play)
						}, obj.interval)
					}				
				}
				
				document.getElementById('da_show_nav_right').onclick = (e)=>{
					e.stopPropagation()
					obj.stop()
					obj.next()
				}	
			}
		}
	}
}


// Класс для DA.show()
class DA_show{
	constructor(_class, _id){
		this.container = document.getElementById(_id) // Контейнет
		this.img_arr = this.container.getElementsByClassName(_class) // Массив изображений в контейнере
		this.sum = this.img_arr.length // Количество изображений
		this.bg = false // Фон с затемнением
		this.wrap = false  // Оболочка
		this.image = false // Текущее большое изображение
		this.interval = 2000 // Интервал анимации
		this.nav_play = false // Кнопка навигации
		this.num = false // Текущий индекс массива изображений
		this.timer = false // Номер таймера
	}

	output(img){
		// Изображение
		let img_out = document.createElement('img')
		img_out.src = img.src
		img_out.id = 'da_show_image'

		for (let i = 0; i < this.sum; i++) {
		    if (typeof this.img_arr[i] == 'undefined')
		        continue

			if (img.src == this.img_arr[i].src)
				this.num = i
		}

		// Обёртка
		this.wrap = document.createElement('div')
		this.wrap.id = 'da_show_wrap'
		this.bg.insertAdjacentElement('afterbegin', this.wrap)

		// Изображение
		this.image = this.wrap.insertAdjacentElement('afterbegin', img_out)

		// Навигация
		let cross = document.createElement('div')
		cross.id = 'da_show_cross'
		cross.innerHTML = '<svg><use xlink:href="https://xn----7sbb0blzeehe.xn--p1ai/smart-site/templates/plugin/svg/sprite.svg#delete"></use></svg>'
		this.wrap.insertAdjacentElement('afterbegin', cross)

		let nav_left = document.createElement('div')
		nav_left.id = 'da_show_nav_left'
		this.wrap.insertAdjacentElement('afterbegin', nav_left)
		nav_left.insertAdjacentHTML('afterbegin', '<svg class="da_show_nav"><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="https://xn----7sbb0blzeehe.xn--p1ai/smart-site/templates/plugin/svg/sprite.svg#prev"></use></svg>')

		let nav_right = document.createElement('div')
		nav_right.id = 'da_show_nav_right'
		this.wrap.insertAdjacentElement('beforeend', nav_right)
		nav_right.insertAdjacentHTML('afterbegin', '<svg class="da_show_nav"><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="https://xn----7sbb0blzeehe.xn--p1ai/smart-site/templates/plugin/svg/sprite.svg#next"></use></svg>')

		let nav_play = document.createElement('div')
		nav_play.id = 'da_show_nav_play'
		this.wrap.insertAdjacentElement('afterbegin', nav_play)
		nav_play.insertAdjacentHTML('afterbegin', '<svg class="da_show_nav"><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="https://xn----7sbb0blzeehe.xn--p1ai/smart-site/templates/plugin/svg/sprite.svg#play"></use></svg>')		
	}
	
	prev(){
		this.num--
		if(this.num < 0) this.num = this.img_arr.length - 1
		this.image.src = this.img_arr[this.num].src
	}

	next(){	
		this.num++
		if(this.num > (this.sum - 1)) this.num = 0
		this.image.src = this.img_arr[this.num].src		
	}

	stop(){
		document.getElementById('da_show_nav_play').removeChild(document.getElementById('da_show_nav_play').lastChild)
		document.getElementById('da_show_nav_play').insertAdjacentHTML('afterbegin', '<svg class="da_show_nav"><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="https://xn----7sbb0blzeehe.xn--p1ai/smart-site/templates/plugin/svg/sprite.svg#play"></use></svg>')		
		clearTimeout(this.timer)
		this.timer = false
	}

	del(e){
		this.stop()
		document.body.removeChild(document.getElementById('da_show_black'))
	}
}