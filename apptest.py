import random
import time
from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run()


time.strftime('%y%m%d %H:%M:%S')


ALARM_CD_LIST = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

alarm_json['ALARMS'] = alarm_json['ALARMS'][random.choice(ALARM_CD_LIST)]
