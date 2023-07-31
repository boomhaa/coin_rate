from flask_cors import CORS, cross_origin
from threading import Thread, Lock
from flask import Flask
import configparser
import psycopg2
import datetime
import requests
import time


class App:
    def __init__(self, courses):
        self.courses = courses
        self.previous = dict()

    def post_and_update_data_in_db(self, courses):
        db_string = 'postgres://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
        con = psycopg2.connect(db_string)
        cursor = con.cursor()
        insert_query = """ INSERT INTO courses (id,coin_name, price, updated_at) 
        VALUES (%s, %s, %s,%s)
        ON CONFLICT (id) DO UPDATE 
        SET price = %s, 
        updated_at = %s;"""

        for i in range(len(courses)):
            item_purchase_time = datetime.datetime.now()
            item_tuple = (
                i + 1, courses[i]['symbol'], courses[i]['price'], item_purchase_time, courses[i]['price'],
                item_purchase_time)
            cursor.execute(insert_query, item_tuple)

        con.commit()
        print('данные обновленны')

    def schedule(self):
        while True:
            self.previous = self.courses
            self.courses = requests.get('https://api.binance.com/api/v3/ticker/price')
            if self.courses.status_code == 200:

                new_courses = self.courses.json()
                self.courses = {'courses': self.courses.json()}
                for i in range(len(self.courses['courses'])):
                    try:
                        if float(self.previous['courses'][i]['price']) - float(self.courses['courses'][i]['price']) > 0:
                            self.courses['courses'][i]['condition'] = 'down'
                        elif float(self.previous['courses'][i]['price']) - float(
                                self.courses['courses'][i]['price']) < 0:
                            self.courses['courses'][i]['condition'] = 'up'
                        else:
                            self.courses['courses'][i]['condition'] = self.previous['courses'][i]['condition']
                    except:
                        pass
                self.post_and_update_data_in_db(new_courses)

            time.sleep(5)

    def site(self):
        app = Flask(__name__, template_folder='html')
        CORS(app)
        app.config['CORS_HEADERS'] = 'Content-Type'

        @cross_origin
        @app.route('/v1/courses', methods=['GET'])
        def get_courses():
            return self.courses

        @app.route('/v1/courses/<string:coin_name>', methods=['GET'])
        def get_course(coin_name):
            task = list(filter(lambda t: t['symbol'] == coin_name, self.courses['courses']))
            if len(task) == 0:
                return 'THIS SYMBOL DOES NOT EXIST'
            return task

        app.run(debug=bool(config['DEFAULT']['debug']), use_reloader=False, port=5000, host='0.0.0.0')


if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read('settings.config')
    lock = Lock()
    courses = {'courses': []}
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
        coin['condition'] = 'normal'
        courses['courses'].append(coin)
    my_app = App(courses)
    t1 = Thread(target=my_app.site, daemon=True)
    t2 = Thread(target=my_app.schedule, daemon=True)
    t1.start()
    t2.start()
    print('все запустилось')
    t1.join()
    t2.join()
