import asyncio
from asyncio.windows_events import NULL
from os import name
import socketio
from flask_socketio import send, emit
import threading
import json
import time
import random
from collections import deque

count = 0
move_data = {
    'DATA_TYPE': None,
    'AGV_NO': None,
    'ACTION': None,
    'BLOCKS': None
}

# 알람
## 본인 디렉토리 위치로 수정
with open('C:/Users/rhd05/OneDrive/바탕 화면/project1-master/Report.json', 'r', encoding='UTF-8') as f:
    test_json = json.load(f)

with open('C:/Users/rhd05/OneDrive/바탕 화면/project1-master/Alarm.json', 'r', encoding='UTF-8') as f:
    alarm_json = json.load(f)

sio = socketio.AsyncClient()

# 알람 전송

ALARM_CD_LIST = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
ALARM_CD_USED = deque([])
temp_end_alarm = 10
temp_start_alarm = 10
alarm_report_json = {
    'DATA_TYPE': 'alarm',
    'AGV_NO': 'AGV0001',
    'ALARMS': []
}
# 랜덤 ALARM_CD
async def random_alarm():
    global temp_end_alarm, temp_start_alarm
    temp_start_alarm = random.choice(ALARM_CD_LIST)
    ALARM_CD_USED.append(temp_start_alarm)
    ALARM_CD_LIST.remove(temp_start_alarm)
    if(len(ALARM_CD_USED) == 5):
        temp_end_alarm = ALARM_CD_USED.popleft()
        ALARM_CD_LIST.append(temp_end_alarm)
    alarm_json['ALARMS'][temp_start_alarm]['ALARM_STATUS'] = 1
    alarm_json['ALARMS'][temp_start_alarm]['OCCUR_DT'] = time.strftime('20%y%m%d %H:%M:%S')
    alarm_json['ALARMS'][temp_start_alarm]['END_DT'] = None
    if(temp_end_alarm != 10):
        alarm_report_json['ALARMS'].append(alarm_json['ALARMS'][temp_end_alarm])
        alarm_json['ALARMS'][temp_end_alarm]['END_DT'] = time.strftime('20%y%m%d %H:%M:%S')
        alarm_json['ALARMS'][temp_end_alarm]['ALARM_STATUS'] = 0
    alarm_report_json['ALARMS'].append(alarm_json['ALARMS'][temp_start_alarm])

async def send_alarm():
    await random_alarm()
    await sio.emit('alarm_report', json.dumps(alarm_report_json, ensure_ascii=False))
    alarm_report_json['ALARMS'] = []
    await asyncio.sleep(0.5)

# connect되면 알람 발생
@sio.event
async def connect():
    while True:
        await send_alarm()

# AGV 상태요청 receive
@sio.on('state_request')
async def state(data):
    json_data = json.loads(data)

    # 상태보고 전송 Thread 시작
    if json_data['DATA_TYPE'] == 'reportRqst':
        await sio.sleep(0.05)

        sio.start_background_task(send_state)

# AGV 상태보고 전송

async def send_state():
    while True:
        await sio.emit('state_report', json.dumps(test_json, ensure_ascii=False))
        await sio.sleep(0.5)

# AGV 이동 명령 receive

@sio.on('move_request')
async def move_avg(data):
    move_data = json.loads(data)
    global count
    await sio.sleep(3)
    test_json['LOCATION'] = move_data['BLOCKS'][count]
    if(count < len(move_data['BLOCKS'])-1):
        count += 1
    print(move_data)

# 서버 연결 해제
@sio.event()
async def disconnect():
    print('disconnected from server')

async def main():
    # local
    await sio.connect('http://127.0.0.1:5000', headers={'AGV_NO': 'AGV00001'})
    # aws ec2
    # await sio.connect('http://13.124.72.207:5000', headers={'AGV_NO': 'AGV00001'})
    await sio.wait()

if __name__ == '__main__':
    asyncio.run(main())
