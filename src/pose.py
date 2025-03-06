import cv2
import imutils
import numpy as np
import mediapipe as mp
from pyray import *
import yaml

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)


vid1 = cv2.VideoCapture(config['video']['src'])
SCALE=config['window']['scale']
WIDTH = config['window']['width']
HEIGHT = config['window']['height']
STEP_SIZE = config['camera']['step_size']
camera_start = Vector3(*config['camera']['start'])
camera_end = Vector3(*config['camera']['end'])
camera_perpendicular = Vector3(*config['camera']['perpendicular'])
init_window(WIDTH, HEIGHT, "Sticc boii")
set_target_fps(config['window']['fps'])
camera = Camera3D(camera_start,camera_end, camera_perpendicular, config['camera']['fov'], CAMERA_PERSPECTIVE)

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
            if(config['video']['show_src']):
                cv2.imshow("Frame", frame1)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame1)
            result = landmarker.detect_for_video(mp_image, int(vid1.get(cv2.CAP_PROP_POS_MSEC)))
            point_map = {}
            if(result.pose_landmarks):
                for i,p in enumerate(result.pose_landmarks[0]):
                    p.x *= SCALE
                    p.y *= SCALE
                    p.z *= SCALE
                    point_map[i] = Vector3(p.x,p.y,p.z)
                draw_line_3d(Vector3(-1000,0,0), Vector3(1000,0,0), config['window']['x-color'])
                draw_line_3d(Vector3(0,-1000,0), Vector3(0,1000,0), config['window']['y-color'])
                draw_line_3d(Vector3(0,0,-1000), Vector3(0,0,1000), config['window']['z-color'])
                for k in config['ragdoll']['connections']:
                    draw_line_3d(point_map[k[0]],point_map[k[1]],config['ragdoll']['primary-color'])
            end_mode_3d()
            end_drawing()
            if is_key_pressed(KeyboardKey.KEY_W):
                camera.position.z += STEP_SIZE
            if is_key_pressed(KeyboardKey.KEY_A):
                camera.position.x -= STEP_SIZE
            if is_key_pressed(KeyboardKey.KEY_S):
                camera.position.z -= STEP_SIZE
            if is_key_pressed(KeyboardKey.KEY_D):
                camera.position.x += STEP_SIZE
            if is_key_pressed(KeyboardKey.KEY_DOWN):
                camera.position.y -= STEP_SIZE
            if is_key_pressed(KeyboardKey.KEY_UP):
                camera.position.y += STEP_SIZE
            if cv2.waitKey(1) == ord('q'):
                break
            cv2.destroyAllWindows

main()

