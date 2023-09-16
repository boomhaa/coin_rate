from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt
from threading import Thread, Lock
from flask import Flask, request, session, jsonify
from models import db, User
import configparser
import psycopg2
import datetime
import requests
import time


class App:
    def __init__(self, courses):
        self.courses = courses
        self.previous = dict()
        self.session = session

    def post_and_update_data_in_db(self, courses):
        db_string = 'postgres://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
        con = psycopg2.connect(db_string)
        cursor = con.cursor()
        insert_query = """ INSERT INTO courses (id,coin_name, price, updated_at) 
        VALUES (%s, %s, %s,%s)
        ON CONFLICT (id) DO UPDATE 
        SET price = %s, 
        updated_at = %s,
        history=%s;"""

        for i in range(len(courses)):

            item_purchase_time = datetime.datetime.now()
            item_tuple = (
                i + 1, courses[i]['symbol'], courses[i]['price'], item_purchase_time, courses[i]['price'],
                item_purchase_time,courses[i]['history'])

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

                for i in range(len(new_courses)):
                    if len(self.previous['courses'][i]['history'])==21:
                        self.previous['courses'][i]['history'].pop(0)
                    self.previous['courses'][i]['history'].append(float(self.courses['courses'][i]['price']))
                    new_courses[i]['history']=self.previous['courses'][i]['history']
                for i in range(len(self.courses['courses'])):
                    try:
                        self.courses['courses'][i]['history']=self.previous['courses'][i]['history']
                    except:
                        pass
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

            time.sleep(10)

    def site(self):
        app = Flask(__name__)
        # Set the secret key to some random bytes. Keep this really secret!
        import secrets
        secret = secrets.token_urlsafe(32)
        app.secret_key = secret
        CORS(app, supports_credentials=True)
        app.config['SESSION_TYPE'] = 'filesystem'
        app.config['SECRET_KEY'] = secret
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskdb.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_ECHO'] = True
        app.config['USE_PERMANENT_SESSION'] = True
        app.config['SESSION_USE_SIGNER'] = True
        app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)

        bcrypt = Bcrypt(app)

        db.init_app(app)
        with app.app_context():
            db.create_all()

        @cross_origin
        @app.route('/v1/courses', methods=['GET'])
        def get_courses():
            return self.courses

        @cross_origin()
        @app.route('/v1/courses/<string:coin_name>', methods=['GET'])
        def get_course(coin_name):
            task = list(filter(lambda t: t['symbol'] == coin_name, self.courses['courses']))
            if len(task) == 0:
                return 'THIS SYMBOL DOES NOT EXIST'
            return task

        @cross_origin
        @app.route("/signup", methods=["POST"])
        def signup():
            email = request.json["email"]
            password = request.json["password"]
            favorite_rates = ""

            user_exists = User.query.filter_by(email=email).first() is not None

            if user_exists:
                return jsonify({"error": "Email already exists"}), 409

            hashed_password = bcrypt.generate_password_hash(password)
            new_user = User(email=email, password=hashed_password, favorite_rates=favorite_rates)
            db.session.add(new_user)
            db.session.commit()

            session["user_id"] = new_user.id

            return jsonify({
                "id": new_user.id,
                "email": new_user.email,
            })

        @cross_origin
        @app.route("/login", methods=["POST"])
        def login_user():

            email = request.json["email"]
            password = request.json["password"]

            user = User.query.filter_by(email=email).first()

            if user is None:
                return jsonify({"error": "Unauthorized Access"}), 401

            if not bcrypt.check_password_hash(user.password, password):
                return jsonify({"error": "Unauthorized"}), 401

            self.session["user_id"] = user.id
            print(self.session)

            return jsonify({
                "id": user.id,
                "email": user.email
            })

        @cross_origin
        @app.route("/favorite_rates", methods=["POST"])
        def favourite_rates():
            favorite_rates = request.json['favorite_rates']
            favorite_rates = ', '.join(favorite_rates)
            user_id = self.session.get('user_id')
            user = User.query.filter_by(id=user_id).first()
            user.favorite_rates = favorite_rates
            db.session.commit()
            return jsonify(
                {
                    "favorite_rates": user.favorite_rates
                }
            )

        @cross_origin
        @app.route('/me', methods=['GET'])
        def get_current_user():

            print(self.session)
            user_id = self.session.get('user_id')
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401
            user = User.query.filter_by(id=user_id).first()
            favourite = list(filter(lambda t:t['symbol'] in user.favorite_rates.split(', '),self.courses['courses']))

            return jsonify({
                "id": user.id,
                "email": user.email,
                "favorite_rates": favourite
            })

        @cross_origin
        @app.route("/logout", methods=["POST"])
        def logout_user():
            self.session.pop("user_id")
            return "200"

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
        if i[4] is not None:
            for j in range(len(i[4])):
                i[4][j]=float(i[4][j])
            coin['history']=i[4]
        else:
            coin['history']=[]
        courses['courses'].append(coin)
    my_app = App(courses)
    t1 = Thread(target=my_app.site, daemon=True)
    t2 = Thread(target=my_app.schedule, daemon=True)
    t1.start()
    t2.start()
    print('все запустилось')
    t1.join()
    t2.join()
