"""
Settings menu with sliders and toggles.
"""
import pygame
from config import *

class Slider:
    def __init__(self, x, y, width, label, min_val, max_val, initial_val, callback):
        self.rect = pygame.Rect(x, y, width, 20)
        self.label = label
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.callback = callback
        self.dragging = False
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self._update_value(event.pos[0])
                return True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging:
                self.dragging = False
                return True
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self._update_value(event.pos[0])
                return True
        return False
    
    def _update_value(self, mouse_x):
        relative = (mouse_x - self.rect.x) / self.rect.width
        relative = max(0, min(1, relative))
        self.value = self.min_val + (self.max_val - self.min_val) * relative
        self.callback(self.value)
    
    def draw(self, screen):
        font = pygame.font.Font(None, 24)
        
        # Label
        label_surf = font.render(self.label, True, COLOR_UI_TEXT)
        screen.blit(label_surf, (self.rect.x, self.rect.y - 25))
        
        # Slider track
        pygame.draw.rect(screen, (70, 70, 80), self.rect)
        pygame.draw.rect(screen, COLOR_UI_TEXT, self.rect, 1)
        
        # Slider handle
        relative = (self.value - self.min_val) / (self.max_val - self.min_val)
        handle_x = self.rect.x + int(relative * self.rect.width)
        handle_rect = pygame.Rect(handle_x - 5, self.rect.y - 5, 10, 30)
        pygame.draw.rect(screen, COLOR_PLAYER, handle_rect)
        
        # Value text
        value_text = f"{self.value:.2f}" if isinstance(self.value, float) else str(self.value)
        value_surf = font.render(value_text, True, COLOR_UI_TEXT)
        screen.blit(value_surf, (self.rect.x + self.rect.width + 10, self.rect.y - 5))


class Toggle:
    def __init__(self, x, y, label, initial_val, callback):
        self.rect = pygame.Rect(x, y, 40, 25)
        self.label = label
        self.value = initial_val
        self.callback = callback
        self.hovered = False
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered:
                self.value = not self.value
                self.callback(self.value)
                return True
        return False
    
    def draw(self, screen):
        font = pygame.font.Font(None, 24)
        
        # Label
        label_surf = font.render(self.label, True, COLOR_UI_TEXT)
        screen.blit(label_surf, (self.rect.x, self.rect.y - 25))
        
        # Toggle box
        color = COLOR_PLAYER if self.value else (70, 70, 80)
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, COLOR_UI_TEXT, self.rect, 2)
        
        # State text
        state_text = "ON" if self.value else "OFF"
        state_surf = font.render(state_text, True, COLOR_UI_TEXT)
        state_rect = state_surf.get_rect(center=self.rect.center)
        screen.blit(state_surf, state_rect)


class SettingsMenu:
    def __init__(self, input_manager, on_back):
        self.input_manager = input_manager
        self.on_back = on_back
        
        start_x = 200
        start_y = 150
        spacing_y = 80
        slider_width = 300
        
        self.controls = []
        
        # Sliders
        self.controls.append(Slider(
            start_x, start_y, slider_width,
            "Aim Sensitivity", 0.1, 3.0, input_manager.aim_sensitivity,
            lambda v: setattr(input_manager, 'aim_sensitivity', v)
        ))
        
        self.controls.append(Slider(
            start_x, start_y + spacing_y, slider_width,
            "Aim Smoothing", 0.0, 0.9, input_manager.aim_smoothing,
            lambda v: setattr(input_manager, 'aim_smoothing', v)
        ))
        
        self.controls.append(Slider(
            start_x, start_y + spacing_y * 2, slider_width,
            "Deadzone", 0, 100, input_manager.deadzone,
            lambda v: setattr(input_manager, 'deadzone', int(v))
        ))
        
        self.controls.append(Slider(
            start_x, start_y + spacing_y * 3, slider_width,
            "Fire Rate", 1.0, 20.0, input_manager.fire_rate,
            lambda v: setattr(input_manager, 'fire_rate', v)
        ))
        
        self.controls.append(Slider(
            start_x, start_y + spacing_y * 4, slider_width,
            "Precision Modifier", 0.1, 1.0, input_manager.precision_modifier,
            lambda v: setattr(input_manager, 'precision_modifier', v)
        ))
        
        # Toggles
        toggle_x = start_x + 400
        self.controls.append(Toggle(
            toggle_x, start_y,
            "Show Crosshair", input_manager.show_crosshair,
            lambda v: setattr(input_manager, 'show_crosshair', v)
        ))
        
        self.controls.append(Toggle(
            toggle_x, start_y + spacing_y,
            "Hide System Cursor", input_manager.hide_system_cursor,
            lambda v: (setattr(input_manager, 'hide_system_cursor', v), pygame.mouse.set_visible(not v))
        ))
        
        self.controls.append(Toggle(
            toggle_x, start_y + spacing_y * 2,
            "Relative Mouse", input_manager.relative_mouse,
            lambda v: setattr(input_manager, 'relative_mouse', v)
        ))
        
        # Back button
        from ui.menu import Button
        self.back_button = Button(
            SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 100,
            300, 50, "Back", on_back
        )
    
    def handle_event(self, event):
        for control in self.controls:
            if control.handle_event(event):
                return True
        return self.back_button.handle_event(event)
    
    def draw(self, screen):
        screen.fill(COLOR_BG)
        
        # Title
        font = pygame.font.Font(None, 60)
        title_surf = font.render("Settings", True, COLOR_UI_TEXT)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 80))
        screen.blit(title_surf, title_rect)
        
        # Input mode info
        font_small = pygame.font.Font(None, 28)
        info_lines = [
            "Press F1 for Click-to-Fire mode",
            "Press F2 for Auto-Fire mode",
            "Press F3 for Keyboard-Only mode (IJKL)",
        ]
        y = SCREEN_HEIGHT - 220
        for line in info_lines:
            line_surf = font_small.render(line, True, COLOR_UI_TEXT)
            line_rect = line_surf.get_rect(center=(SCREEN_WIDTH // 2, y))
            screen.blit(line_surf, line_rect)
            y += 35
        
        # Draw controls
        for control in self.controls:
            control.draw(screen)
        
        self.back_button.draw(screen)
