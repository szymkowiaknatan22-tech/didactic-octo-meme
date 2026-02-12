"""
Input manager with multiple aim modes for touchpad optimization.
"""
import pygame
import math
from enum import Enum
from config import *
from core.utils import normalize, length, lerp

class AimMode(Enum):
    CURSOR_CLICK = 1  # F1: Move cursor, click to fire
    AUTO_FIRE = 2     # F2: Move cursor, auto-fire
    KEYBOARD_ONLY = 3 # F3: IJKL aim, Space to fire

class InputManager:
    def __init__(self):
        self.aim_mode = AimMode.CURSOR_CLICK
        self.aim_sensitivity = DEFAULT_AIM_SENSITIVITY
        self.aim_smoothing = DEFAULT_AIM_SMOOTHING
        self.deadzone = DEFAULT_DEADZONE
        self.fire_rate = DEFAULT_FIRE_RATE
        self.auto_fire = DEFAULT_AUTO_FIRE
        self.show_crosshair = DEFAULT_SHOW_CROSSHAIR
        self.hide_system_cursor = DEFAULT_HIDE_SYSTEM_CURSOR
        self.relative_mouse = DEFAULT_RELATIVE_MOUSE
        self.precision_modifier = DEFAULT_PRECISION_MODIFIER
        self.crosshair_size = DEFAULT_CROSSHAIR_SIZE
        
        self.cursor_x = SCREEN_WIDTH // 2
        self.cursor_y = SCREEN_HEIGHT // 2
        self.target_cursor_x = self.cursor_x
        self.target_cursor_y = self.cursor_y
        
        self.keyboard_aim_dir = [0, 0]
        self.fire_button_down = False
        self.fire_cooldown = 0
        
        self.last_mouse_pos = pygame.mouse.get_pos()
    
    def set_aim_mode(self, mode):
        self.aim_mode = mode
        if mode == AimMode.CURSOR_CLICK:
            self.auto_fire = False
        elif mode == AimMode.AUTO_FIRE:
            self.auto_fire = True
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                self.set_aim_mode(AimMode.CURSOR_CLICK)
            elif event.key == pygame.K_F2:
                self.set_aim_mode(AimMode.AUTO_FIRE)
            elif event.key == pygame.K_F3:
                self.set_aim_mode(AimMode.KEYBOARD_ONLY)
        
        if self.aim_mode == AimMode.CURSOR_CLICK:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.fire_button_down = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.fire_button_down = False
        elif self.aim_mode == AimMode.KEYBOARD_ONLY:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.fire_button_down = True
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                self.fire_button_down = False
    
    def update(self, dt):
        self.fire_cooldown = max(0, self.fire_cooldown - dt)
        
        if self.aim_mode == AimMode.CURSOR_CLICK or self.aim_mode == AimMode.AUTO_FIRE:
            self._update_cursor_mode(dt)
        elif self.aim_mode == AimMode.KEYBOARD_ONLY:
            self._update_keyboard_mode(dt)
    
    def _update_cursor_mode(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        dx = mouse_pos[0] - self.last_mouse_pos[0]
        dy = mouse_pos[1] - self.last_mouse_pos[1]
        self.last_mouse_pos = mouse_pos
        
        keys = pygame.key.get_pressed()
        precision_active = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        sensitivity = self.aim_sensitivity
        if precision_active:
            sensitivity *= self.precision_modifier
        
        if not self.relative_mouse:
            self.target_cursor_x = mouse_pos[0]
            self.target_cursor_y = mouse_pos[1]
        else:
            move_dist = math.sqrt(dx**2 + dy**2)
            if move_dist > self.deadzone * 0.01:
                self.target_cursor_x += dx * sensitivity
                self.target_cursor_y += dy * sensitivity
        
        self.target_cursor_x = max(0, min(SCREEN_WIDTH, self.target_cursor_x))
        self.target_cursor_y = max(0, min(SCREEN_HEIGHT, self.target_cursor_y))
        
        self.cursor_x = lerp(self.cursor_x, self.target_cursor_x, 1.0 - self.aim_smoothing)
        self.cursor_y = lerp(self.cursor_y, self.target_cursor_y, 1.0 - self.aim_smoothing)
    
    def _update_keyboard_mode(self, dt):
        keys = pygame.key.get_pressed()
        self.keyboard_aim_dir = [0, 0]
        
        if keys[pygame.K_i]:
            self.keyboard_aim_dir[1] -= 1
        if keys[pygame.K_k]:
            self.keyboard_aim_dir[1] += 1
        if keys[pygame.K_j]:
            self.keyboard_aim_dir[0] -= 1
        if keys[pygame.K_l]:
            self.keyboard_aim_dir[0] += 1
        
        if self.keyboard_aim_dir != [0, 0]:
            norm_dir = normalize(self.keyboard_aim_dir)
            self.keyboard_aim_dir = norm_dir
    
    def get_aim_direction(self, player_screen_x, player_screen_y):
        if self.aim_mode == AimMode.KEYBOARD_ONLY:
            if self.keyboard_aim_dir == [0, 0]:
                return None
            return self.keyboard_aim_dir
        else:
            dx = self.cursor_x - player_screen_x
            dy = self.cursor_y - player_screen_y
            dist = math.sqrt(dx**2 + dy**2)
            if dist < 1:
                return None
            return (dx / dist, dy / dist)
    
    def should_fire(self):
        if self.fire_cooldown > 0:
            return False
        
        if self.aim_mode == AimMode.AUTO_FIRE:
            return True
        elif self.aim_mode == AimMode.CURSOR_CLICK or self.aim_mode == AimMode.KEYBOARD_ONLY:
            if self.fire_button_down:
                self.fire_cooldown = 1.0 / self.fire_rate
                return True
        return False
    
    def draw_crosshair(self, screen):
        if not self.show_crosshair:
            return
        
        if self.aim_mode == AimMode.KEYBOARD_ONLY:
            return
        
        size = 10 * self.crosshair_size
        pygame.draw.line(screen, COLOR_CROSSHAIR, 
                        (self.cursor_x - size, self.cursor_y), 
                        (self.cursor_x + size, self.cursor_y), 2)
        pygame.draw.line(screen, COLOR_CROSSHAIR, 
                        (self.cursor_x, self.cursor_y - size), 
                        (self.cursor_x, self.cursor_y + size), 2)
