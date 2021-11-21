import time
import random
from collections import deque
alarm_report_json = {
    'DATA_TYPE': 'alarm',
    'AGV_NO': 'AGV0001',
    'ALARMS': []
}

alarm_json = {
    'DATA_TYPE': 'alarm',
    'AGV_NO': 'AGV0001',
    'ALARMS': [
        {
            'ALARM_CD': '11',
            'ALARM_DTL': 'Current location is not confirmed',
            'ALARM_STATUS': '0',
            'OCCUR_DT': None,
            'END_DT': None
        },
        {
            'ALARM_CD': '12',
            'ALARM_DTL': 'After going straight, position error',
            'ALARM_STATUS': '0',
            'OCCUR_DT': None,
            'END_DT': None
        },
        {
            'ALARM_CD': '13',
            'ALARM_DTL': 'After turning right 90 degrees, position error',
            'ALARM_STATUS': '0',
            'OCCUR_DT': None,
            'END_DT': None
        },
        {
            'ALARM_CD': '14',
            'ALARM_DTL': 'After turning left 90 degrees, position error',
            'ALARM_STATUS': '0',
            'OCCUR_DT': None,
            'END_DT': None
        },
        {
            'ALARM_CD': '15',
            'ALARM_DTL': 'After 180 degrees of rotation, position error',
            'ALARM_STATUS': '0',
            'OCCUR_DT': None,
            'END_DT': None
        },
        {
            'ALARM_CD': '16',
            'ALARM_DTL': 'After reversing, position error',
            'ALARM_STATUS': '0',
            'OCCUR_DT': None,
            'END_DT': None
        },
        {
            'ALARM_CD': '21',
            'ALARM_DTL': 'LOW BATTERY',
            'ALARM_STATUS': '0',
            'OCCUR_DT': None,
            'END_DT': None
        },
        {
            'ALARM_CD': '22',
            'ALARM_DTL': 'Over-current occurs',
            'ALARM_STATUS': '0',
            'OCCUR_DT': None,
            'END_DT': None
        },
        {
            'ALARM_CD': '31',
            'ALARM_DTL': 'Belt driving failed',
            'ALARM_STATUS': '0',
            'OCCUR_DT': None,
            'END_DT': None
        },
        {
            'ALARM_CD': '32',
            'ALARM_DTL': 'Failed to drive Tray',
            'ALARM_STATUS': '0',
            'OCCUR_DT': None,
            'END_DT': None
        },

    ]
}
# alarm_json['ALARMS'].append(alarm_json['ALARMS'][9])
# print(alarm_json['ALARMS'].pop())
# print(alarm_json['ALARMS'])


async def send_alarm():
    alarm_json['ALARMS'][temp_start_alarm]['ALARM_STATUS'] = 1
    alarm_json['ALARMS'][temp_start_alarm]['OCCUR_DT'] = time.strftime(
        '20%y%m%d %H:%M:%S')
    if(alarm_json['ALARMS'][temp_start_alarm]['END_DT'] is not None):
        alarm_json['ALARMS'][temp_start_alarm]['END_DT'] is None
    if(temp_end_alarm != 10):
        alarm_report_json['ALARMS'].append(
            alarm_json['ALARMS'][temp_end_alarm])
        alarm_json['ALARMS'][temp_end_alarm]['END_DT'] = time.strftime(
            '20%y%m%d %H:%M:%S')
        alarm_json['ALARMS'][temp_end_alarm]['ALARM_STATUS'] = 0

    alarm_report_json['ALARMS'].append(alarm_json['ALARMS'][temp_start_alarm])


ALARM_CD_LIST = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
ALARM_CD_USED = deque([])
temp_end_alarm = 10
temp_start_alarm = 10


def random_alarm():
    global temp_end_alarm, temp_start_alarm
    temp_start_alarm = random.choice(ALARM_CD_LIST)
    ALARM_CD_USED.append(temp_start_alarm)
    ALARM_CD_LIST.remove(temp_start_alarm)
    if(len(ALARM_CD_USED) == 5):
        temp_end_alarm = ALARM_CD_USED.popleft()
        ALARM_CD_LIST.append(temp_end_alarm)


while(True):
    random_alarm()
    send_alarm()
    print(alarm_report_json)
    time.sleep(0.5)
