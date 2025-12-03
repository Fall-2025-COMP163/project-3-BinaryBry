"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: Bryant Clarke

AI Usage: AI helped with syntax formatting and error checking

Handles combat mechanics
"""

from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

import random  # Needed for escape % and Rogue crit chance

# Basic enemy stat templates for creation.
# This lets us reference enemy types easily and avoids repeated code.
ENEMY_STATS = {
    "goblin": {
        "name": "Goblin",
        "health": 50,
        "strength": 8,
        "magic": 2,
        "xp_reward": 25,
        "gold_reward": 10,
    },
    "orc": {
        "name": "Orc",
        "health": 80,
        "strength": 12,
        "magic": 5,
        "xp_reward": 50,
        "gold_reward": 25,
    },
    "dragon": {
        "name": "Dragon",
        "health": 200,
        "strength": 25,
        "magic": 15,
        "xp_reward": 200,
        "gold_reward": 100,
    },
}

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    """
    Create an enemy based on type    
    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100
    
    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
    # TODO: Implement enemy creation

    enemy_type = enemy_type.lower()  # Normalize input so "Goblin"/"goblin" both work

    if enemy_type not in ENEMY_STATS:
        # The test expects InvalidTargetError for unknown enemy names
        raise InvalidTargetError(f"Enemy type '{enemy_type}' does not exist.")

    base = ENEMY_STATS[enemy_type]  # Get template

    # Build a fresh enemy dictionary so edits don't modify template
    enemy = {
        "name": base["name"],
        "health": base["health"],
        "max_health": base["health"],  # Copy base health
        "strength": base["strength"],
        "magic": base["magic"],
        "xp_reward": base["xp_reward"],
        "gold_reward": base["gold_reward"],
    }
    return enemy


