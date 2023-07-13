import time

from flask import Flask, jsonify, abort
import requests
import psycopg2
from threading import Thread, Lock
import datetime


def db(courses):
    global new_courses
    db_name = 'postgres'
    db_user = 'postgres'
    db_pass = 'vladik12345'
    db_host = 'db'
    db_port = '5432'
    db_string = 'postgres://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
    con = psycopg2.connect(db_string)
    cursor = con.cursor()

    insert_query = """ INSERT INTO courses (id, coin_name, price, updated_at)
                                                  VALUES (%s, %s, %s, %s)"""
    update_query = """ UPDATE courses SET price = %s, updated_at = %s WHERE coin_name = %s"""

    for i in range(len(courses)):

        item_purchase_time = datetime.datetime.now()
        item_tuple = (i + 1, courses[i]['symbol'], courses[i]['price'], item_purchase_time)
        item2 = (courses[i]['price'], item_purchase_time, courses[i]['symbol'])
        checker = '''SELECT EXISTS(SELECT * FROM courses WHERE coin_name = ''' + "'{}'".format(
            courses[i]['symbol']) + ''')'''
        cursor.execute(checker)

        if not cursor.fetchall()[0][0]:
            cursor.execute(insert_query, item_tuple)
        else:
            cursor.execute(update_query, item2)

    con.commit()
    print('данные обновленны')


def scedule():
    global new_courses
    while True:
        courses = requests.get('https://api.binance.com/api/v3/ticker/price')
        if courses.status_code == 200:
            lock.acquire()
            try:
                new_courses = courses.json()
            finally:
                lock.release()
            db(courses.json())
        time.sleep(300)


def site():
    app = Flask(__name__)

    @app.route('/v1/courses', methods=['GET'])
    def get_courses():
        lock.acquire()
        try:
            return jsonify({'courses': new_courses})
        finally:
            lock.release()

    @app.route('/v1/courses/<string:coin_name>', methods=['GET'])
    def get_course(coin_name):
        lock.acquire()
        try:
            task = list(filter(lambda t: t['symbol'] == coin_name, new_courses))
        finally:
            lock.release()
        if len(task) == 0:
            return 'THIS SYMBOL DOES NOT EXIST'
        return jsonify({'course': task[0]})

    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    lock = Lock()
    new_courses = {'courses': []}
    db_name = 'postgres'
    db_user = 'postgres'
    db_pass = 'vladik12345'
    db_host = 'db'
    db_port = '5432'
    db_string = 'postgres://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
    con = psycopg2.connect(db_string)
    cursor = con.cursor()
    cursor.execute('''SELECT * FROM courses''')
    data = cursor.fetchall()
    data.sort(key=lambda x: x[0])
    for i in data:
        coin = dict()
        coin['symbol'] = str(i[1])
        number = float(i[2])
        coin['price'] = str(f'{number:.10f}')
        new_courses['courses'].append(coin)
    t1 = Thread(target=site, daemon=True)
    t2 = Thread(target=scedule, daemon=True)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
