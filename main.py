import psycopg2

connection = psycopg2.connect(
    host="localhost",
    port=5432,
    user="postgres",
    password="242003",
    database="pg5",
)

cursor = connection.cursor()
def analitic():
    print("Добро пожаловать в меню аналитических запросов. Доступные следющие функции: 1.Показать средний рабочий стаж персонала.")
    choise = int(input("2.Показать наиболее популярный процессор у клиентов. 3.	Узнать наиболее частую критичность проблем клиентов. "))
    if choise == 1:
        cursor.execute("SELECT AVG(stash) FROM worker")
        rows = cursor.fetchone()[0]
        print(rows)
    elif choise == 2:
        cursor.execute("SELECT cpu, count(cpu) as value_cpu FROM complect GROUP BY cpu ORDER BY value_cpu DESC LIMIT 1")
        rows = cursor.fetchone()[0]
        print(rows)
    elif choise == 3:
        cursor.execute("SELECT crutical, count(crutical) as value_crutical FROM defect GROUP BY crutical ORDER BY value_crutical DESC LIMIT 1")
        rows = cursor.fetchone()[0]
        print(rows)
    else:
        print("Неправильный выбор, возврат")
        analitic()
    main()

def view():
    table_name = input("Введите название таблицы: ")
    if table_name == "computer":
        cursor.execute("select id_computer_fk, worker.wio_worker, order_computer.problem, state_computer.critical from computer left join worker on id_worker_fk = id_worker left join order_computer on id_number_fk = number_order left join state_computer on id_state_fk = id_state")
    elif table_name == "worker":
        cursor.execute("select id_worker, fio_worker, stash, date_birthday, job_title.job_name, organization.name_org from worker left join job_title on id_job_fk = id_job left join organization on id_org_fk = id_org")
    else:
        cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    for table in rows:
        print(table)
    print("Возврат в главное меню")
    main()
def add():
    choise = int(input("Добавить данные в таблицу на конкретный столбец - 1 и 2 - если на всех: "))
    table_name = input("Введите название таблцы: ")
    if choise == 1:
        row_name = input("Введите название столбца в который хотите добавить: ")
        value = input("Введите значение данной ячекйки: ")
        if value.isnumeric():
            cursor.execute(f"INSERT INTO {table_name}({row_name}) VALUES ({value})")
        else:
            cursor.execute(f"INSERT INTO {table_name}({row_name}) VALUES ('{value}')")
        connection.commit()
        print("Успешно отправлено")
    elif choise == 2:
        print("Введите данные которые нужно добавить в таблицу в таком формате:")
        print("Каждый новый тип данных должен разделяться запятой, если это текстовый формат то обраляем текст с помощью ''")
        value = input("Введите данные: ")
        cursor.execute(f"INSERT INTO {table_name} VALUES ({value})")
        connection.commit()
        print("Успешно отправлено")
    main()
def redait():
    print("Добро пожаловать в меню редактирования таблиц.")
    table_name = input("Введите название таблцы: ")
    choise = int(input("Выберите 1 если хотите редактировать весь столбец или 2 если хотите редактировать конкретное значение: "))
    if choise == 1:
        value = input("Введите название столбца который хотите редактировать и его значение, пример price=5000,name = 'Олег': ")
        cursor.execute(f"UPDATE {table_name} SET {value}")
        connection.commit()
    elif choise == 2:
        cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
        column_id_name = cursor.fetchone()[0]
        value = input("Введите название столбца который хотите редактировать и его значение, пример price=5000,name = 'Олег': ")
        id_column = int(input("Введите id который хотите изменить: "))
        cursor.execute(f"UPDATE {table_name} SET {value} WHERE {column_id_name} = {id_column}")
        connection.commit()
    print("Успешно")
def delete():
    print("Добро пожаловать в меню удаления записи")
    table_name = input("Введите название таблицы: ")
    #value_table = input("Введите условие удаления, например id = 5: ")
    id_table = input("Введите id записи: ")
    if table_name == "client":
        cursor.execute(f"DELETE FROM complect WHERE id_computer_fk = {id_table}")
        cursor.execute(f"DELETE FROM defect WHERE id_computer_fk = {id_table}")
        cursor.execute(f"DELETE FROM sclad WHERE id_computer_fk = {id_table}")
        cursor.execute(f"DELETE FROM computer WHERE id_computer_fk = {id_table}")
        cursor.execute(f"DELETE FROM client WHERE id_computer = {id_table}")
    elif table_name == "complect":
        cursor.execute(f"DELETE FROM complect WHERE id_computer_fk = {id_table}")
    elif table_name == "sclad":
        cursor.execute(f"DELETE FROM sclad WHERE id_computer_fk = {id_table}")
    elif table_name == "defect":
        cursor.execute(f"DELETE FROM defect WHERE id_computer_fk = {id_table}")
    elif table_name == "job_title":
        cursor.execute(f"DELETE FROM job_title WHERE id_job = {id_table}")
    elif table_name == "order_computer":
        cursor.execute(f"DELETE FROM order_computer WHERE number_order = {id_table}")
    elif table_name == "organization":
        cursor.execute(f"DELETE FROM organization WHERE id_org = {id_table} ")
    elif table_name == "sclad":
        cursor.execute(f"DELETE FROM sclad WHERE id_computer_fk = {id_table}")
    elif table_name == "state_computer":
        cursor.execute(f"DELETE FROM state_computer WHERE id_state = {id_table}")
    elif table_name == "worker":
        cursor.execute(f"DELETE FROM worker WHERE id_worker = {id_table}")
    connection.commit()
    #cursor.execute(f"DELETE FROM {table_name} WHERE {id_table}")
    print("Успешно")
    main()
def main():
    print("Добро пожаловать в панель управления для 6-той лабораторной работе")
    print("Список доступных операций: Посмотреть таблицу = 1, Добавить запись = 2, Редактировать запись = 3, Удалить запись = 4")
    print("Переход в раздел аналитических запросов = 5")
    choise = int(input("Выберите действие: "))
    if choise == 1:
        view()
    elif choise == 2:
        add()
    elif choise == 3:
        redait()
    elif choise == 4:
        delete()
    elif choise == 5:
        analitic()
    else:
        print("Неверное выбран вариант ответа")
        main()


if __name__ == '__main__':
    main()


