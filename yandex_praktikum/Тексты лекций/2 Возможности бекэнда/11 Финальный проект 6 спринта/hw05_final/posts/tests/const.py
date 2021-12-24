T_TEXT = 'Тестовый текст'
AUTHOR_NAME = 'user_writer'
USER_NAME = 'user_BigBag'
USER_NAME2 = 'user_LittleBag'
T_PASSWORD = 'test_password'

TEST_GIF = (
    b'\x47\x49\x46\x38\x39\x61\x02\x00'
    b'\x01\x00\x80\x00\x00\x00\x00\x00'
    b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
    b'\x00\x00\x00\x2C\x00\x00\x00\x00'
    b'\x02\x00\x01\x00\x00\x02\x02\x0C'
    b'\x0A\x00\x3B'
)
GROUP_NOTE = {
    'title': 'Рассказ',
    'slug': 'story',
    'description': 'Рассказ любого содержания',
}
GROUP_STORY = {
    'title': 'Заметки',
    'slug': 'note',
    'description': 'Небольшие заметки любого содержания',
}
GROUP_MODEL = {
    'title': 'ж' * 200,
    'slug': 'model',
    'description': 'Небольшие заметки любого содержания',
}
LOAD_FILE = {
    'name': 'test.gif',
    'content': TEST_GIF,
    'content_type': 'image/gif'
}
LOAD_FILE2 = {
    'name': 'test2.gif',
    'content': TEST_GIF,
    'content_type': 'image/gif'
}
FIELD_VERBOSE = {
    'title': 'Заголовок',
    'slug': 'Адрес',
    'description': 'Описание',
}
FIELD_HELP_TEXTS = {
    'title': 'Дайте короткое название группе',
    'slug': 'Укажите адрес для страницы группы',
    'description': 'Укажите краткое описание группы',
}
