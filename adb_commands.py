#!/usr/bin/python3

import os

def deviceList():
    result = os.popen('adb devices').read()
    # print(result)
    return result.replace('List of devices attached\n', '').replace('device', '').replace(' ', '').strip('\n')

def recordPerfettoTrace(trace_name, deviceId, config, duration):
    command = 'python .\\record_android_trace --serial ' + deviceId + ' -o ' + trace_name + '.html ' + ' -t ' + duration + ' -c ' + config
    print(command)
    os.popen(command)

def recordPerfettoTrace(trace_name, deviceId, config):
    command = 'python .\\record_android_trace --serial ' + deviceId + ' -o ' + trace_name + '.html ' + '-c ' + config
    print(command)
    os.popen(command)