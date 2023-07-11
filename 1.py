import time
from threading import Thread
from flask import Flask, jsonify, abort
def site():


    app = Flask(__name__)

    @app.route('/v1/courses', methods=['GET'])
    def get_courses():
        return jsonify({'courses': 'p'})
    app.run(debug=True, use_reloader=False)

def f2():
    while True:
        print('ggg')
        time.sleep(5)


if __name__ == '__main__':

    t1 = Thread(target=site,daemon=True)
    t2 = Thread(target=f2,daemon=True)
    t1.start()
    t2.start()
    t1.join()
    t2.join()


