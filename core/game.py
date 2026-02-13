"""
Minimal Game class for Pygbag deployment.
"""
import pygame

class Game:
    """Main game orchestrator."""
    
    def __init__(self, screen):
        """Initialize game with display surface."""
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.message = "Fractured Depths - Awaiting Full Implementation"
        self.submessage = "Press ESC to quit | WASD to move (when implemented)"
        
    def handle_event(self, event):
        """Process input events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
    
    def update(self, dt):
        """Update game state."""
        pass
    
    def draw(self):
        """Render game to screen."""
        # Clear screen with dark background
        self.screen.fill((15, 15, 20))
        
        # Draw title message
        text_surface = self.font.render(self.message, True, (100, 200, 255))
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, 
                                                   self.screen.get_height() // 2 - 20))
        self.screen.blit(text_surface, text_rect)
        
        # Draw submessage
        small_font = pygame.font.Font(None, 24)
        sub_surface = small_font.render(self.submessage, True, (170, 170, 170))
        sub_rect = sub_surface.get_rect(center=(self.screen.get_width() // 2,
                                                 self.screen.get_height() // 2 + 20))
        self.screen.blit(sub_surface, sub_rect)
        
        # Draw instructions
        instructions = [
            "GitHub Pages Deployment: READY",
            "Pygbag WebAssembly: CONFIGURED",
            "Awaiting: Full game implementation"
        ]
        
        y_offset = self.screen.get_height() // 2 + 100
        for instruction in instructions:
            inst_surface = small_font.render(instruction, True, (100, 255, 100))
            inst_rect = inst_surface.get_rect(center=(self.screen.get_width() // 2, y_offset))
            self.screen.blit(inst_surface, inst_rect)
            y_offset += 30
