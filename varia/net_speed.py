'''
Если вдруг захотелось измерить скорость интернета.
То это очень легко сделать в Питоне с помощью библиотеке
speedtest-cli 2.1.2 которая работает с известным сайтом
SpeedTest.Net

Устанавливаем библиотеку :
pip install speedtest-cli
'''
import speedtest
import time

try:
    start_time = time.time()
    test = speedtest.Speedtest()
    download = test.download()
    upload = test.upload()
    down = (download/1024)/1024
    upp = (upload/1024)/1024
    execution_time = round(time.time() - start_time, 1)

    print('Download speed: {:0.2f} Mb/s'.format(down))
    print('Upload speed: {:0.2f} Mb/s'.format(upp))
    print(f'Test time: {execution_time} sec.')
    
except speedtest.ConfigRetrievalError:
    print('Error connect.')
