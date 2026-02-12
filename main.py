"""
Entry point. Game loop and state orchestration.
"""
import sys
import pygame
from config import *
from core.game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    
    game = Game(screen)
    
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # delta time in seconds
        dt *= GAME_SPEED
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)
        
        game.update(dt)
        game.draw()
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
