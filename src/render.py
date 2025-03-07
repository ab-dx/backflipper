from pyray import *

import yaml

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

class RENDER:
    def __init__(self):
        
        self.SCALE=config['window']['scale']
        self.WIDTH = config['window']['width']
        self.HEIGHT = config['window']['height']
        self.STEP_SIZE = config['camera']['step_size']
        self.camera_start = Vector3(*config['camera']['start'])
        self.camera_end = Vector3(*config['camera']['end'])
        self.camera_perpendicular = Vector3(*config['camera']['perpendicular'])
        
        
        self.camera = Camera3D(self.camera_start, self.camera_end, self.camera_perpendicular, config['camera']['fov'], CAMERA_PERSPECTIVE)
        
        init_window(self.WIDTH, self.HEIGHT, "Sticc boii")
        set_target_fps(config['window']['fps'])
        
        
    def render_sticc_boi(self, coords):
        """Creates the window that displays the sticcboi

        Args:
            coords (list of tuples): coordinates
        """
        
        begin_drawing()
        clear_background(config['window']['background'])
        begin_mode_3d(self.camera)
        
        self.controller()

        if coords:
            self.mark(coords[0])
            self.draw_lines()
            self.draw_joints(config['ragdoll']['radius'])
            # self.draw_head()
        
        end_mode_3d()
        end_drawing()
        
    def mark(self, coords):
        """makes variable point map and joints

        Args:
            coords (list of tuples): coordinates
            
        """
        self.point_map = {}
        self.joints = set()
        for i,p in enumerate(coords):
            p.x *= self.SCALE
            p.y *= self.SCALE
            p.z *= self.SCALE
            self.point_map[i] = Vector3(p.x,p.y,p.z)
            
        for k in config['ragdoll']['connections']:
            self.joints.add(k[0])
            self.joints.add(k[1])

            
        
    def draw_lines(self):
        """draws axis and connects the joints 
        """
        
        
        #drawing axis  
        draw_line_3d(Vector3(-100,0,0), Vector3(100,0,0), config['window']['x-color'])
        draw_line_3d(Vector3(0,-100,0), Vector3(0,100,0), config['window']['y-color'])
        draw_line_3d(Vector3(0,0,-100), Vector3(0,0,100), config['window']['z-color'])
        
        #drawing the connections
        for k in config['ragdoll']['connections']:
            draw_line_3d(self.point_map[k[0]],self.point_map[k[1]],config['ragdoll']['primary-color'])
    
    def controller(self):
        """
        controls the camera
        """
        if is_key_pressed(KeyboardKey.KEY_W):
            self.camera.position.z += self.STEP_SIZE
        if is_key_pressed(KeyboardKey.KEY_A):
            self.camera.position.x -= self.STEP_SIZE
        if is_key_pressed(KeyboardKey.KEY_S):
            self.camera.position.z -= self.STEP_SIZE
        if is_key_pressed(KeyboardKey.KEY_D):
            self.camera.position.x += self.STEP_SIZE
        if is_key_pressed(KeyboardKey.KEY_DOWN):
            self.camera.position.y -= self.STEP_SIZE
        if is_key_pressed(KeyboardKey.KEY_UP):
            self.camera.position.y += self.STEP_SIZE
            
    def draw_head(self):
        
        radius_vector = vector3_subtract(self.point_map[0], self.point_map[7])
        radius = radius_vector.x**2 + radius_vector.y**2 + radius_vector.z**2
        radius = radius**(1/2)
        draw_sphere(self.point_map[0], radius, config['ragdoll']['secondary-color'])
        
    def draw_joints(self, radius):
        
        for i in self.joints:
            draw_sphere(self.point_map[i], radius, config['ragdoll']['secondary-color'])