def get_random_enemy_for_level(character_level):
    """
    Return enemy type appropriate for character level
    """
    # TODO: Implement level-appropriate enemy selection

    # Simple level brackets required by tests
    if character_level <= 2:
        enemy_type = "goblin"
    elif character_level <= 5:
        enemy_type = "orc"
    else:
        enemy_type = "dragon"

    # Reuse create_enemy so all validation stays consistent
    return create_enemy(enemy_type)

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:

    def __init__(self, character, enemy):
        """
        Create a battle instance.
        """
        # TODO: Implement initialization

        self.character = character         # Store character reference
        self.enemy = enemy                 # Store enemy reference
        self.combat_active = True          # Needed so tests know combat is "on"
        self.turn_count = 0                # Helps track turns if needed later

    def start_battle(self):
        """
        Start combat loop (auto-runs to avoid menu input during tests)
        """
        # TODO: Implement battle loop

        if self.character.get("health", 0) <= 0:
            # Tests expect starting battle with zero health to raise this error
            raise CharacterDeadError("Cannot start battle when dead.")

        # Auto-battle loop to satisfy tests without requiring user input
        while self.combat_active:

            self.turn_count += 1

            # Player attacks first
            self.player_turn()
            winner = self.check_battle_end()
            if winner is not None:
                break

            # Enemy responds
            self.enemy_turn()
            winner = self.check_battle_end()
            if winner is not None:
                break

        # If player wins, return rewards in required structure
        if winner == "player":
            rewards = get_victory_rewards(self.enemy)
            return {
                "winner": "player",
                "xp_gained": rewards["xp"],
                "gold_gained": rewards["gold"]
            }

        # Otherwise player lost
        return {"winner": "enemy", "xp_gained": 0, "gold_gained": 0}

    def player_turn(self):
        """
        Player basic turn — tests expect automatic basic attack
        """
        # TODO: Implement player turn

        if not self.combat_active:
            # Required test: calling this while inactive must raise CombatNotActiveError
            raise CombatNotActiveError("Battle is not active.")

        # Basic attack damage calculation
        damage = self.calculate_damage(self.character, self.enemy)

        # Apply damage to enemy
        self.apply_damage(self.enemy, damage)

        display_battle_log(f"{self.character.get('name', 'Hero')} hits for {damage} damage.")

    def enemy_turn(self):
        """
        Enemy AI: always attacks directly.
        """
        # TODO: Implement enemy turn

        if not self.combat_active:
            raise CombatNotActiveError("Battle is not active.")

        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)

        display_battle_log(f"{self.enemy.get('name', 'Enemy')} hits for {damage} damage.")

    def calculate_damage(self, attacker, defender):
        """
        Damage = attacker strength - (defender strength // 4)
        """
        # TODO: Implement damage calculation

        atk = int(attacker.get("strength", 0))
        defense = int(defender.get("strength", 0)) // 4

        # Damage formula ensures weaker defenders take more damage
        damage = atk - defense

        # Tests require minimum damage of at least 1
        if damage < 1:
            damage = 1

        return damage

    def apply_damage(self, target, damage):
        """
        Reduce target health, cannot go negative
        """
        # TODO: Implement damage application

        hp = target.get("health", 0) - damage
        if hp < 0:
            hp = 0
        target["health"] = hp

    def check_battle_end(self):
        """
        Determine if someone died; used by tests
        """
        # TODO: Implement battle end check

        if self.enemy.get("health", 0) <= 0:
            return "player"
        if self.character.get("health", 0) <= 0:
            return "enemy"
        return None

    def attempt_escape(self):
        """
        50% chance to escape battle
        """
        # TODO: Implement escape attempt

        # If combat already ended, escape makes no sense
        if not self.combat_active:
            return False

        # Random chance check
        if random.random() < 0.5:
            display_battle_log("Escape succeeded!")
            self.combat_active = False
            return True

        display_battle_log("Escape failed!")
        return False

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Route to correct special ability based on class.
    """
    # TODO: Implement special abilities

    char_class = character.get("class", "")

    if char_class == "Warrior":
        return warrior_power_strike(character, enemy)
    elif char_class == "Mage":
        return mage_fireball(character, enemy)
    elif char_class == "Rogue":
        return rogue_critical_strike(character, enemy)
    elif char_class == "Cleric":
        return cleric_heal(character)
    else:
        return "No special ability available."


def warrior_power_strike(character, enemy):
    """Warrior doubles their STR for a powerful strike"""
    # TODO: Implement power strike

    damage = character.get("strength", 0) * 2
    new_hp = max(enemy.get("health", 0) - damage, 0)
    enemy["health"] = new_hp

    msg = f"{character.get('name', 'Warrior')} uses Power Strike for {damage} damage!"
    display_battle_log(msg)
    return msg


def mage_fireball(character, enemy):
    """Mage uses magic for double magic damage"""
    # TODO: Implement fireball

    damage = character.get("magic", 0) * 2
    new_hp = max(enemy.get("health", 0) - damage, 0)
    enemy["health"] = new_hp

    msg = f"{character.get('name', 'Mage')} casts Fireball for {damage} damage!"
    display_battle_log(msg)
    return msg


def rogue_critical_strike(character, enemy):
    """Rogue: 50% chance to deal triple damage"""
    # TODO: Implement critical strike

    strength = character.get("strength", 0)

    if random.random() < 0.5:
        # Crit happens
        damage = strength * 3
        crit = True
    else:
        # No crit
        damage = strength
        crit = False

    new_hp = max(enemy.get("health", 0) - damage, 0)
    enemy["health"] = new_hp

    if crit:
        msg = f"{character.get('name', 'Rogue')} lands a CRITICAL STRIKE for {damage}!"
    else:
        msg = f"{character.get('name', 'Rogue')} strikes for {damage}."

    display_battle_log(msg)
    return msg


def cleric_heal(character):
    """Cleric restores 30 HP"""
    # TODO: Implement healing

    old_hp = character.get("health", 0)
    healed_hp = min(character.get("max_health", old_hp), old_hp + 30)
    character["health"] = healed_hp

    amount = healed_hp - old_hp
    msg = f"{character.get('name', 'Cleric')} heals for {amount} HP."
    display_battle_log(msg)
    return msg

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Returns True if character is alive.
    """
    # TODO: Implement fight check

    return character.get("health", 0) > 0


def get_victory_rewards(enemy):
    """
    Return rewards exactly as test expects
    """
    # TODO: Implement reward calculation

    return {
        "xp": enemy.get("xp_reward", 0),
        "gold": enemy.get("gold_reward", 0)
    }


def display_combat_stats(character, enemy):
    """
    Show both fighter HP — used for debugging only
    """
    # TODO: Implement status display

    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")
    pass


def display_battle_log(message):
    """
    Print battle text (kept simple for grading)
    """
    # TODO: Implement battle log display
    print(f">>> {message}")
    pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    # Manual tests left as provided
