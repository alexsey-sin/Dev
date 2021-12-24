import os
import time
import requests
import telegram
import logging
from dotenv import load_dotenv


load_dotenv()
logging.basicConfig(
    level=logging.DEBUG,
    filename='program.log',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)
logger = logging.getLogger(__name__)

PRAKTIKUM_TOKEN = os.getenv('PRAKTIKUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


def parse_homework_status(homework):
    homework_name = homework.get('homework_name')
    status = homework.get('status')
    status_answer = {
        'approved': ('Ревьюеру всё понравилось,'
                     ' можно приступать к следующему уроку.'),
        'rejected': 'К сожалению в работе нашлись ошибки.',
        'reviewing': 'работа находится на проверке'
    }
    if homework_name is None or status not in status_answer:
        return 'Sorry, error parsing.'
    verdict = status_answer[status]
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp):
    try:
        homework_statuses = requests.get(
            'https://praktikum.yandex.ru/api/user_api/homework_statuses/',
            headers={'Authorization': f'OAuth {PRAKTIKUM_TOKEN}'},
            params={'from_date': current_timestamp or int(time.time())}
        )
        # хотя current_timestamp пустой прилететь не может,
        # в main подстраховано
        return homework_statuses.json()
    except requests.exceptions.RequestException:
        logger.error('Error: get_homework_statuses')
        return {}


def send_message(message, bot_client):
    logger.info(message)
    return bot_client.send_message(chat_id=CHAT_ID, text=message)


def main():
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    logger.debug('Бот запущен.')

    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                send_message(
                    parse_homework_status(new_homework.get('homeworks')[0]),
                    bot
                )
            current_timestamp = new_homework.get(
                'current_date',
                current_timestamp
            )
            time.sleep(300)

        except Exception as e:
            message = f'Error: main {e}'
            send_message(message, bot)
            logger.error(message)
            time.sleep(5)


if __name__ == '__main__':
    main()
