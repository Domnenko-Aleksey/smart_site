def mainpage(SITE):
    SITE.debug('/pages/mainpage/mainpage.py')

    SITE.addHeadFile('/smart-site/lib/DAN/DAN.css')
    SITE.addHeadFile('/smart-site/lib/DAN/DAN.js')
    SITE.addHeadFile('/smart-site/templates/pages/css/mainpage.css')

    SITE.content = f'''
        <div class="menu">
            <div class="dan_flex_between w1440">
                <div class="menu_left">
                    <div class="menu_left_logo_1">Смарт-сайты</div>
                    <div class="menu_left_logo_2">нейросетевые сайты</div>
                </div>
                <div class="menu_center" style="display:none;">
                    <a class="nav" href="">Главная</a>
                    <a class="nav" href="">Концепция</a>
                    <a class="nav" href="">Контакты</a>
                </div>
                <div class="menu_right">
                    <a href="tel:+79879555554">+7 9879 55555 4</a><br>
                    <a href="mailto:info@63s.ru">info@63s.ru</a>
                </div>
            </div>
        </div>
        <div class="content">
            <div class="main">
                <div class="dan_flex_between w1440">
                    <div>
                        <h1>Концепция сайтов 4 поколения:</h1>                        
						<div class="main_ico_wrap">							
							<div><div class="main_ico"><img alt="" src="/smart-site/templates/pages/svg/code.svg"></div>Использование нейросетей и машинного обучения</div>
							<div><div class="main_ico"><img alt="" src="/smart-site/templates/pages/svg/content.svg"></div>Персонализированный контент</div>
							<div><div class="main_ico"><img alt="" src="/smart-site/templates/pages/svg/computer.svg"></div>Одноэкранное представление</div>
							<div><div class="main_ico"><img alt="" src="/smart-site/templates/pages/svg/microphone.svg"></div>Голосовой интерфейс</div>						
						</div>
                        <div style="padding-bottom:20px">Бот обучен на теме <b>"Создание и продвижение сайта"</b>
                        </div>
                        <div class="dan_flex_row">						
						    <div class="main_button" onclick="DA.set_active()">Попробовать</div>
                            <a href="/smart-site/templates/pages/files/smart-site.pdf" target="blank" class="main_button_ghost">Презентация</a>
                        </div>                       
					</div>
                    <div>
						<img alt="" class="main_image" src="/smart-site/templates/pages/images/seo.png">
						<div class="circle">
						</div>
                    </div>
                </div>
            </div>
		</div>
		<div class="wave_relative">
			<div class="wave_flex wave_absolute"><svg height="100%" width="100%" id="svg" viewBox="0 0 1440 400" xmlns="http://www.w3.org/2000/svg" class="transition duration-300 ease-in-out delay-150"><path d="M 0,400 C 0,400 0,200 0,200 C 93.6267942583732,160.73684210526315 187.2535885167464,121.4736842105263 299,142 C 410.7464114832536,162.5263157894737 540.6124401913876,242.84210526315786 626,244 C 711.3875598086124,245.15789473684214 752.2966507177035,167.15789473684214 837,155 C 921.7033492822965,142.84210526315786 1050.200956937799,196.5263157894737 1158,215 C 1265.799043062201,233.4736842105263 1352.8995215311006,216.73684210526315 1440,200 C 1440,200 1440,400 1440,400 Z" stroke="none" stroke-width="0" fill="#00cba9ff" class="transition-all duration-300 ease-in-out delay-150"></path></svg></div>
			<div class="wave_flex" style="background: transparent;"><svg height="100%" width="100%" id="svg" viewBox="0 0 1440 400" xmlns="http://www.w3.org/2000/svg" class="transition duration-300 ease-in-out delay-150"><path d="M 0,400 C 0,400 0,200 0,200 C 93.6267942583732,160.73684210526315 187.2535885167464,121.4736842105263 299,142 C 410.7464114832536,162.5263157894737 540.6124401913876,242.84210526315786 626,244 C 711.3875598086124,245.15789473684214 752.2966507177035,167.15789473684214 837,155 C 921.7033492822965,142.84210526315786 1050.200956937799,196.5263157894737 1158,215 C 1265.799043062201,233.4736842105263 1352.8995215311006,216.73684210526315 1440,200 C 1440,200 1440,400 1440,400 Z" stroke="none" stroke-width="0" fill="#00cba9ff" class="transition-all duration-300 ease-in-out delay-150"></path><path d="M 0,400 C 0,400 0,200 0,200 C 93.6267942583732,160.73684210526315 187.2535885167464,121.4736842105263 299,142 C 410.7464114832536,162.5263157894737 540.6124401913876,242.84210526315786 626,244 C 711.3875598086124,245.15789473684214 752.2966507177035,167.15789473684214 837,155 C 921.7033492822965,142.84210526315786 1050.200956937799,196.5263157894737 1158,215 C 1265.799043062201,233.4736842105263 1352.8995215311006,216.73684210526315 1440,200 C 1440,200 1440,400 1440,400 Z" stroke="none" stroke-width="0" fill="#00cba9ff" class="transition-all duration-300 ease-in-out delay-150"></path></svg></div>
		</div>
        
    '''
