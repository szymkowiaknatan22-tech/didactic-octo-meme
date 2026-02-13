"""
Heads-up display.
"""
import pygame
from config import *

class HUD:
    def __init__(self):
        self.font = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 20)
    
    def draw(self, screen, player, current_room, floor_data=None):
        # HP bar
        self._draw_hp_bar(screen, player)
        
        # Currency
        currency_text = f"Currency: {player.currency}"
        currency_surf = self.font.render(currency_text, True, COLOR_UI_TEXT)
        screen.blit(currency_surf, (20, 60))
        
        # Artifacts count
        artifacts_text = f"Artifacts: {len(player.artifacts)}"
        artifacts_surf = self.font.render(artifacts_text, True, COLOR_UI_TEXT)
        screen.blit(artifacts_surf, (20, 90))
        
        # Room type
        if current_room:
            room_text = f"Room: {current_room.room_type.name}"
            room_surf = self.font_small.render(room_text, True, COLOR_UI_TEXT)
            screen.blit(room_surf, (20, 120))
        
        # Input mode indicator (top right)
        mode_text = "F1: Click | F2: Auto | F3: IJKL"
        mode_surf = self.font_small.render(mode_text, True, COLOR_UI_TEXT)
        screen.blit(mode_surf, (SCREEN_WIDTH - 300, 20))
        
        # Minimap
        if floor_data:
            self._draw_minimap(screen, floor_data)
    
    def _draw_hp_bar(self, screen, player):
        bar_x = 20
        bar_y = 20
        bar_width = 200
        bar_height = 25
        
        # Background
        pygame.draw.rect(screen, COLOR_HP_BAR_BG, (bar_x, bar_y, bar_width, bar_height))
        
        # HP fill
        hp_ratio = player.hp / player.max_hp
        fill_width = int(bar_width * hp_ratio)
        pygame.draw.rect(screen, COLOR_HP_BAR, (bar_x, bar_y, fill_width, bar_height))
        
        # Border
        pygame.draw.rect(screen, COLOR_UI_TEXT, (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Text
        hp_text = f"{int(player.hp)}/{int(player.max_hp)}"
        hp_surf = self.font.render(hp_text, True, COLOR_UI_TEXT)
        hp_rect = hp_surf.get_rect(center=(bar_x + bar_width // 2, bar_y + bar_height // 2))
        screen.blit(hp_surf, hp_rect)
    
    def _draw_minimap(self, screen, floor_data):
        map_size = 150
        map_x = SCREEN_WIDTH - map_size - 20
        map_y = SCREEN_HEIGHT - map_size - 20
        
        # Background
        pygame.draw.rect(screen, COLOR_UI_BG, (map_x, map_y, map_size, map_size))
        pygame.draw.rect(screen, COLOR_UI_TEXT, (map_x, map_y, map_size, map_size), 2)
        
        rooms = floor_data.get("rooms", {})
        current_pos = floor_data.get("current_pos")
        grid_size = floor_data.get("grid_size", 9)
        
        cell_size = map_size // grid_size
        
        for pos, room in rooms.items():
            x = map_x + pos[0] * cell_size
            y = map_y + pos[1] * cell_size
            
            # Room color based on type
            if pos == current_pos:
                color = COLOR_PLAYER
            elif room.cleared:
                color = (100, 100, 100)
            elif room.room_type.name == "BOSS":
                color = COLOR_BOSS
            elif room.room_type.name == "REWARD":
                color = (255, 215, 0)
            else:
                color = (150, 150, 150)
            
            pygame.draw.rect(screen, color, (x + 2, y + 2, cell_size - 4, cell_size - 4))
            
            # Draw doors
            if room.doors.get("N"):
                pygame.draw.line(screen, color, (x + cell_size // 2, y), (x + cell_size // 2, y + 2), 2)
            if room.doors.get("S"):
                pygame.draw.line(screen, color, (x + cell_size // 2, y + cell_size - 2), 
                               (x + cell_size // 2, y + cell_size), 2)
            if room.doors.get("E"):
                pygame.draw.line(screen, color, (x + cell_size - 2, y + cell_size // 2), 
                               (x + cell_size, y + cell_size // 2), 2)
            if room.doors.get("W"):
                pygame.draw.line(screen, color, (x, y + cell_size // 2), 
                               (x + 2, y + cell_size // 2), 2)
