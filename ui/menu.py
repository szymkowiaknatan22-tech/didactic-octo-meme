"""
Menu UI components.
"""
import pygame
from config import *

class Button:
    def __init__(self, x, y, width, height, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.hovered = False
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered:
                self.callback()
                return True
        return False
    
    def draw(self, screen):
        color = (80, 80, 100) if self.hovered else (50, 50, 70)
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, COLOR_UI_TEXT, self.rect, 2)
        
        font = pygame.font.Font(None, 32)
        text_surf = font.render(self.text, True, COLOR_UI_TEXT)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)


class TitleMenu:
    def __init__(self, on_start, on_settings, on_quit):
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        button_width = 300
        button_height = 60
        spacing = 80
        
        self.buttons = [
            Button(center_x - button_width // 2, center_y - spacing, 
                   button_width, button_height, "Start Game", on_start),
            Button(center_x - button_width // 2, center_y, 
                   button_width, button_height, "Settings", on_settings),
            Button(center_x - button_width // 2, center_y + spacing, 
                   button_width, button_height, "Quit", on_quit),
        ]
    
    def handle_event(self, event):
        for button in self.buttons:
            if button.handle_event(event):
                return True
        return False
    
    def draw(self, screen):
        screen.fill(COLOR_BG)
        
        # Title
        font = pygame.font.Font(None, 80)
        title_surf = font.render(TITLE, True, COLOR_PLAYER)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(title_surf, title_rect)
        
        # Subtitle
        font_small = pygame.font.Font(None, 32)
        subtitle = font_small.render("A Touchpad-Optimized Roguelike Shooter", True, COLOR_UI_TEXT)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 60))
        screen.blit(subtitle, subtitle_rect)
        
        for button in self.buttons:
            button.draw(screen)


class PauseMenu:
    def __init__(self, on_resume, on_settings, on_quit):
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        button_width = 300
        button_height = 60
        spacing = 80
        
        self.buttons = [
            Button(center_x - button_width // 2, center_y - spacing, 
                   button_width, button_height, "Resume", on_resume),
            Button(center_x - button_width // 2, center_y, 
                   button_width, button_height, "Settings", on_settings),
            Button(center_x - button_width // 2, center_y + spacing, 
                   button_width, button_height, "Quit to Menu", on_quit),
        ]
    
    def handle_event(self, event):
        for button in self.buttons:
            if button.handle_event(event):
                return True
        return False
    
    def draw(self, screen):
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Title
        font = pygame.font.Font(None, 80)
        title_surf = font.render("PAUSED", True, COLOR_UI_TEXT)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(title_surf, title_rect)
        
        for button in self.buttons:
            button.draw(screen)


class DeathMenu:
    def __init__(self, on_restart, on_quit):
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        button_width = 300
        button_height = 60
        spacing = 80
        
        self.buttons = [
            Button(center_x - button_width // 2, center_y + 50, 
                   button_width, button_height, "Try Again", on_restart),
            Button(center_x - button_width // 2, center_y + 50 + spacing, 
                   button_width, button_height, "Quit to Menu", on_quit),
        ]
    
    def handle_event(self, event):
        for button in self.buttons:
            if button.handle_event(event):
                return True
        return False
    
    def draw(self, screen, player):
        screen.fill(COLOR_BG)
        
        # Death message
        font = pygame.font.Font(None, 80)
        title_surf = font.render("YOU DIED", True, (255, 50, 50))
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(title_surf, title_rect)
        
        # Stats
        font_small = pygame.font.Font(None, 36)
        y = SCREEN_HEIGHT // 3 + 80
        
        stats = [
            f"Currency Collected: {player.currency}",
            f"Artifacts: {len(player.artifacts)}",
        ]
        
        for stat in stats:
            stat_surf = font_small.render(stat, True, COLOR_UI_TEXT)
            stat_rect = stat_surf.get_rect(center=(SCREEN_WIDTH // 2, y))
            screen.blit(stat_surf, stat_rect)
            y += 40
        
        for button in self.buttons:
            button.draw(screen)
