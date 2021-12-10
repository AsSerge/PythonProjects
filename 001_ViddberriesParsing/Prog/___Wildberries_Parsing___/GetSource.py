# Получаем данные для скраппинга
# DataFile = r'E:\_006_Python\Source\list.csv' # Список страниц со страницами
# DataFile = r'E:\_006_Python\Source\list_31818.csv' # Список страниц со страницами
DataFile = r'E:\_006_Python\Source\list_ERROR.csv' # Список страниц со страницами
# DataDir = r'E:\_006_Python\Target'
DataDir = r'E:\_006_Python\Target2'
LogFile = r'E:\_006_Python\log.txt'

import csv
import time
import requests
# proxies = {"https":"https://z00m_serge_gmail_com:0e15791926@91.212.51.168:30001"} # Данные для авторизации на прокси
# proxies = {"https":"https://z00mserge:c5v5PiRUsk@192.144.18.63:49155"} # Данные для авторизации на прокси
proxies = {"https":"https://z00mserge:c5v5PiRUsk@94.45.182.66:49155"} # Данные для авторизации на прокси

from fake_useragent import UserAgent
ua = UserAgent() # Фэйковый юзер-агент

# ФУНКЦИЯ Создание файла
def CreateFile(DataDir, FileName, FileSource):
    FilePath = "%s\%s" % (DataDir, FileName)
    f = open(FilePath, 'w+', encoding='utf-8')
    f.write(FileSource)
    f.close()

# ФУНКЦИЯ Получние информации
def GetUrlSource(Url, Headers, proxies):
    r = requests.get(Url, headers=Headers, proxies=proxies)
    return r.text

# ФУНКЦИЯ записи в лог текущей позиции
def SendToLog(number, logFile):
    with open(logFile, 'w+') as LogFile:
        LogFile.write(number)

# Главная функция
logKey = 1
with open(DataFile, newline='') as File:
    reader = csv.reader(File)
    for row in reader:
        try:
            Headers = {'user-agent': ua.random} # Фэйковый юзер-агент (подключение к запросу)
            num = ''.join(row)
            num = num.split(';')
            FileName = num[0]+".html" # Имя файла
            FileContent = GetUrlSource(num[1], Headers, proxies) # Содержимое файла
            CreateFile(DataDir, FileName, FileContent) # Создание файла
            print(logKey, num[0])
            SendToLog(str(logKey) + ":[success]" + str(num[0]), LogFile) # Запись в лог
            logKey += 1
            time.sleep(2)
        except Exception:
            print(logKey, num[0], 'error')
            SendToLog(str(logKey) + ":[error]" + str(num[0]), LogFile) # Запись в лог
            logKey += 1
            continue