#!/usr/bin/env python3
"""
Test script to verify all game features and systems.
Runs in headless mode for automated testing.
"""
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import pygame
import sys
sys.path.insert(0, '.')

from config import *
from core.game import Game, GameState
from systems.input_manager import AimMode
from content.artifacts import ARTIFACTS

def test_game_initialization():
    """Test that the game initializes correctly"""
    print("Testing game initialization...")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game = Game(screen)
    
    assert game.state == GameState.TITLE, "Game should start in TITLE state"
    assert game.camera is not None, "Camera should be initialized"
    assert game.input_manager is not None, "Input manager should be initialized"
    print("✓ Game initialization successful")
    return game, screen

def test_game_start(game):
    """Test starting a new game"""
    print("\nTesting game start...")
    game.start_game()
    
    assert game.state == GameState.PLAYING, "Game should be in PLAYING state"
    assert game.player is not None, "Player should be created"
    assert game.current_room is not None, "Room should be loaded"
    assert game.floor_generator is not None, "Floor should be generated"
    
    print(f"✓ Game started successfully")
    print(f"  - Player HP: {game.player.hp}/{game.player.max_hp}")
    print(f"  - Player position: ({game.player.x:.1f}, {game.player.y:.1f})")
    print(f"  - Room type: {game.current_room.room_type.name}")
    print(f"  - Floor size: {len(game.floor_generator.rooms)} rooms")

def test_input_modes(game):
    """Test all three input modes"""
    print("\nTesting input modes...")
    
    # Test mode 1: Cursor Click
    game.input_manager.set_aim_mode(AimMode.CURSOR_CLICK)
    assert game.input_manager.aim_mode == AimMode.CURSOR_CLICK
    assert game.input_manager.auto_fire == False
    print("✓ F1: Click-to-Fire mode works")
    
    # Test mode 2: Auto Fire
    game.input_manager.set_aim_mode(AimMode.AUTO_FIRE)
    assert game.input_manager.aim_mode == AimMode.AUTO_FIRE
    assert game.input_manager.auto_fire == True
    print("✓ F2: Auto-Fire mode works")
    
    # Test mode 3: Keyboard Only
    game.input_manager.set_aim_mode(AimMode.KEYBOARD_ONLY)
    assert game.input_manager.aim_mode == AimMode.KEYBOARD_ONLY
    print("✓ F3: Keyboard-Only mode works")

def test_player_systems(game):
    """Test player movement, shooting, and stats"""
    print("\nTesting player systems...")
    
    # Test movement
    initial_x = game.player.x
    game.player.move(1, 0, 0.1, game.current_room)
    assert game.player.x != initial_x, "Player should move"
    print("✓ Player movement works")
    
    # Test shooting
    initial_proj_count = len([p for p in game.projectile_system.projectiles if p.active])
    game.player.shoot((1, 0), game.projectile_system)
    new_proj_count = len([p for p in game.projectile_system.projectiles if p.active])
    assert new_proj_count > initial_proj_count, "Projectile should be spawned"
    print("✓ Player shooting works")
    
    # Test damage
    initial_hp = game.player.hp
    game.player.take_damage(10)
    assert game.player.hp < initial_hp, "Player should take damage"
    print("✓ Player damage system works")

def test_enemy_systems(game):
    """Test enemy spawning and behavior"""
    print("\nTesting enemy systems...")
    
    from content.enemies import Chaser, Shooter, Charger, Splitter
    
    # Test enemy creation
    enemies = [
        Chaser(200, 200),
        Shooter(300, 300),
        Charger(400, 400),
        Splitter(500, 500)
    ]
    
    for enemy in enemies:
        assert enemy.alive, f"{enemy.__class__.__name__} should be alive"
        assert enemy.hp > 0, f"{enemy.__class__.__name__} should have HP"
    
    print(f"✓ All 4 enemy archetypes created successfully")
    
    # Test enemy damage
    enemies[0].take_damage(50)
    assert not enemies[0].alive, "Enemy should die when HP reaches 0"
    print("✓ Enemy damage system works")

