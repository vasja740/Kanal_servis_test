import psycopg2
from usdprice import data2

con = psycopg2.connect(
  database="postgres", 
  user="postgres", 
  password="admin", 
  host="localhost", 
  port="5432"
) 
 
print("БД открыта успешно")
cur = con.cursor()  
cur.execute("SELECT ADMISSION, NUMB, PRICE_USD, PRICE_DATE , PRICE_RUB from PRICES01")

rows = cur.fetchall()  
for row in rows:  
   print("ADMISSION =", row[0])
   print("NUMB =", row[1])
   print("PRICE_USD =", row[2])
   print("COURSE =", row[3])
   print("PRICE_RUB =", row[4], "\n")

print("Извлечение данных прошло успешно")  
con.close()
print(data2)

#Скрипт выводит все данные, но почему-то некоторые измененные строки уходят в середину выведенного списка. К сожалению, не могу найти причину