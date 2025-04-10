from pyray import *
import math

# Initialize the window and camera
init_window(800, 600, "3D Line Example")
camera = Camera3D(Vector3(5, 0, 0), Vector3(0, 0, 0), Vector3(0, 1, 0), 90, CAMERA_PERSPECTIVE)

# Define your 3D points (replace with your coordinates)
point_a = Vector3(0, 0, 0)   # Start point (origin)
point_b = Vector3(0, 0, 0)  # End point

set_target_fps(60)
theta = 0
set_target_fps(60)
while not window_should_close():
    begin_drawing()
    clear_background(BLACK)
    theta += 1/180
    begin_mode_3d(camera)
    point_a = Vector3(0, math.sin(theta), math.cos(theta)) 
    point_b = Vector3(0, -math.sin(theta), -math.cos(theta)) 
    # Draw the 3D line between points
    draw_line_3d(point_a, point_b, WHITE,)
    end_mode_3d()

    end_drawing()

close_window()