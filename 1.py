import psycopg2
from psycopg2 import Error

try:
    # Подключение к существующей базе данных
    connection = psycopg2.connect(user="postgres",
                                  # пароль, который указали при установке PostgreSQL
                                  password="vladik12345",
                                  host="localhost",
                                  port="5432",
                                  database="postgres")

    # Курсор для выполнения операций с базой данных
    cursor = connection.cursor()
    # Распечатать сведения о PostgreSQL
    insert_query = """ SELECT EXISTS(SELECT * FROM courses WHERE coin_name="""+"'ETHBTC'" +""")"""
    cursor.execute(insert_query)
    print(cursor.fetchall())
    connection.commit()

except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")