"""
Artifact definitions with stat modifiers.
"""

class Artifact:
    def __init__(self, name, description, effect_func):
        self.name = name
        self.description = description
        self.effect_func = effect_func
    
    def apply(self, player):
        self.effect_func(player)

def create_artifacts():
    artifacts = []
    
    # Damage boosters
    artifacts.append(Artifact(
        "Overcharged Cells",
        "+20% Damage",
        lambda p: setattr(p, 'damage', p.damage * 1.2)
    ))
    
    artifacts.append(Artifact(
        "Plasma Amplifier",
        "+30% Damage",
        lambda p: setattr(p, 'damage', p.damage * 1.3)
    ))
    
    # Fire rate boosters
    artifacts.append(Artifact(
        "Rapid Actuators",
        "+25% Fire Rate",
        lambda p: setattr(p, 'fire_rate', p.fire_rate * 1.25)
    ))
    
    artifacts.append(Artifact(
        "Neural Accelerator",
        "+40% Fire Rate",
        lambda p: setattr(p, 'fire_rate', p.fire_rate * 1.4)
    ))
    
    # Movement speed
    artifacts.append(Artifact(
        "Kinetic Boots",
        "+20% Speed",
        lambda p: setattr(p, 'speed', p.speed * 1.2)
    ))
    
    artifacts.append(Artifact(
        "Phase Shifter",
        "+35% Speed",
        lambda p: setattr(p, 'speed', p.speed * 1.35)
    ))
    
    # Health boosts
    artifacts.append(Artifact(
        "Reinforced Plating",
        "+20 Max HP",
        lambda p: (setattr(p, 'max_hp', p.max_hp + 20), setattr(p, 'hp', p.hp + 20))
    ))
    
    artifacts.append(Artifact(
        "Regenerative Core",
        "+30 Max HP",
        lambda p: (setattr(p, 'max_hp', p.max_hp + 30), setattr(p, 'hp', p.hp + 30))
    ))
    
    # Projectile count
    artifacts.append(Artifact(
        "Split Barrel",
        "+1 Projectile",
        lambda p: setattr(p, 'projectile_count', p.projectile_count + 1)
    ))
    
    artifacts.append(Artifact(
        "Tri-Barrel Array",
        "+2 Projectiles",
        lambda p: setattr(p, 'projectile_count', p.projectile_count + 2)
    ))
    
    # Projectile speed
    artifacts.append(Artifact(
        "Ballistic Enhancer",
        "+30% Projectile Speed",
        lambda p: setattr(p, 'projectile_speed', p.projectile_speed * 1.3)
    ))
    
    # Currency bonus
    artifacts.append(Artifact(
        "Fortune Magnet",
        "+50% Currency Gain",
        lambda p: setattr(p, 'currency_mult', p.currency_mult * 1.5)
    ))
    
    # Combo effects
    artifacts.append(Artifact(
        "Berserker Chip",
        "+15% Dmg, +15% Speed",
        lambda p: (setattr(p, 'damage', p.damage * 1.15), setattr(p, 'speed', p.speed * 1.15))
    ))
    
    artifacts.append(Artifact(
        "Glass Cannon",
        "+50% Dmg, -10 Max HP",
        lambda p: (setattr(p, 'damage', p.damage * 1.5), setattr(p, 'max_hp', max(10, p.max_hp - 10)))
    ))
    
    artifacts.append(Artifact(
        "Tank Module",
        "+40 Max HP, -10% Speed",
        lambda p: (setattr(p, 'max_hp', p.max_hp + 40), setattr(p, 'hp', p.hp + 40), setattr(p, 'speed', p.speed * 0.9))
    ))
    
    artifacts.append(Artifact(
        "Precision Optics",
        "Tighter Spread",
        lambda p: setattr(p, 'projectile_spread', p.projectile_spread * 0.5)
    ))
    
    artifacts.append(Artifact(
        "Scatter Matrix",
        "Wider Spread, +1 Projectile",
        lambda p: (setattr(p, 'projectile_spread', p.projectile_spread * 1.5), setattr(p, 'projectile_count', p.projectile_count + 1))
    ))
    
    artifacts.append(Artifact(
        "Vampiric Protocol",
        "Heal 1 HP per kill",
        lambda p: setattr(p, 'lifesteal', True)
    ))
    
    artifacts.append(Artifact(
        "Siege Engine",
        "+100% Dmg, -40% Fire Rate",
        lambda p: (setattr(p, 'damage', p.damage * 2.0), setattr(p, 'fire_rate', p.fire_rate * 0.6))
    ))
    
    artifacts.append(Artifact(
        "Perfect Balance",
        "+10% All Stats",
        lambda p: (
            setattr(p, 'damage', p.damage * 1.1),
            setattr(p, 'fire_rate', p.fire_rate * 1.1),
            setattr(p, 'speed', p.speed * 1.1),
            setattr(p, 'max_hp', int(p.max_hp * 1.1)),
            setattr(p, 'hp', int(p.hp * 1.1))
        )
    ))
    
    return artifacts

ARTIFACTS = create_artifacts()
