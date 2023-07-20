import time
from flask import Flask
from flask_cors import CORS,cross_origin
import requests
import psycopg2
from threading import Thread, Lock
import datetime
import configparser


def post_and_update_data_in_db(courses):
    db_string = 'postgres://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
    con = psycopg2.connect(db_string)
    cursor = con.cursor()
    insert_query = """ INSERT INTO courses (id,coin_name, price, updated_at) 
    VALUES (%s, %s, %s,%s)
    ON CONFLICT (id) DO UPDATE 
    SET price = %s, 
    updated_at = %s"""

    for i in range(len(courses)):
        item_purchase_time = datetime.datetime.now()
        item_tuple = (
            i + 1, courses[i]['symbol'], courses[i]['price'], item_purchase_time, courses[i]['price'],
            item_purchase_time)
        cursor.execute(insert_query, item_tuple)

    con.commit()
    print('данные обновленны')


def scedule():

    while True:
        courses = requests.get('https://api.binance.com/api/v3/ticker/price')
        if courses.status_code == 200:
            lock.acquire()
            try:
                new_courses = courses.json()
            finally:
                lock.release()
            post_and_update_data_in_db(new_courses)
        time.sleep(300)


def site():
    app = Flask(__name__, template_folder='html')
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    @cross_origin
    @app.route('/v1/courses', methods=['GET'])
    def get_courses():
        lock.acquire()
        try:
            data_courses = new_courses

        finally:
            lock.release()
        return data_courses

    @app.route('/v1/courses/<string:coin_name>', methods=['GET'])
    def get_course(coin_name):
        lock.acquire()
        try:
            task = list(filter(lambda t: t['symbol'] == coin_name, new_courses))
        finally:
            lock.release()
        if len(task) == 0:
            return 'THIS SYMBOL DOES NOT EXIST'
        return task

    app.run(debug=bool(config['DEFAULT']['debug']), use_reloader=False, port=5000,host='0.0.0.0')


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('settings.config')
    lock = Lock()
    new_courses = {'courses': []}
    db_name = config['DEFAULT']['db_name']
    db_user = config['DEFAULT']['db_user']
    db_pass = config['DEFAULT']['db_pass']
    db_host = config['DEFAULT']['db_host']
    db_port = int(config['DEFAULT']['db_port'])
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
    print('все запустилось')
    t1.join()
    t2.join()
