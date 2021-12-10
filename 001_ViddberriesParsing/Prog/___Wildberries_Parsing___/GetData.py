import os
from bs4 import BeautifulSoup
ItogFile = r'E:\_006_Python\itog_new.csv'  # Итоговый файл
# DataDir = r'E:\_006_Python\Target' # Папка с файлами для обработки
DataDir = r'E:\_006_Python\Target2' # Папка с файлами для обработки
LogFile = r'E:\_006_Python\log.txt'
ParamsNames = ['Фактура материала', 'Декоративные элементы', 'Возрастная группа', 'Вес с упаковкой (кг)', 'Высота предмета', 'Ширина предмета', 'Ширина упаковки', 'Высота упаковки', 'Глубина упаковки', 'Размер полотенца', 'Назначение полотенца', 'Плотность полотенца', 'Комплектация', 'Страна производитель', 'Спортивное назначение', 'Вес товара без упаковки (г)', 'Повод', 'Количество предметов в упаковке', 'Особенности белья', 'Рисунок', 'Направление', 'Ограничение', 'Назначение подарка', 'Назначение', 'Вес товара с упаковкой (г)']
MAINLINK = 'https://www.wildberries.ru'
ERRORMESSAGE = "-"

# Чтение файла
def GetFileContent(DataDir, FileName):
    FilePath = "%s/%s" % (DataDir, FileName)
    f = open(FilePath, 'r', encoding='utf-8')
    ItsHTML = f.read()
    f.close()
    return ItsHTML

# Очистка данных от мусора
def getClearContent(text):
    text = text.replace("&nbsp", "")
    text = text.replace(";", ",")
    text = text.replace("\r", "")
    text = text.replace("\n", "")
    text = text.replace("₽", "р.")
    text = text.strip()
    return text

# Запись LOG файла
def LogWrite(FileName):
    with open(LogFile, "a") as loglile:
        loglile.write(FileName+"\n")

# :::::::::::::::::::: ПАРСИНГ функции ::::::::::::::::::::
# Адрес обрабатываемой страницы
def GetPageURL(html):
    soup = BeautifulSoup (html, "lxml")
    PageURL = soup.find('link', {'rel' : 'canonical'}).get("href")
    return MAINLINK + PageURL

# Название товара
def GetProductName (html):
    soup = BeautifulSoup(html, "lxml")
    ProductName = soup.find('h1').text
    return getClearContent(ProductName)


# Цвет товара
def GetProductColor (html):
    soup = BeautifulSoup(html, "lxml")
    try:
        ProductColor = soup.find('p', class_='same-part-kt__color').find('span').text
        return ProductColor
    except Exception:
        return ERRORMESSAGE

# Состав товара
def GetProductComposition (html):
    soup = BeautifulSoup(html, "lxml")
    try:
        ProductComposition = soup.find('section', class_='product-detail__details details').find('h2').find_next_sibling().text
        return getClearContent(ProductComposition)
    except Exception:
        return ERRORMESSAGE

# Описание товара
def GetProductDescription (html):
    soup = BeautifulSoup(html, "lxml")
    try:
        ProductDescription = soup.find('div', class_='j-description').text
        return getClearContent(ProductDescription)
    except Exception:
        return ERRORMESSAGE

# Цена товара
def GetProductPrice (html):
    soup = BeautifulSoup(html, "lxml")
    try:
        ProductPrice = soup.find('p', class_='price-block__price-wrap').findAll()
        Price = getClearContent(ProductPrice[0].text)
        return Price
    except Exception:
        return ERRORMESSAGE

# Товар без скидки
def GetProductOldPrice (html):
    soup = BeautifulSoup(html, "lxml")
    try:
        ProductPrice = soup.find('p', class_='price-block__price-wrap').findAll()
        Price = getClearContent(ProductPrice[1].text)
        return Price
    except Exception:
        return ERRORMESSAGE

# Производитель товара
def GetProductProducer (html):
    soup = BeautifulSoup(html, "lxml")
    try:
        ProductProducer = soup.find('a', class_='img-plug').find('img').get('alt')
        return ProductProducer
    except Exception:
        return ERRORMESSAGE

# Расширенные параметры
def GetParamsSet (html):
    soup = BeautifulSoup(html, "lxml")
    ParamsSet = soup.find('table', class_='product-params__table').findAll('tr')
    return ParamsSet

# Выборка прарметров для заполннения таблицы
def Get_parameters(arr, title):
    for key in arr:
        if key[0] == title:
            return key[1]

# :::::::::::::::::::: Основная программа  ::::::::::::::::::::

f = open(ItogFile, 'w+', encoding='windows-1251')
HedaerLine = 'URL;Название1;Название2;Цвет;Состав;Описание;Цена;Старая цена;Производитель;'
HedaerLine += ';'.join(ParamsNames)
HedaerLine += '\r'
f.write(HedaerLine) # Пишем заголовок
SmallCounter = 0
ErrorCounter = 0
with os.scandir(DataDir) as listOfEntries:
    for entry in listOfEntries:
        if entry.is_file(): # Перебор всех записей, являющихся файлами
            SmallCounter += 1
            try:
                mainHTML = str(GetFileContent(DataDir, entry.name))  # Контекст файла
                PageURL = GetPageURL(mainHTML)  # Адрес страницы
                ProductName = GetProductName(mainHTML) # Название товара
                try:
                    PN = ProductName.split(' /  ') # Разбиваем название товара на части
                except Exception:
                    PN[0] = ProductName
                    PN[1] = '-'
                ProductColor = GetProductColor(mainHTML)  # Цвет товара
                ProductComposition = GetProductComposition(mainHTML) # Состав товара
                ProductDescription = GetProductDescription(mainHTML)  # Описание товара
                ProductPrice = GetProductPrice(mainHTML) # Цена товара
                ProductPriceOldPrice = GetProductOldPrice(mainHTML) # Цена товара без скидки
                ProductProducer = GetProductProducer(mainHTML) # Производитель товара
                ParamsSet = GetParamsSet(mainHTML) # Список дополнительных параметров
                # Заполнили список
                FileSource = PageURL + ";" + PN[0] + ";" + PN[1]+ ";" + ProductColor + ";" + ProductComposition + ";" + ProductDescription + ";" + ProductPrice + ";" + ProductPriceOldPrice + ";" + ProductProducer + ";"
                # Дополнительные параметры со страницы
                local_param = []
                for i in range(len(ParamsSet)):
                    local_param.append([getClearContent(ParamsSet[i].find('th').text), getClearContent(ParamsSet[i].find('td').text)])

                for title in ParamsNames:
                    key = Get_parameters(local_param, title)
                    if key:
                        FileSource += str(key) + ";"
                    else:
                        FileSource += '-' + ";"
                FileSource += "\r"  # Закрываем строку
                f.write(FileSource)  # Пишем строку
                print(SmallCounter, "(" + str(ErrorCounter) + ")", entry.name)

            except Exception:
                ErrorCounter += 1
                print(SmallCounter, "("+str(ErrorCounter)+")", entry.name, "Ошибка")
                LogWrite(entry.name)
                continue
f.close()