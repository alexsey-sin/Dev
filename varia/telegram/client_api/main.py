from pyrogram import Client

api_id = 4413039
api_hash = "507813929cf20863405f3db451b88784"

with Client("my_account", api_id, api_hash) as app:
    # Первый параметр метода send_message — id (int) или имя (str) того пользователя,
    # которому будет отправлено сообщение.
    # Зарезервированное слово "me" означает ваш собственный аккаунт.
    app.send_message("me", "Еще раз Привет себе будущему!")