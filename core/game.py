"""
Main game orchestration and state management.
"""
import pygame
import random
import math
from enum import Enum
from config import *
from core.camera import Camera
from core.utils import circle_vs_circle, distance
from systems.input_manager import InputManager
from systems.entity_manager import EntityManager
from systems.projectile_system import ProjectileSystem
from content.player import Player
from content.enemies import Chaser, Shooter, Charger, Splitter
from content.bosses import Sentinel, NexusCore
from content.artifacts import ARTIFACTS
from content.rooms import get_random_layout
from content.floor_generator import FloorGenerator, RoomType
from ui.menu import TitleMenu, PauseMenu, DeathMenu, Button
from ui.hud import HUD
from ui.settings_menu import SettingsMenu

class GameState(Enum):
    TITLE = 1
    PLAYING = 2
    PAUSED = 3
    SETTINGS = 4
    DEAD = 5
    REWARD = 6

class Room:
    def __init__(self, layout, room_type):
        self.layout = layout
        self.room_type = room_type
        self.walls = []
        self.doors = {"N": None, "S": None, "E": None, "W": None}
        self.locked = True
        self.cleared = False
        self._generate_walls()
    
    def _generate_walls(self):
        self.walls = []
        for y in range(len(self.layout)):
            for x in range(len(self.layout[y])):
                if self.layout[y][x] == 1:
                    wall_rect = (
                        x * ROOM_TILE_SIZE,
                        y * ROOM_TILE_SIZE,
                        ROOM_TILE_SIZE,
                        ROOM_TILE_SIZE
                    )
                    self.walls.append(wall_rect)
    
    def set_doors(self, door_config):
        # door_config: {"N": True/False, ...}
        door_positions = {
            "N": (ROOM_WIDTH // 2 * ROOM_TILE_SIZE, 0, ROOM_TILE_SIZE * 3, ROOM_TILE_SIZE),
            "S": (ROOM_WIDTH // 2 * ROOM_TILE_SIZE, (ROOM_HEIGHT - 1) * ROOM_TILE_SIZE, 
                  ROOM_TILE_SIZE * 3, ROOM_TILE_SIZE),
            "E": ((ROOM_WIDTH - 1) * ROOM_TILE_SIZE, ROOM_HEIGHT // 2 * ROOM_TILE_SIZE, 
                  ROOM_TILE_SIZE, ROOM_TILE_SIZE * 3),
            "W": (0, ROOM_HEIGHT // 2 * ROOM_TILE_SIZE, ROOM_TILE_SIZE, ROOM_TILE_SIZE * 3)
        }
        
        for direction, has_door in door_config.items():
            if has_door:
                self.doors[direction] = door_positions[direction]
    
    def unlock(self):
        self.locked = False
    
    def draw(self, screen, camera):
        # Draw floor
        for y in range(ROOM_HEIGHT):
            for x in range(ROOM_WIDTH):
                if self.layout[y][x] == 0:
                    screen_x, screen_y = camera.world_to_screen(
                        x * ROOM_TILE_SIZE, y * ROOM_TILE_SIZE
                    )
                    pygame.draw.rect(screen, COLOR_FLOOR, 
                                   (screen_x, screen_y, ROOM_TILE_SIZE, ROOM_TILE_SIZE))
        
        # Draw walls
        for wall in self.walls:
            screen_x, screen_y = camera.world_to_screen(wall[0], wall[1])
            pygame.draw.rect(screen, COLOR_WALL, 
                           (screen_x, screen_y, wall[2], wall[3]))
        
        # Draw doors
        for direction, door in self.doors.items():
            if door:
                screen_x, screen_y = camera.world_to_screen(door[0], door[1])
                color = COLOR_DOOR_UNLOCKED if not self.locked else COLOR_DOOR_LOCKED
                pygame.draw.rect(screen, color, (screen_x, screen_y, door[2], door[3]))

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.state = GameState.TITLE
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.input_manager = InputManager()
        self.entity_manager = EntityManager()
        self.projectile_system = ProjectileSystem()
        self.hud = HUD()
        
        # Game state
        self.player = None
        self.current_room = None
        self.floor_generator = None
        self.current_floor_pos = None
        
        # Menus
        self.title_menu = TitleMenu(
            on_start=self.start_game,
            on_settings=lambda: self.set_state(GameState.SETTINGS),
            on_quit=self.quit_game
        )
        self.pause_menu = PauseMenu(
            on_resume=lambda: self.set_state(GameState.PLAYING),
            on_settings=lambda: self.set_state(GameState.SETTINGS),
            on_quit=self.return_to_title
        )
        self.death_menu = None
        self.settings_menu = SettingsMenu(
            self.input_manager,
            on_back=self.return_from_settings
        )
        
        # Reward state
        self.reward_choices = []
        self.reward_buttons = []
    
    def set_state(self, state):
        self.state = state
    
    def start_game(self):
        # Initialize new game
        self.floor_generator = FloorGenerator(FLOOR_GRID_SIZE)
        self.floor_generator.generate()
        self.current_floor_pos = self.floor_generator.start_room
        
        # Create player
        spawn_x = ROOM_WIDTH * ROOM_TILE_SIZE // 2
        spawn_y = ROOM_HEIGHT * ROOM_TILE_SIZE // 2
        self.player = Player(spawn_x, spawn_y)
        
        # Load first room
        self.load_room(self.current_floor_pos)
        self.set_state(GameState.PLAYING)
    
    def load_room(self, floor_pos):
        floor_room = self.floor_generator.rooms[floor_pos]
        layout = get_random_layout()
        self.current_room = Room(layout, floor_room.room_type)
        self.current_room.set_doors(floor_room.doors)
        self.current_room.cleared = floor_room.cleared
        
        # Set camera bounds
        bounds = (0, 0, ROOM_WIDTH * ROOM_TILE_SIZE, ROOM_HEIGHT * ROOM_TILE_SIZE)
        self.camera.set_room_bounds(bounds)
        
        # Spawn player at center or appropriate door
        self.player.x = ROOM_WIDTH * ROOM_TILE_SIZE // 2
        self.player.y = ROOM_HEIGHT * ROOM_TILE_SIZE // 2
        
        # Clear entities
        self.entity_manager.clear()
        
        # Spawn enemies if not cleared and not start room
        if not floor_room.cleared and floor_room.room_type in [RoomType.COMBAT, RoomType.BOSS]:
            self._spawn_enemies(floor_room.room_type)
            self.current_room.locked = True
        else:
            self.current_room.locked = False
    
    def _spawn_enemies(self, room_type):
        if room_type == RoomType.BOSS:
            # Spawn boss
            boss_x = ROOM_WIDTH * ROOM_TILE_SIZE // 2
            boss_y = ROOM_HEIGHT * ROOM_TILE_SIZE // 3
            boss = NexusCore(boss_x, boss_y)
            self.entity_manager.add_enemy(boss)
        else:
            # Spawn regular enemies
            num_enemies = random.randint(3, 6)
            for _ in range(num_enemies):
                enemy_type = random.choice([Chaser, Shooter, Charger, Splitter])
                x = random.randint(100, ROOM_WIDTH * ROOM_TILE_SIZE - 100)
                y = random.randint(100, ROOM_HEIGHT * ROOM_TILE_SIZE - 100)
                enemy = enemy_type(x, y)
                
                # Set split callback for splitters
                if isinstance(enemy, Splitter):
                    enemy.split_callback = lambda sx, sy: self._spawn_split(sx, sy)
                
                self.entity_manager.add_enemy(enemy)
    
    def _spawn_split(self, x, y):
        for i in range(2):
            offset_x = random.randint(-30, 30)
            offset_y = random.randint(-30, 30)
            split = Splitter(x + offset_x, y + offset_y, size=1)
            self.entity_manager.add_enemy(split)
    
    def return_to_title(self):
        self.set_state(GameState.TITLE)
    
    def return_from_settings(self):
        if self.player:
            self.set_state(GameState.PLAYING)
        else:
            self.set_state(GameState.TITLE)
    
    def quit_game(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))
    
    def handle_event(self, event):
        if self.state == GameState.TITLE:
            self.title_menu.handle_event(event)
        elif self.state == GameState.PLAYING:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.set_state(GameState.PAUSED)
            else:
                self.input_manager.handle_event(event)
        elif self.state == GameState.PAUSED:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.set_state(GameState.PLAYING)
            else:
                self.pause_menu.handle_event(event)
        elif self.state == GameState.SETTINGS:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.return_from_settings()
            else:
                self.settings_menu.handle_event(event)
        elif self.state == GameState.DEAD:
            if self.death_menu:
                self.death_menu.handle_event(event)
        elif self.state == GameState.REWARD:
            for button in self.reward_buttons:
                button.handle_event(event)
    
    def update(self, dt):
        if self.state == GameState.PLAYING:
            self._update_playing(dt)
        elif self.state == GameState.TITLE:
            pass
        elif self.state == GameState.PAUSED:
            pass
        elif self.state == GameState.SETTINGS:
            pass
        elif self.state == GameState.DEAD:
            pass
        elif self.state == GameState.REWARD:
            pass
    
    def _update_playing(self, dt):
        # Update input
        self.input_manager.update(dt)
        
        # Player movement
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0
        if keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_s]:
            dy += 1
        if keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_d]:
            dx += 1
        
        self.player.move(dx, dy, dt, self.current_room)
        self.player.update(dt)
        
        # Player shooting
        player_screen_x, player_screen_y = self.camera.world_to_screen(
            self.player.x, self.player.y
        )
        aim_dir = self.input_manager.get_aim_direction(player_screen_x, player_screen_y)
        
        if self.input_manager.should_fire() and aim_dir:
            self.player.shoot(aim_dir, self.projectile_system)
        
        # Update entities
        self.entity_manager.update(dt, self.player, self.current_room, self.projectile_system)
        
        # Update projectiles
        self.projectile_system.update(dt)
        
        # Collision detection
        self._handle_collisions()
        
        # Check room clear
        if self.current_room.locked:
            all_dead = all(not e.alive for e in self.entity_manager.enemies)
            if all_dead and len(self.entity_manager.enemies) > 0:
                self.current_room.unlock()
                self.current_room.cleared = True
                floor_room = self.floor_generator.rooms[self.current_floor_pos]
                floor_room.cleared = True
                
                # Show reward if combat room
                if floor_room.room_type == RoomType.COMBAT:
                    self._show_reward_screen()
        
        # Check door transitions
        if not self.current_room.locked:
            self._check_door_transitions()
        
        # Camera follow player
        self.camera.update(self.player.x, self.player.y, dt)
        
        # Check player death
        if self.player.hp <= 0:
            self.death_menu = DeathMenu(
                on_restart=self.start_game,
                on_quit=self.return_to_title
            )
            self.set_state(GameState.DEAD)
    
    def _handle_collisions(self):
        # Player projectiles vs enemies
        for proj in self.projectile_system.get_active_projectiles(is_player=True):
            for enemy in self.entity_manager.enemies:
                if enemy.alive and circle_vs_circle(
                    (proj.x, proj.y), proj.radius,
                    (enemy.x, enemy.y), enemy.radius
                ):
                    enemy.take_damage(proj.damage)
                    proj.on_hit()
                    if not enemy.alive:
                        self.player.currency += int(enemy.currency_value * self.player.currency_mult)
                        if self.player.lifesteal:
                            self.player.heal(1)
                    break
        
        # Enemy projectiles vs player
        for proj in self.projectile_system.get_active_projectiles(is_player=False):
            if circle_vs_circle(
                (proj.x, proj.y), proj.radius,
                (self.player.x, self.player.y), self.player.radius
            ):
                self.player.take_damage(proj.damage)
                proj.on_hit()
        
        # Enemies vs player (melee)
        for enemy in self.entity_manager.enemies:
            if enemy.alive and distance(
                (enemy.x, enemy.y), (self.player.x, self.player.y)
            ) < (enemy.radius + self.player.radius):
                self.player.take_damage(enemy.damage * 0.5)  # Reduced contact damage
    
    def _check_door_transitions(self):
        for direction, door in self.current_room.doors.items():
            if door:
                # Check if player is in door
                player_in_door = (
                    self.player.x > door[0] and
                    self.player.x < door[0] + door[2] and
                    self.player.y > door[1] and
                    self.player.y < door[1] + door[3]
                )
                
                if player_in_door:
                    # Calculate new floor position
                    new_pos = self._get_adjacent_floor_pos(self.current_floor_pos, direction)
                    if new_pos and new_pos in self.floor_generator.rooms:
                        self.current_floor_pos = new_pos
                        self.load_room(new_pos)
                        break
    
    def _get_adjacent_floor_pos(self, pos, direction):
        if direction == "N":
            return (pos[0], pos[1] - 1)
        elif direction == "S":
            return (pos[0], pos[1] + 1)
        elif direction == "E":
            return (pos[0] + 1, pos[1])
        elif direction == "W":
            return (pos[0] - 1, pos[1])
        return None
    
    def _show_reward_screen(self):
        # Choose 3 random artifacts
        self.reward_choices = random.sample(ARTIFACTS, min(3, len(ARTIFACTS)))
        self.reward_buttons = []
        
        center_x = SCREEN_WIDTH // 2
        start_y = SCREEN_HEIGHT // 3
        button_width = 300
        button_height = 80
        spacing = 100
        
        for i, artifact in enumerate(self.reward_choices):
            def make_callback(art):
                return lambda: self._select_artifact(art)
            
            button = Button(
                center_x - button_width // 2,
                start_y + i * spacing,
                button_width,
                button_height,
                artifact.name,
                make_callback(artifact)
            )
            self.reward_buttons.append(button)
        
        self.set_state(GameState.REWARD)
    
    def _select_artifact(self, artifact):
        self.player.add_artifact(artifact)
        self.set_state(GameState.PLAYING)
    
    def draw(self):
        if self.state == GameState.TITLE:
            self.title_menu.draw(self.screen)
        elif self.state == GameState.PLAYING:
            self._draw_playing()
        elif self.state == GameState.PAUSED:
            self._draw_playing()
            self.pause_menu.draw(self.screen)
        elif self.state == GameState.SETTINGS:
            self.settings_menu.draw(self.screen)
        elif self.state == GameState.DEAD:
            if self.death_menu:
                self.death_menu.draw(self.screen, self.player)
        elif self.state == GameState.REWARD:
            self._draw_reward_screen()
    
    def _draw_playing(self):
        self.screen.fill(COLOR_BG)
        
        if self.current_room:
            self.current_room.draw(self.screen, self.camera)
        
        self.entity_manager.draw(self.screen, self.camera)
        self.projectile_system.draw(self.screen, self.camera)
        
        if self.player:
            self.player.draw(self.screen, self.camera)
        
        # HUD
        floor_data = None
        if self.floor_generator:
            floor_data = {
                "rooms": self.floor_generator.rooms,
                "current_pos": self.current_floor_pos,
                "grid_size": self.floor_generator.grid_size
            }
        self.hud.draw(self.screen, self.player, self.current_room, floor_data)
        
        # Crosshair
        self.input_manager.draw_crosshair(self.screen)
    
    def _draw_reward_screen(self):
        self.screen.fill(COLOR_BG)
        
        font = pygame.font.Font(None, 60)
        title = font.render("Choose Your Reward", True, COLOR_UI_TEXT)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        font_small = pygame.font.Font(None, 24)
        for i, (button, artifact) in enumerate(zip(self.reward_buttons, self.reward_choices)):
            button.draw(self.screen)
            
            # Draw description below button
            desc = font_small.render(artifact.description, True, COLOR_UI_TEXT)
            desc_rect = desc.get_rect(center=(button.rect.centerx, button.rect.bottom + 20))
            self.screen.blit(desc, desc_rect)
