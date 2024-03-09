import os
from dotenv import load_dotenv
import datetime
import time

load_dotenv()

path = os.getenv('path')
number_of_days = os.getenv('number_of_days')
name_of_the_database = os.getenv('name_of_the_database')

current_time = datetime.datetime.now().strftime('%d.%m.%Y_%H:%M:%S')
lower_bound_in_sec = time.time() - float(86400*int(number_of_days))  # бэкапы ниже этой границы удаляются

listdir = os.listdir(path)

for element in listdir:
    dt = datetime.datetime(int(element[6:10]),int(element[3:5]),int(element[0:2]),0,0,0) # Дата из названия файла
    name_of_files_in_sec = time.mktime(dt.timetuple())  # Получаем количество секунд, которому соответствует название файла
    if name_of_files_in_sec < lower_bound_in_sec:       # Если название файла меньше чем нижняя граница, то удаляем бэкап
        os.remove(f'{path}{element}')

string = f"pg_dump --format=custom -v -w {name_of_the_database} > {path}{current_time}.backup 2>{path}{current_time}.log"
# #string = f"pg_restore --clean --dbname=test_db back_up_test.backup" # Строка для восстановления БД
result = os.system(string)

with open('logfile.log', 'a') as file:
    if result == 0:
        file.write(f'Дата:{current_time}. Запись файла {current_time }.backup в каталог {path} Статус: "Успех"\n')
    else:
        file.write(f'{current_time}: Запись файла {current_time}.backup в каталог {path} Статус: "Ошибка". Код ошибки: {result}\n')


