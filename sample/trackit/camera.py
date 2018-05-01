import os
import time
from threading import Thread
import base64

import cv2
import requests
import json
from threading import Thread


CAM_NAME = 'cam1'
FUNC_ID = 5
TARGET = '7LEU552'
video_capture = cv2.VideoCapture(0)

GATEWAY = os.environ.get('GATEWAY', 'http://localhost:5001')

if video_capture.isOpened():
    ret, frame = video_capture.read()
else:
    ret = False

count = 0
while ret:
    cv2.imshow('webcam', frame)
    ret, frame = video_capture.read()
    key = cv2.waitKey(25)
    if key == 27: # exit on ESC
        break
    ret, buff = cv2.imencode('.jpg', frame)

    files = {'upload_file': buff.tobytes()}
    filename = '{0}_frame{1}.jpg'.format(CAM_NAME, count)
    argv = [CAM_NAME, filename, TARGET]

    requests.post('{0}/upload/{1}'.format(GATEWAY, filename,), files=files)
    resp = requests.post('{0}/tasks/'.format(GATEWAY,), json={'id': FUNC_ID, 'argv': argv})

    js = json.loads(resp.text)
    if 'found' in js['ret']:
        print(js['ret'])
        break
    count += 1

cv2.destroyWindow("preview")
video_capture.release()
