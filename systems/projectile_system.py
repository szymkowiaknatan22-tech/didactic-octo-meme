"""
Projectile management with object pooling.
"""
import pygame
import math
from config import *
from core.utils import circle_vs_circle, circle_vs_rect

class Projectile:
    def __init__(self):
        self.active = False
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.damage = 0
        self.lifetime = 0
        self.is_player_projectile = False
        self.radius = 4
    
    def spawn(self, x, y, vx, vy, damage, is_player, lifetime=PROJECTILE_LIFETIME):
        self.active = True
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.damage = damage
        self.is_player_projectile = is_player
        self.lifetime = lifetime
    
    def update(self, dt):
        if not self.active:
            return
        
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.lifetime -= dt
        
        if self.lifetime <= 0:
            self.active = False
    
    def on_hit(self):
        self.active = False
    
    def draw(self, screen, camera):
        if not self.active:
            return
        
        screen_x, screen_y = camera.world_to_screen(self.x, self.y)
        color = COLOR_PROJECTILE_PLAYER if self.is_player_projectile else COLOR_PROJECTILE_ENEMY
        pygame.draw.circle(screen, color, (int(screen_x), int(screen_y)), self.radius)


class ProjectileSystem:
    def __init__(self, pool_size=500):
        self.projectiles = [Projectile() for _ in range(pool_size)]
    
    def spawn_projectile(self, x, y, angle, speed, damage, is_player):
        for proj in self.projectiles:
            if not proj.active:
                vx = math.cos(angle) * speed
                vy = math.sin(angle) * speed
                proj.spawn(x, y, vx, vy, damage, is_player)
                return proj
        return None
    
    def update(self, dt):
        for proj in self.projectiles:
            if proj.active:
                proj.update(dt)
    
    def draw(self, screen, camera):
        for proj in self.projectiles:
            if proj.active:
                proj.draw(screen, camera)
    
    def get_active_projectiles(self, is_player=None):
        if is_player is None:
            return [p for p in self.projectiles if p.active]
        return [p for p in self.projectiles if p.active and p.is_player_projectile == is_player]
