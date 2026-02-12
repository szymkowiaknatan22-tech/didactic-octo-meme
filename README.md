# Fractured Depths

A touchpad-optimized 2D roguelike shooter built with Python and Pygame.

## Features

- **3 Input Modes** optimized for touchpad/laptop play
  - **F1**: Click-to-Fire (cursor movement + click to shoot)
  - **F2**: Auto-Fire (cursor movement + automatic firing)
  - **F3**: Keyboard-Only (WASD movement + IJKL aiming + Space to shoot)
  
- **Procedurally Generated Floors** with random layouts
- **4 Enemy Archetypes**: Chaser, Shooter, Charger, Splitter
- **Boss Battles** with unique patterns
- **20 Unique Artifacts** with various stat modifiers
- **Touchpad Settings**:
  - Adjustable aim sensitivity
  - Smoothing control
  - Deadzone configuration
  - Precision modifier (hold Shift)
  - Fire rate adjustment

## Installation

1. Install Python 3.8 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Play

Run the game:
```bash
python main.py
```

### Controls

**Movement**: WASD keys

**Aiming & Shooting**:
- Press **F1** for Click-to-Fire mode
- Press **F2** for Auto-Fire mode  
- Press **F3** for Keyboard-Only mode (IJKL to aim, Space to shoot)

**Menu**:
- ESC: Pause game
- Settings menu: Adjust touchpad controls

### Gameplay

1. Start in a safe room
2. Clear combat rooms by defeating all enemies
3. Unlock doors and progress through the floor
4. Choose artifact rewards after clearing rooms
5. Defeat the boss to complete the floor
6. Survive as long as you can!

## Settings

Access the Settings menu from the title screen or pause menu to customize:

- **Aim Sensitivity**: Cursor movement speed
- **Aim Smoothing**: Smoothness of cursor movement (higher = smoother, lower = more responsive)
- **Deadzone**: Minimum touchpad movement before cursor moves
- **Fire Rate**: How fast you can shoot
- **Precision Modifier**: Sensitivity multiplier when holding Shift
- **Show Crosshair**: Toggle crosshair visibility
- **Hide System Cursor**: Hide the OS cursor
- **Relative Mouse**: Use relative mouse movement (experimental)

## Credits

This is a clean-room original design with no copyrighted content.

Designed for touchpad optimization as the primary input method.

## License

This project is provided as-is for educational purposes.
