from flask import Flask, jsonify, abort
import requests
import psycopg2
import asyncio
import datetime


def db():
    con = psycopg2.connect(user='postgres', password='vladik12345', host='localhost', port='5432',
                           database="postgres")
    cursor = con.cursor()
    insert_query = """ INSERT INTO courses (id, coin_name, price, time)
                                                  VALUES (%s, %s, %s, %s)"""
    update_query = """ UPDATE courses SET price = %s, time = %s WHERE coin_name = %s"""

    for i in range(len(courses)):

        item_purchase_time = datetime.datetime.now()
        item_tuple = (i + 1, courses[i]['symbol'], courses[i]['price'], item_purchase_time)
        item2 = (courses[i]['price'], item_purchase_time, courses[i]['symbol'])
        checker = '''SELECT EXISTS(SELECT * FROM courses WHERE coin_name = ''' +"'{}'".format(courses[i]['symbol']) +''')'''
        cursor.execute(checker)

        if not cursor.fetchall()[0][0]:
            cursor.execute(insert_query, item_tuple)
        else:
            cursor.execute(update_query,item2)

    con.commit()


app = Flask(__name__)

courses = requests.get('https://api.binance.com/api/v3/ticker/price').json()

db()


@app.route('/v1/courses', methods=['GET'])
def get_courses():
    return jsonify({'courses': courses})


@app.route('/v1/courses/<string:coin_name>', methods=['GET'])
def get_course(coin_name):
    task = list(filter(lambda t: t['symbol'] == coin_name, courses))
    if len(task) == 0:
        abort(404)
    return jsonify({'course': task[0]})


if __name__ == '__main__':
    app.run(debug=True)
