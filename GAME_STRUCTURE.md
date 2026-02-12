# Fractured Depths - Game Structure

## File Count: 27 Files Total

### Root Directory (5 files)
```
├── main.py                 # Entry point and game loop
├── config.py              # Global configuration and constants
├── requirements.txt       # Python dependencies
├── README.md             # User documentation
└── .gitignore            # Git ignore patterns
```

### Core Module (4 files)
```
core/
├── __init__.py           # Module initialization
├── utils.py              # Math and collision utilities
├── camera.py             # Camera system with smooth following
└── game.py               # Main game orchestration and state management
```

### Systems Module (5 files)
```
systems/
├── __init__.py           # Module initialization
├── input_manager.py      # 3 input modes (F1/F2/F3) with touchpad optimization
├── entity_manager.py     # Enemy lifecycle management
├── collision.py          # Collision detection (placeholder for optimizations)
└── projectile_system.py  # Object pooling for projectiles (500 pool)
```

### Content Module (7 files)
```
content/
├── __init__.py           # Module initialization
├── player.py             # Player entity with stats and movement
├── enemies.py            # 4 enemy archetypes (Chaser, Shooter, Charger, Splitter)
├── bosses.py             # 2 boss types (Sentinel, NexusCore)
├── artifacts.py          # 20 unique artifacts with stat modifiers
├── rooms.py              # 20+ room layout prefabs
└── floor_generator.py    # Procedural floor generation
```

### UI Module (4 files)
```
ui/
├── __init__.py           # Module initialization
├── menu.py               # Title, Pause, and Death menus
├── hud.py                # In-game HUD with HP, currency, minimap
└── settings_menu.py      # Settings with sliders and toggles
```

### Testing (2 files)
```
├── test_game.py          # Comprehensive test suite
```

---

## Key Features Implemented

### Input Systems (3 Modes)
- **F1**: Click-to-Fire - Cursor movement + click to shoot
- **F2**: Auto-Fire - Cursor movement + automatic firing
- **F3**: Keyboard-Only - IJKL aiming + Space to shoot

### Touchpad Optimizations
- Aim sensitivity adjustment (0.1 - 3.0)
- Aim smoothing (0.0 - 0.9)
- Deadzone configuration (0 - 100)
- Precision modifier (Shift key: 0.1 - 1.0)
- Fire rate control (1.0 - 20.0)

### Enemy Types (4 Archetypes)
1. **Chaser** - Pursues player directly
2. **Shooter** - Maintains distance and shoots
3. **Charger** - Dash attack with telegraph and stun
4. **Splitter** - Splits into smaller enemies on death

### Boss Types (2 Unique)
1. **Sentinel** - Mini-boss with spread shot patterns
2. **NexusCore** - Final boss with 3 phases

### Artifacts (20 Unique)
- Damage boosters (Overcharged Cells, Plasma Amplifier)
- Fire rate boosters (Rapid Actuators, Neural Accelerator)
- Movement speed (Kinetic Boots, Phase Shifter)
- Health boosts (Reinforced Plating, Regenerative Core)
- Projectile count (Split Barrel, Tri-Barrel Array)
- Combo effects (Berserker Chip, Glass Cannon, Tank Module)
- Special effects (Vampiric Protocol, Perfect Balance)

### Room System
- 20+ unique room layouts
- Procedural floor generation (10-15 rooms per floor)
- Room types: START, COMBAT, BOSS, REWARD
- Door system with lock/unlock mechanics

### Core Systems
- Smooth camera following with bounds
- Object pooling (500 projectile pool)
- Collision detection (circle-circle, circle-rect)
- State management (TITLE, PLAYING, PAUSED, SETTINGS, DEAD, REWARD)
- Minimap with room visualization

### UI Components
- Title menu with Start/Settings/Quit
- Pause menu (ESC key)
- Death screen with stats
- Settings menu with 8 controls
- HUD with HP bar, currency, artifacts count, minimap
- Crosshair visualization (toggle-able)

---

## Performance Targets
- 60 FPS target
- 500 projectile object pool
- Efficient collision detection
- Minimal memory allocations per frame

## Design Principles
- **Touchpad-First**: All controls optimized for laptop touchpads
- **Original Content**: 100% clean-room design, no copyrighted material
- **Self-Contained**: No external assets, all rendering procedural
- **Modular**: Clear separation of concerns across modules
- **Testable**: Comprehensive test suite included
