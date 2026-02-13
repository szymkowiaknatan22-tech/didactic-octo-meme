"""
Manages all entities (enemies, etc).
"""

class EntityManager:
    def __init__(self):
        self.enemies = []
    
    def add_enemy(self, enemy):
        self.enemies.append(enemy)
    
    def clear(self):
        self.enemies = []
    
    def update(self, dt, player, room, projectile_system):
        for enemy in self.enemies:
            if enemy.alive:
                enemy.update(dt, player, room, projectile_system)
    
    def draw(self, screen, camera):
        for enemy in self.enemies:
            if enemy.alive:
                enemy.draw(screen, camera)
