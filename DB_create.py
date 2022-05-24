import gspread
import psycopg2
import time
#Импортируем курс валюты по ЦБ РФ из отдельного файла
from usdprice import data2
#соединяемся с БД (пароль должен быть такой же, как пароль админа в приложении PostgreSQL)
con = psycopg2.connect(
  database="postgres", 
  user="postgres", 
  password="admin", 
  host="localhost", 
  port="5432"
)
#Создаем таблицу в БД и прописываем имена, аргументы столбцов
print("База данных открыта успешно")
cur = con.cursor()  
cur.execute('''CREATE TABLE PRICES01  
     (ADMISSION INT PRIMARY KEY,
     NUMB TEXT,
     PRICE_USD INT,
     PRICE_DATE DATE,
     PRICE_RUB INT );''')

#Вводим название тестового ключа Google API, который находится в корне нашего проекта
gc = gspread.service_account(filename='pythontest-350820-1b6b67293bb5.json')
#Открываем тестовую таблицу
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1RZtW9uCGkGOykNpfjAYmG4LFv15UHPNBZEg3bLUr2y0/edit#gid=0')
#Открываем нужный нам лист таблицы
worksheet = sh.get_worksheet(0)
#Получаем количество строк для цикла
sheet_len = len(worksheet.col_values(1))


#С помощью цикла заносим данные из таблицы в БД
for i in range(2, sheet_len+1):
    cur = con.cursor()
#Добавляем к извлеченным данным стобец со стоимостью в рублях
    values_rub = worksheet.row_values(i)
    values_rub.append(int(values_rub[2])*data2)
    cur.execute("INSERT INTO PRICES01(ADMISSION, NUMB, PRICE_USD, PRICE_DATE, PRICE_RUB) VALUES(%s, %s, %s, %s, %s)", values_rub)
print("Таблица создана успешно")

#Добавляем бесконечный цикл для обновления таблицы с таймером в 61 сек, чтобы не превышать ограниченное количество запросов к таблице
upd_arg = 1
while upd_arg == 1:
    time.sleep(61)
    print('Обновление...')
    for i in range(2, sheet_len+1):
        cur = con.cursor()
        values_rub = worksheet.row_values(i)
        values_rub.append(int(values_rub[2])*data2)
        cur.execute("UPDATE PRICES01 set ADMISSION = %s where ADMISSION = %s", (values_rub[0], i-1))
        cur.execute("UPDATE PRICES01 set NUMB = %s where ADMISSION = %s", (values_rub[1], i-1))
        cur.execute("UPDATE PRICES01 set PRICE_USD = %s where ADMISSION = %s", (values_rub[2], i-1))
        cur.execute("UPDATE PRICES01 set PRICE_DATE = %s where ADMISSION = %s", (values_rub[3], i-1))
        cur.execute("UPDATE PRICES01 set PRICE_RUB = %s where ADMISSION = %s", (values_rub[4], i-1))
    print("Таблица обновлена успешно")
    con.commit()


con.commit()  
con.close()