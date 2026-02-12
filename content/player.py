"""
Player entity with movement, shooting, and stats.
"""
import pygame
import math
from config import *
from core.utils import circle_vs_rect, normalize

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 12
        self.speed = PLAYER_SPEED
        self.max_hp = PLAYER_MAX_HP
        self.hp = self.max_hp
        self.damage = PLAYER_START_DAMAGE
        self.fire_rate = DEFAULT_FIRE_RATE
        self.projectile_speed = PROJECTILE_SPEED
        self.projectile_count = 1
        self.projectile_spread = 0.1
        self.currency = 0
        self.currency_mult = 1.0
        self.artifacts = []
        self.lifesteal = False
        self.invuln_time = 0
        self.invuln_duration = 0.5
    
    def move(self, dx, dy, dt, room):
        if dx == 0 and dy == 0:
            return
        
        # Normalize diagonal movement
        length = math.sqrt(dx**2 + dy**2)
        if length > 0:
            dx /= length
            dy /= length
        
        # Try moving on X axis
        new_x = self.x + dx * self.speed * dt
        if not self._collides_with_walls(new_x, self.y, room):
            self.x = new_x
        
        # Try moving on Y axis
        new_y = self.y + dy * self.speed * dt
        if not self._collides_with_walls(self.x, new_y, room):
            self.y = new_y
    
    def _collides_with_walls(self, x, y, room):
        for wall in room.walls:
            if circle_vs_rect(x, y, self.radius, wall):
                return True
        return False
    
    def shoot(self, direction, projectile_system):
        if direction is None:
            return
        
        angle = math.atan2(direction[1], direction[0])
        
        if self.projectile_count == 1:
            projectile_system.spawn_projectile(
                self.x, self.y, angle, self.projectile_speed, self.damage, True
            )
        else:
            # Spread multiple projectiles
            half_count = self.projectile_count / 2
            for i in range(self.projectile_count):
                offset = (i - half_count + 0.5) * self.projectile_spread
                proj_angle = angle + offset
                projectile_system.spawn_projectile(
                    self.x, self.y, proj_angle, self.projectile_speed, self.damage, True
                )
    
    def add_artifact(self, artifact):
        self.artifacts.append(artifact)
        artifact.apply(self)
    
    def take_damage(self, amount):
        if self.invuln_time > 0:
            return
        
        self.hp -= amount
        self.invuln_time = self.invuln_duration
        if self.hp <= 0:
            self.hp = 0
    
    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)
    
    def update(self, dt):
        if self.invuln_time > 0:
            self.invuln_time -= dt
    
    def draw(self, screen, camera):
        screen_x, screen_y = camera.world_to_screen(self.x, self.y)
        
        # Draw player with invulnerability flash
        color = COLOR_PLAYER
        if self.invuln_time > 0 and int(self.invuln_time * 20) % 2 == 0:
            color = (255, 255, 255)
        
        pygame.draw.circle(screen, color, (int(screen_x), int(screen_y)), self.radius)
        # Draw direction indicator
        pygame.draw.circle(screen, (255, 255, 255), (int(screen_x), int(screen_y)), 3)
