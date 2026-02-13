"""
Camera with smooth following.
"""
from core.utils import lerp, clamp

class Camera:
    def __init__(self, screen_width, screen_height):
        self.x = 0
        self.y = 0
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.smoothing = 0.1
        self.room_bounds = None
    
    def set_room_bounds(self, bounds):
        self.room_bounds = bounds
    
    def update(self, target_x, target_y, dt):
        target_cam_x = target_x - self.screen_width / 2
        target_cam_y = target_y - self.screen_height / 2
        
        self.x = lerp(self.x, target_cam_x, self.smoothing)
        self.y = lerp(self.y, target_cam_y, self.smoothing)
        
        if self.room_bounds:
            max_x = max(0, self.room_bounds[2] - self.screen_width)
            max_y = max(0, self.room_bounds[3] - self.screen_height)
            self.x = clamp(self.x, self.room_bounds[0], self.room_bounds[0] + max_x)
            self.y = clamp(self.y, self.room_bounds[1], self.room_bounds[1] + max_y)
    
    def world_to_screen(self, world_x, world_y):
        return (world_x - self.x, world_y - self.y)
    
    def screen_to_world(self, screen_x, screen_y):
        return (screen_x + self.x, screen_y + self.y)
