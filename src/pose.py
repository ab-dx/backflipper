import cv2
import imutils
import numpy as np
import mediapipe as mp
from pyray import *
import yaml
from render import *
from frame_from_csv import *

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)


vid1 = cv2.VideoCapture(config['video']['src'])
WIDTH = config['window']['width']
HEIGHT = config['window']['height']

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode
options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='./models/pose_landmarker_full.task'),
    running_mode=VisionRunningMode.VIDEO)

window = RENDER()
frame_from_csv = FRAME_FROM_CSV()

def main():
    with PoseLandmarker.create_from_options(options) as landmarker:
        while True:
            _, frame1 = vid1.read()
            frame1 = imutils.resize(frame1, width=WIDTH, height=HEIGHT)
            if(config['video']['show_src']):
                cv2.imshow("Frame", frame1)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame1)
            result = landmarker.detect_for_video(mp_image, int(vid1.get(cv2.CAP_PROP_POS_MSEC)))
            window.render_sticc_boi(result.pose_landmarks)

            if cv2.waitKey(1) == ord('q'):
                break
            cv2.destroyAllWindows

def from_csv():
    counter = 0
    window.mark_from_frame(frame_from_csv.get_frame(counter))
    #print(window.point_map)
    while True:
        frame = frame_from_csv.get_frame(counter)
        if(frame == None):
         break
        window.render_sticc_boi_from_frame(frame)
        print("Frame", counter)
        print(frame)
        counter += 1

from_csv()

