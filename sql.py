import sqlite3

#Функция занесения пользователя в базу
def add_to_base (label, counter_type):
    conn = sqlite3.connect('base.db')
    c = conn.cursor()
    c.execute("INSERT INTO base (label, counter_type) VALUES ('%s','%s')" % (label, counter_type))
    conn.commit()
    # Закрываем соединение с базой
    c.close()
    conn.close()

def print_from_base():
    conn = sqlite3.connect('base.db')
    c = conn.cursor()
    c.execute('SELECT * FROM  base')
    row = c.fetchone()
    #Выводим список пользователей в цикле
    while row is not None:
        print("id:"+str(row[0])+" Логин:"+row[1]+" Пароль: "+row[2])
        row = c.fetchone()
    c.close()
    conn.close()


#Вводим данные
label = '123'
counter_type = 'merc'
print('\n')
#Делаем запрос в базу
print("Список пользователей:\n")
add_to_base(label, counter_type)
print_from_base()

