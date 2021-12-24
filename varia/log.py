import logging

# ваш код здесь
logging.basicConfig(
    level=logging.DEBUG,
    filename='main.log',
    format='%(asctime)s:%(levelname)-8s:%(name)s:%(message)s'
)

log = logging.getLogger(__name__)  # запустили


log.debug('This message should go to the log file')
log.info('So should this')
log.warning('And this, too')

