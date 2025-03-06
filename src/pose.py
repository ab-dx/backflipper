import cv2
import imutils
import numpy as np
import mediapipe as mp
from pyray import *
import yaml

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)


vid1 = cv2.VideoCapture(0)
SCALE=config['window']['scale']
WIDTH = config['window']['width']
HEIGHT = config['window']['height']
init_window(WIDTH, HEIGHT, "Sticc boii")
set_target_fps(config['window']['fps'])
camera = Camera3D(config['camera']['start'],config['camera']['end'], config['camera']['perpendicular'], config['camera']['fov'], CAMERA_PERSPECTIVE)

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode
options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='./models/pose_landmarker_full.task'),
    running_mode=VisionRunningMode.VIDEO)

def main():
    with PoseLandmarker.create_from_options(options) as landmarker:
        while True:
            begin_drawing()
            clear_background(config['window']['background'])
            _, frame1 = vid1.read()
            frame1 = imutils.resize(frame1, width=WIDTH, height=HEIGHT)
            begin_mode_3d(camera)
            cv2.imshow("Frame", frame1)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame1)
            result = landmarker.detect_for_video(mp_image, int(vid1.get(cv2.CAP_PROP_POS_MSEC)))
            #result = vid1.get(cv2.CAP_PROP_POS_MSEC)
            #pprint.pp(result.pose_landmarks[0])
            point_map = {}
            #connections = [(11,13),(13,15),(12,14),(14,16),(11,12),(24,23),(12,24),(11,23),(24,26),(23,25)]
            for i,p in enumerate(result.pose_landmarks[0]):
                p.x *= SCALE
                p.y *= SCALE
                p.z *= SCALE
                point_map[i] = Vector3(p.x,p.y,p.z)
                if(i==11):
                    print("11:", p.x,p.y,p.z)
                if(i==23):
                    print("23:", p.x,p.y,p.z)
            draw_line_3d(Vector3(-100,0,0), Vector3(100,0,0), config['window']['x-color'])
            draw_line_3d(Vector3(0,-100,0), Vector3(0,100,0), config['window']['y-color'])
            draw_line_3d(Vector3(0,0,-100), Vector3(0,0,100), config['window']['z-color'])
            for k in config['ragdoll']['connections']:
                draw_line_3d(point_map[k[0]],point_map[k[1]],WHITE)
            #            draw_sphere(Vector3(0,0,0), 2, BLUE)
            end_mode_3d()
            end_drawing()
            if cv2.waitKey(1) == ord('q'):
                break
            cv2.destroyAllWindows

main()

