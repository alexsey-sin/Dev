import time
from selenium import webdriver  # $ pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys

# Создание драйвера
EXE_PATH = 'driver/chromedriver.exe'  # Это сам драйвер, лежит уровнем выше в папке driver
driver = webdriver.Chrome(executable_path=EXE_PATH)

# Страница которую разбираем
base_url = 'https://oao.mgts.ru'
# Если на сайте требуется аутентификация на уровне доменного имени
# то логин/пароль вставляем в урл
base_url = f'https://{login}:{password}@oao.mgts.ru'

# Настройка времени ожидания html элементов если их пока нет
driver.implicitly_wait(10)
# Загружаем страницу
driver.get(base_url)
time.sleep(3)


# Преключиться на всплывающее окно alert javascript
driver.switch_to.alert
            element = driver.switch_to.active_element
            alert = driver.switch_to.alert
            driver.switch_to.default_content()
            driver.switch_to.frame('frame_name')
            driver.switch_to.frame(1)
            driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[0])
            driver.switch_to.parent_frame()
            driver.switch_to.window('main')
# Подробнее C:\Users\al-si\AppData\Local\Programs\Python\Python39\Lib\site-packages\selenium\webdriver\remote



# Поиск по названию тега
els = driver.find_elements(By.TAG_NAME, 'li')
# Поиск по id
els = driver.find_elements(By.ID, 'loginform-password')
# Поиск по атрибутам элементов
els = driver.find_elements(By.XPATH, '//div[@class="panel-body"]')
# Так можно взять вложенные дочерние div`ы первого уровня
els = driver.find_elements(By.XPATH, '//div[@class="panel-body"]/div')

# Поиск по вхождению фразы в атрибут элемента
els = driver.find_elements(By.XPATH, '//button[contains(@onclick, "saveManualFlat")]')

# Поиск элементов внутри родительского элемента
els = els_parent.find_elements(By.XPATH, './/button[contains(@onclick, "saveManualFlat")]')

# Взять значение атрибута у элемента
attr = els[0].get_attribute('value')
# Взять значение внутри тэга у элемента
attr = els[0].get_attribute('innerHTML')

# По нормальному тэг svg selenium не находит
els_svg = driver.find_elements(By.XPATH, '//*[local-name() = "svg"]')

# По нескольким свойствам
els_svg = driver.find_elements(By.XPATH, '//*[local-name() = "svg" and (@ng-click="ticket.expandedTicket()")]')
els = driver.find_elements(By.XPATH, '//input[(@id="id_Start") and (@class = "blabla")]')

# Кликнуть мышкой
try: els[0].click()
except: raise Exception('Ошибка клика')

# Ввести слово с клавиатуры (если элемент типа input и это действие допускает)
try: els[0].send_keys('Введенная фраза')
except: raise Exception('Ошибка ввода фразы')

# Имитация стрелок клавиатуры, Enter
from selenium.webdriver.common.keys import Keys
try: els[0].send_keys(Keys.ENTER)       # Keys.ARROW_DOWN
except: raise Exception('Ошибка ENTER')
        els[0].send_keys(Keys.CONTROL + 'a')
        time.sleep(2)
        els[0].send_keys(Keys.DELETE)


# Кликнуть мышкой javascript
# Если Обычным способом чекбокс не отмечается - element not interactable
driver.execute_script("arguments[0].click();", els[0])

# Передвинем страницу чтоб элемент стал видимым
driver.execute_script("arguments[0].scrollIntoView();", els[0])
time.sleep(1)
# прокручивает страницу относительно её текущего положения
driver.execute_script('window.scrollBy(-100, -100)')  # x(по горизонтали), y(по вертикали)
time.sleep(1)

# Перемещение страницы на координаты левого верхнего угла
driver.execute_script('window.scrollTo(-500, 500)')
time.sleep(1)

# Прокрутка страницы до конца
driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')

# Развернуть страницу на весь экран
driver.fullscreen_window()

# Изменить размеры окна
driver.set_window_size(300,800)


# Сохранить содержимое страницы для исследования
#===========
time.sleep(10)
with open('out.html', 'w', encoding='utf-8') as outfile:
    outfile.write(driver.page_source)
raise Exception('Финиш.')
#===========


