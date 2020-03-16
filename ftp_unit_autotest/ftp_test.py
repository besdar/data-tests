from ftplib import FTP
from threading import Thread
import os
import os.path
import time
import shutil

test_folder_path = '/home/dmitry/Documents/DINS/'
# создадим подкаталоги для тестов
if not os.path.exists(test_folder_path + 'parallelism/'):
    os.mkdir(test_folder_path + 'parallelism/')
if not os.path.exists(test_folder_path + 'download/'):
    os.mkdir(test_folder_path + 'download/')
if not os.path.exists(test_folder_path + 'upload/'):
    os.mkdir(test_folder_path + 'upload/')
if not os.path.exists(test_folder_path + 'parallelism/download/'):
    os.mkdir(test_folder_path + 'parallelism/download/')
if not os.path.exists(test_folder_path + 'parallelism/upload/'):
    os.mkdir(test_folder_path + 'parallelism/upload/')
# создадим переменные отвечающие за прохождение теста
test1_passed = True
test2_passed = True
test3_passed = True
test4_passed = True

def ftp_connect():
    ftp = FTP(ftp_server_name)
    ftp.login()

def ftp_downloading(num, File_Name, download_count, download_path, ftp_server_name):
    """
    Функция для загрузки файлов на FTP-сервер
    @param File_Name: Имя файла на сервере для загрузки
    @param download_count: Сколько раз зугружать
    @param download_path: Путь к директории на локальной машине куда загружать
    @param ftp_server_name: Имя сервера FTP
    @param ftp_server_name: Номер теста
    """
    os.mkdir(download_path + str(num))
    ftp = FTP(ftp_server_name)
    ftp.login()
    for i in range(download_count):
        with open(download_path + str(num) + '/' + str(i), 'wb') as f:
            ftp.retrbinary('RETR ' + File_Name, f.write)

def ftp_upload(path, upload_count, ftp_server_name):
    """
    Функция для загрузки файлов на FTP-сервер
    @param path: Путь к файлу для загрузки
    @param ftp_server_name: Имя сервера FTP
    @param upload_count: Сколько раз зугружать
    """
    ftp = FTP(ftp_server_name)
    ftp.login()
    ftp.cwd('/upload')
    for i in range(upload_count):
        with open(path, 'rb') as fobj:
            ftp.storbinary('STOR ' + 'newfile', fobj, 1024)

# ==================test 1 ===============
# попытка соединения с сервером фтп
print('Start Test 1...')
try:
    ftp_connect()
except Excepton:
    test1_passed = False

# ==================test 2 ===============
# тестовый случай: простая одиночная загрузка нескольких файлов с сервера
print('Start Test 2...')
try:
    ftp_downloading(0, '10MB.zip', 1, test_folder_path + '/download/', 'speedtest.tele2.net')
    ftp_downloading(1, '100MB.zip', 1, test_folder_path + '/download/', 'speedtest.tele2.net')
    ftp_downloading(2, '1MB.zip', 1, test_folder_path + '//download/', 'speedtest.tele2.net')
    test2_passed = os.path.exists(test_folder_path + '/download/' + '0/0') & os.path.exists(test_folder_path + '/download/' + '1/0') & os.path.exists(test_folder_path + '/download/' + '2/0')
except Exception:
    test2_passed = False

# ==================test 3 ===============
# тестовый случай: простая одиночная загрузка нескольких файлов на сервер
print('Start Test 3...')
if not os.path.exists(test_folder_path + '/upload/10MB.zip') & test1_passed:
    ftp = FTP('speedtest.tele2.net')
    ftp.login()
    with open(test_folder_path + '/upload/10MB.zip', 'wb') as f:
        ftp.retrbinary('RETR ' + '10MB.zip', f.write)
try: # не нашел как получить ответ от сервера что все ок и невозможно посмотреть на файл на сервере т.к. он сразу удаляется, поэтому так
    ftp_upload(test_folder_path + '/upload/10MB.zip', 1, 'speedtest.tele2.net')
    ftp_upload(test_folder_path + '/upload/10MB.zip', 1, 'speedtest.tele2.net')
    ftp_upload(test_folder_path + '/upload/10MB.zip', 1, 'speedtest.tele2.net')
except Exception:
    test3_passed = False

# ==================test 4 ===============
# тестовый случай: файлы должны скачиваться с сервера несколькими пользователями одновременно
print('Start Test 4...')
for i in range(10):
    thread = Thread(target=ftp_downloading, args=(i, '10MB.zip', 2, test_folder_path + 'parallelism/download/', 'speedtest.tele2.net'))
    thread.start()

time.sleep(30) # дождемся завершения параллельных процессов
for i in range(10):
    for j in range(2):
        if not os.path.exists('/home/dmitry/Documents/DINS/parallelism/download/' + str(i) + '/' + str(j)):
            test4_passed = False

# ==================== results ==========================
if test1_passed:
    print('Test 1 passed!')
else:
    print('Test 1 ended with errors!')
if test2_passed:
    print('Test 2 passed!')
else:
    print('Test 2 ended with errors!')
if test3_passed:
    print('Test 3 passed!')
else:
    print('Test 3 ended with errors!')
if test4_passed:
    print('Test 4 passed!')
else:
    print('Test 4 ended with errors!')

# =================== сборка мусора ======================
shutil.rmtree(test_folder_path + 'parallelism/')
shutil.rmtree(test_folder_path + 'download/')
shutil.rmtree(test_folder_path + 'upload/')