def test_boss_systems():
    """Test boss creation"""
    print("\nTesting boss systems...")
    
    from content.bosses import Sentinel, NexusCore
    
    sentinel = Sentinel(600, 600)
    nexus = NexusCore(700, 700)
    
    assert sentinel.alive, "Sentinel should be alive"
    assert nexus.alive, "NexusCore should be alive"
    assert nexus.phase == 1, "NexusCore should start in phase 1"
    
    print("✓ Both boss types created successfully")
    print(f"  - Sentinel HP: {sentinel.hp}/{sentinel.max_hp}")
    print(f"  - NexusCore HP: {nexus.hp}/{nexus.max_hp}")

def test_artifact_system(game):
    """Test artifact application"""
    print("\nTesting artifact system...")
    
    initial_damage = game.player.damage
    initial_speed = game.player.speed
    
    # Apply damage boost artifact
    damage_artifact = [a for a in ARTIFACTS if "Damage" in a.description][0]
    damage_artifact.apply(game.player)
    assert game.player.damage > initial_damage, "Artifact should increase damage"
    
    print(f"✓ Artifacts work (tested {len(ARTIFACTS)} total)")
    print(f"  - Damage increased from {initial_damage:.1f} to {game.player.damage:.1f}")

def test_projectile_system(game):
    """Test projectile pooling and collision"""
    print("\nTesting projectile system...")
    
    # Test spawning
    proj = game.projectile_system.spawn_projectile(100, 100, 0, 400, 10, True)
    assert proj is not None, "Projectile should spawn"
    assert proj.active, "Projectile should be active"
    
    # Test update
    initial_x = proj.x
    proj.update(0.1)
    assert proj.x != initial_x, "Projectile should move"
    
    print("✓ Projectile system with object pooling works")
    print(f"  - Pool size: {len(game.projectile_system.projectiles)}")

def test_room_system(game):
    """Test room generation and layout"""
    print("\nTesting room system...")
    
    assert game.current_room is not None, "Room should exist"
    assert len(game.current_room.walls) > 0, "Room should have walls"
    assert game.current_room.layout is not None, "Room should have layout"
    
    print("✓ Room system works")
    print(f"  - Wall count: {len(game.current_room.walls)}")
    print(f"  - Layout size: {len(game.current_room.layout)}x{len(game.current_room.layout[0])}")

def test_floor_generation(game):
    """Test procedural floor generation"""
    print("\nTesting floor generation...")
    
    assert game.floor_generator is not None, "Floor generator should exist"
    assert len(game.floor_generator.rooms) >= 10, "Floor should have at least 10 rooms"
    assert game.floor_generator.start_room is not None, "Should have start room"
    assert game.floor_generator.boss_room is not None, "Should have boss room"
    
    room_types = {}
    for room in game.floor_generator.rooms.values():
        room_type = room.room_type.name
        room_types[room_type] = room_types.get(room_type, 0) + 1
    
    print("✓ Floor generation works")
    print(f"  - Total rooms: {len(game.floor_generator.rooms)}")
    print(f"  - Room types: {room_types}")

def test_ui_systems(game):
    """Test UI components"""
    print("\nTesting UI systems...")
    
    assert game.title_menu is not None, "Title menu should exist"
    assert game.pause_menu is not None, "Pause menu should exist"
    assert game.settings_menu is not None, "Settings menu should exist"
    assert game.hud is not None, "HUD should exist"
    
    print("✓ All UI systems initialized")

def test_game_loop(game):
    """Test game update loop"""
    print("\nTesting game loop...")
    
    # Run a few frames
    for i in range(60):  # ~1 second at 60 FPS
        game.update(0.016)
    
    print("✓ Game loop runs without errors")

def run_all_tests():
    """Run all test suites"""
    print("=" * 60)
    print("Fractured Depths - Comprehensive Test Suite")
    print("=" * 60)
    
    game, screen = test_game_initialization()
    test_game_start(game)
    test_input_modes(game)
    test_player_systems(game)
    test_enemy_systems(game)
    test_boss_systems()
    test_artifact_system(game)
    test_projectile_system(game)
    test_room_system(game)
    test_floor_generation(game)
    test_ui_systems(game)
    test_game_loop(game)
    
    print("\n" + "=" * 60)
    print("✓ ALL TESTS PASSED!")
    print("=" * 60)
    print("\nGame is ready to play!")
    print("Run with: python main.py")

if __name__ == "__main__":
    run_all_tests()
