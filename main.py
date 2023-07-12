import time

from flask import Flask, jsonify, abort
import requests
import psycopg2
from threading import Thread
import datetime


def db(courses):

    con = psycopg2.connect(user='postgres', password='vladik12345', database="postgres",host='host.docker.internal')
    cursor = con.cursor()
    insert_query = """ INSERT INTO courses (id, coin_name, price, time)
                                                  VALUES (%s, %s, %s, %s)"""
    update_query = """ UPDATE courses SET price = %s, time = %s WHERE coin_name = %s"""

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


courses = requests.get('https://api.binance.com/api/v3/ticker/price').json()


def scedule():
    while True:
        courses = requests.get('https://api.binance.com/api/v3/ticker/price').json()
        db(courses)
        time.sleep(300)


def site():
    app = Flask(__name__)

    @app.route('/v1/courses', methods=['GET'])
    def get_courses():
        return jsonify({'courses': courses})

    @app.route('/v1/courses/<string:coin_name>', methods=['GET'])
    def get_course(coin_name):
        task = list(filter(lambda t: t['symbol'] == coin_name, courses))
        if len(task) == 0:
            abort(404)
        return jsonify({'course': task[0]})


    app.run(debug=True, use_reloader=False,host='0.0.0.0', port=5000)


if __name__ == '__main__':

    t1 = Thread(target=site,daemon=True)
    t2 = Thread(target=scedule,daemon=True)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
