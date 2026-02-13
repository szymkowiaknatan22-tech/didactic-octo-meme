"""
Enemy archetypes with different behaviors.
"""
import pygame
import math
import random
from config import *
from core.utils import distance, normalize, circle_vs_rect

class Enemy:
    def __init__(self, x, y, hp, damage, speed, color, radius=15):
        self.x = x
        self.y = y
        self.max_hp = hp
        self.hp = hp
        self.damage = damage
        self.speed = speed
        self.color = color
        self.radius = radius
        self.alive = True
        self.currency_value = 5
    
    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.alive = False
    
    def _collides_with_walls(self, x, y, room):
        for wall in room.walls:
            if circle_vs_rect(x, y, self.radius, wall):
                return True
        return False
    
    def update(self, dt, player, room, projectile_system):
        pass
    
    def draw(self, screen, camera):
        screen_x, screen_y = camera.world_to_screen(self.x, self.y)
        pygame.draw.circle(screen, self.color, (int(screen_x), int(screen_y)), self.radius)
        
        # HP bar
        bar_width = self.radius * 2
        bar_height = 4
        bar_x = int(screen_x - bar_width / 2)
        bar_y = int(screen_y - self.radius - 8)
        
        pygame.draw.rect(screen, COLOR_HP_BAR_BG, (bar_x, bar_y, bar_width, bar_height))
        hp_ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, COLOR_HP_BAR, (bar_x, bar_y, int(bar_width * hp_ratio), bar_height))


class Chaser(Enemy):
    """Pursues player directly"""
    def __init__(self, x, y):
        super().__init__(x, y, hp=30, damage=10, speed=100, color=COLOR_ENEMY_CHASER)
        self.currency_value = 5
    
    def update(self, dt, player, room, projectile_system):
        # Move towards player
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.sqrt(dx**2 + dy**2)
        
        if dist > 0.1:
            dx /= dist
            dy /= dist
            
            new_x = self.x + dx * self.speed * dt
            new_y = self.y + dy * self.speed * dt
            
            if not self._collides_with_walls(new_x, self.y, room):
                self.x = new_x
            if not self._collides_with_walls(self.x, new_y, room):
                self.y = new_y


class Shooter(Enemy):
    """Maintains distance and shoots at player"""
    def __init__(self, x, y):
        super().__init__(x, y, hp=20, damage=8, speed=80, color=COLOR_ENEMY_SHOOTER)
        self.shoot_cooldown = 0
        self.shoot_rate = 2.0
        self.min_distance = 200
        self.currency_value = 8
    
    def update(self, dt, player, room, projectile_system):
        self.shoot_cooldown -= dt
        
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.sqrt(dx**2 + dy**2)
        
        # Maintain distance
        if dist > 0.1:
            dx /= dist
            dy /= dist
            
            if dist < self.min_distance:
                # Move away from player
                dx = -dx
                dy = -dy
            
            new_x = self.x + dx * self.speed * dt
            new_y = self.y + dy * self.speed * dt
            
            if not self._collides_with_walls(new_x, self.y, room):
                self.x = new_x
            if not self._collides_with_walls(self.x, new_y, room):
                self.y = new_y
        
        # Shoot at player
        if self.shoot_cooldown <= 0 and dist > 0.1:
            angle = math.atan2(player.y - self.y, player.x - self.x)
            projectile_system.spawn_projectile(
                self.x, self.y, angle, 250, self.damage, False
            )
            self.shoot_cooldown = 1.0 / self.shoot_rate


class Charger(Enemy):
    """Charges at player with telegraph"""
    def __init__(self, x, y):
        super().__init__(x, y, hp=40, damage=15, speed=80, color=COLOR_ENEMY_CHARGER)
        self.state = "idle"  # idle, charging, stunned
        self.charge_cooldown = 0
        self.charge_duration = 0
        self.stun_duration = 0
        self.charge_speed = 400
        self.charge_dx = 0
        self.charge_dy = 0
        self.currency_value = 10
    
    def update(self, dt, player, room, projectile_system):
        if self.state == "idle":
            self.charge_cooldown -= dt
            if self.charge_cooldown <= 0:
                # Start charging
                dx = player.x - self.x
                dy = player.y - self.y
                dist = math.sqrt(dx**2 + dy**2)
                if dist > 0.1:
                    self.charge_dx = dx / dist
                    self.charge_dy = dy / dist
                    self.state = "charging"
                    self.charge_duration = 0.8
                    self.charge_cooldown = 3.0
        
        elif self.state == "charging":
            self.charge_duration -= dt
            
            new_x = self.x + self.charge_dx * self.charge_speed * dt
            new_y = self.y + self.charge_dy * self.charge_speed * dt
            
            if self._collides_with_walls(new_x, new_y, room):
                self.state = "stunned"
                self.stun_duration = 1.0
            else:
                self.x = new_x
                self.y = new_y
            
            if self.charge_duration <= 0:
                self.state = "idle"
        
        elif self.state == "stunned":
            self.stun_duration -= dt
            if self.stun_duration <= 0:
                self.state = "idle"


class Splitter(Enemy):
    """Splits into smaller enemies on death"""
    def __init__(self, x, y, size=2):
        hp = 25 if size == 2 else 10
        radius = 18 if size == 2 else 10
        super().__init__(x, y, hp=hp, damage=8, speed=90, color=COLOR_ENEMY_SPLITTER, radius=radius)
        self.size = size
        self.currency_value = 6 if size == 2 else 3
        self.split_callback = None
    
    def update(self, dt, player, room, projectile_system):
        # Move towards player
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.sqrt(dx**2 + dy**2)
        
        if dist > 0.1:
            dx /= dist
            dy /= dist
            
            new_x = self.x + dx * self.speed * dt
            new_y = self.y + dy * self.speed * dt
            
            if not self._collides_with_walls(new_x, self.y, room):
                self.x = new_x
            if not self._collides_with_walls(self.x, new_y, room):
                self.y = new_y
    
    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.alive = False
            # Split if large size
            if self.size == 2 and self.split_callback:
                self.split_callback(self.x, self.y)
