from flask import Flask, jsonify, abort
import requests
import psycopg2
import asyncio
import datetime


def db():
    con = psycopg2.connect(user='postgres', password='vladik12345', host='localhost', port='5432',
                           database="postgres_db")
    cursor = con.cursor()

    for i in range(len(courses)):

        item_purchase_time = datetime.datetime.now()

        insert_query = """INSERT INTO courses (id,coin_name, price, time) VALUES ({},{},{},{})""".format(i+1,courses[i]['symbol'], courses[i]['price'],item_purchase_time)
        cursor.execute(insert_query)
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
