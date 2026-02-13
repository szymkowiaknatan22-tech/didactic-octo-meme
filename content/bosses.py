"""
Boss enemies with unique patterns.
"""
import pygame
import math
import random
from config import *
from content.enemies import Enemy

class Sentinel(Enemy):
    """Mini-boss with spread shot pattern"""
    def __init__(self, x, y):
        super().__init__(x, y, hp=100, damage=12, speed=60, color=COLOR_BOSS, radius=25)
        self.shoot_cooldown = 0
        self.shoot_rate = 1.5
        self.currency_value = 50
    
    def update(self, dt, player, room, projectile_system):
        self.shoot_cooldown -= dt
        
        # Circle around player
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.sqrt(dx**2 + dy**2)
        
        target_dist = 250
        
        if dist > 0.1:
            # Move in a circle
            angle_to_player = math.atan2(dy, dx)
            perpendicular_angle = angle_to_player + math.pi / 2
            
            move_dx = math.cos(perpendicular_angle) * 0.5
            move_dy = math.sin(perpendicular_angle) * 0.5
            
            # Also maintain distance
            if dist < target_dist - 50:
                move_dx += dx / dist * -0.5
                move_dy += dy / dist * -0.5
            elif dist > target_dist + 50:
                move_dx += dx / dist * 0.5
                move_dy += dy / dist * 0.5
            
            new_x = self.x + move_dx * self.speed * dt
            new_y = self.y + move_dy * self.speed * dt
            
            if not self._collides_with_walls(new_x, self.y, room):
                self.x = new_x
            if not self._collides_with_walls(self.x, new_y, room):
                self.y = new_y
        
        # Shoot spread pattern
        if self.shoot_cooldown <= 0:
            angle = math.atan2(player.y - self.y, player.x - self.x)
            for i in range(5):
                offset = (i - 2) * 0.2
                proj_angle = angle + offset
                projectile_system.spawn_projectile(
                    self.x, self.y, proj_angle, 200, self.damage, False
                )
            self.shoot_cooldown = 1.0 / self.shoot_rate


class NexusCore(Enemy):
    """Final boss with multiple phases"""
    def __init__(self, x, y):
        super().__init__(x, y, hp=300, damage=15, speed=50, color=(255, 0, 0), radius=35)
        self.phase = 1
        self.shoot_cooldown = 0
        self.pattern_timer = 0
        self.currency_value = 100
    
    def update(self, dt, player, room, projectile_system):
        self.shoot_cooldown -= dt
        self.pattern_timer += dt
        
        # Change phase based on HP
        if self.hp < self.max_hp * 0.66 and self.phase == 1:
            self.phase = 2
            self.speed = 70
        elif self.hp < self.max_hp * 0.33 and self.phase == 2:
            self.phase = 3
            self.speed = 90
        
        # Movement
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.sqrt(dx**2 + dy**2)
        
        if dist > 0.1:
            dx /= dist
            dy /= dist
            
            # Slower, more deliberate movement
            new_x = self.x + dx * self.speed * dt * 0.5
            new_y = self.y + dy * self.speed * dt * 0.5
            
            if not self._collides_with_walls(new_x, self.y, room):
                self.x = new_x
            if not self._collides_with_walls(self.x, new_y, room):
                self.y = new_y
        
        # Attack patterns based on phase
        if self.shoot_cooldown <= 0:
            if self.phase == 1:
                self._shoot_circle(projectile_system, 8)
                self.shoot_cooldown = 2.0
            elif self.phase == 2:
                self._shoot_spiral(projectile_system, player)
                self.shoot_cooldown = 1.5
            else:  # phase 3
                self._shoot_rapid(projectile_system, player)
                self.shoot_cooldown = 0.5
    
    def _shoot_circle(self, projectile_system, count):
        for i in range(count):
            angle = (i / count) * math.pi * 2 + self.pattern_timer
            projectile_system.spawn_projectile(
                self.x, self.y, angle, 180, self.damage, False
            )
    
    def _shoot_spiral(self, projectile_system, player):
        for i in range(3):
            angle = math.atan2(player.y - self.y, player.x - self.x) + (i - 1) * 0.3 + self.pattern_timer
            projectile_system.spawn_projectile(
                self.x, self.y, angle, 200, self.damage, False
            )
    
    def _shoot_rapid(self, projectile_system, player):
        angle = math.atan2(player.y - self.y, player.x - self.x)
        projectile_system.spawn_projectile(
            self.x, self.y, angle, 250, self.damage, False
        )
    
    def draw(self, screen, camera):
        screen_x, screen_y = camera.world_to_screen(self.x, self.y)
        
        # Draw differently based on phase
        color = self.color
        if self.phase == 2:
            color = (255, 100, 0)
        elif self.phase == 3:
            color = (255, 200, 0)
        
        pygame.draw.circle(screen, color, (int(screen_x), int(screen_y)), self.radius)
        pygame.draw.circle(screen, (255, 255, 255), (int(screen_x), int(screen_y)), self.radius - 5, 3)
        
        # HP bar
        bar_width = self.radius * 3
        bar_height = 6
        bar_x = int(screen_x - bar_width / 2)
        bar_y = int(screen_y - self.radius - 12)
        
        pygame.draw.rect(screen, COLOR_HP_BAR_BG, (bar_x, bar_y, bar_width, bar_height))
        hp_ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, COLOR_HP_BAR, (bar_x, bar_y, int(bar_width * hp_ratio), bar_height))
