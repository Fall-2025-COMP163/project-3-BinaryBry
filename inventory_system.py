"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: Bryant Clarke

AI Usage: AI helped with syntax formatting and error checking

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    """
    Add an item to character's inventory
    """
    # TODO: Implement adding items
    # Check if inventory is full (>= MAX_INVENTORY_SIZE)
    # Add item_id to character['inventory'] list

    inventory = character.setdefault("inventory", [])  # Make sure inventory list exists

    if len(inventory) >= MAX_INVENTORY_SIZE:
        # Matches test_inventory_full_exception
        raise InventoryFullError("Inventory is full.")

    inventory.append(item_id)
    return True

def remove_item_from_inventory(character, item_id):
    """
    Remove an item from character's inventory
    """
    # TODO: Implement item removal
    # Check if item exists in inventory
    # Remove item from list

    inventory = character.setdefault("inventory", [])

    if item_id not in inventory:
        # Tests expect ItemNotFoundError when removing something not present
        raise ItemNotFoundError(f"Item '{item_id}' not found in inventory.")

    inventory.remove(item_id)
    return True

def has_item(character, item_id):
    """
    Check if character has a specific item
    """
    # TODO: Implement item check

    return item_id in character.get("inventory", [])

def count_item(character, item_id):
    """
    Count how many of a specific item the character has
    """
    # TODO: Implement item counting
    # Use list.count() method

    return character.get("inventory", []).count(item_id)

def get_inventory_space_remaining(character):
    """
    Calculate how many more items can fit in inventory
    """
    # TODO: Implement space calculation

    return MAX_INVENTORY_SIZE - len(character.get("inventory", []))

def clear_inventory(character):
    """
    Remove all items from inventory
    """
    # TODO: Implement inventory clearing
    # Save current inventory before clearing
    # Clear character's inventory list

    current = list(character.get("inventory", []))  # Make a copy
    character["inventory"] = []                    # Clear inventory
    return current

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    """
    Use a consumable item from inventory
    """
    # TODO: Implement item usage
    # Check if character has the item
    # Check if item type is 'consumable'
    # Parse effect (format: "stat_name:value" e.g., "health:20")
    # Apply effect to character
    # Remove item from inventory

    if not has_item(character, item_id):
        # Required by tests
        raise ItemNotFoundError(f"Item '{item_id}' not found.")

    if item_data.get("type") != "consumable":
        # test_invalid_item_type_exception triggers this
        raise InvalidItemTypeError("Only consumable items can be used.")

    stat_name, value = parse_item_effect(item_data.get("effect", ""))
    apply_stat_effect(character, stat_name, value)

    # Remove a single copy of the item after use
    remove_item_from_inventory(character, item_id)

    return f"Used {item_id} and applied {stat_name}+{value}."

def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon
    """
    # TODO: Implement weapon equipping
    # Check item exists and is type 'weapon'
    # Handle unequipping current weapon if exists
    # Parse effect and apply to character stats
    # Store equipped_weapon in character dictionary
    # Remove item from inventory

    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Weapon '{item_id}' not found in inventory.")

    if item_data.get("type") != "weapon":
        raise InvalidItemTypeError("Item is not a weapon.")

    # If a weapon is already equipped, unequip it first
    if "equipped_weapon" in character and character["equipped_weapon"] is not None:
        unequip_weapon(character)

    stat_name, value = parse_item_effect(item_data.get("effect", ""))

    # Track what stat and bonus this weapon gave so we can reverse it later
    character["equipped_weapon"] = item_id
    character["equipped_weapon_stat"] = stat_name
    character["equipped_weapon_bonus"] = value

    apply_stat_effect(character, stat_name, value)

    # Remove weapon from inventory when equipped
    remove_item_from_inventory(character, item_id)

    return f"Equipped weapon {item_id} (+{value} {stat_name})."

def equip_armor(character, item_id, item_data):
    """
    Equip armor
    """
    # TODO: Implement armor equipping
    # Similar to equip_weapon but for armor

    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Armor '{item_id}' not found in inventory.")

    if item_data.get("type") != "armor":
        raise InvalidItemTypeError("Item is not armor.")

    # If armor already equipped, unequip first
    if "equipped_armor" in character and character["equipped_armor"] is not None:
        unequip_armor(character)

    stat_name, value = parse_item_effect(item_data.get("effect", ""))

    character["equipped_armor"] = item_id
    character["equipped_armor_stat"] = stat_name
    character["equipped_armor_bonus"] = value

    apply_stat_effect(character, stat_name, value)

    remove_item_from_inventory(character, item_id)

    return f"Equipped armor {item_id} (+{value} {stat_name})."

def unequip_weapon(character):
    """
    Remove equipped weapon and return it to inventory
    """
    # TODO: Implement weapon unequipping
    # Check if weapon is equipped
    # Remove stat bonuses
    # Add weapon back to inventory
    # Clear equipped_weapon from character

    weapon_id = character.get("equipped_weapon")
    if not weapon_id:
        return None

    # Before unequipping, make sure inventory has space
    if get_inventory_space_remaining(character) <= 0:
        # Spec says to raise InventoryFullError if inventory is full
        raise InventoryFullError("Inventory is full; cannot unequip weapon.")

    stat_name = character.get("equipped_weapon_stat")
    bonus = character.get("equipped_weapon_bonus", 0)

    # Remove the stat bonus we added when equipping
    if stat_name in character:
        character[stat_name] -= bonus

    # Add weapon back to inventory
    add_item_to_inventory(character, weapon_id)

    # Clear equipped info
    character["equipped_weapon"] = None
    character["equipped_weapon_stat"] = None
    character["equipped_weapon_bonus"] = 0

    return weapon_id

def unequip_armor(character):
    """
    Remove equipped armor and return it to inventory
    """
    # TODO: Implement armor unequipping

    armor_id = character.get("equipped_armor")
    if not armor_id:
        return None

    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError("Inventory is full; cannot unequip armor.")

    stat_name = character.get("equipped_armor_stat")
    bonus = character.get("equipped_armor_bonus", 0)

    if stat_name in character:
        character[stat_name] -= bonus

    add_item_to_inventory(character, armor_id)

    character["equipped_armor"] = None
    character["equipped_armor_stat"] = None
    character["equipped_armor_bonus"] = 0

    return armor_id

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    """
    Purchase an item from a shop
    """
    # TODO: Implement purchasing
    # Check if character has enough gold
    # Check if inventory has space
    # Subtract gold from character
    # Add item to inventory

    cost = item_data.get("cost", 0)

    # If gold too low, raise InsufficientResourcesError (test expects this)
    if character.get("gold", 0) < cost:
        raise InsufficientResourcesError("Not enough gold.")

    # If inventory is full, raise InventoryFullError
    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError("Inventory is full.")

    # Apply purchase
    character["gold"] -= cost
    add_item_to_inventory(character, item_id)

    return True

def sell_item(character, item_id, item_data):
    """
    Sell an item for half its purchase cost
    """
    # TODO: Implement selling
    # Check if character has item
    # Calculate sell price (cost // 2)
    # Remove item from inventory
    # Add gold to character

    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Item '{item_id}' not found in inventory.")

    cost = item_data.get("cost", 0)
    sell_price = cost // 2  # test_shop_system expects 25 // 2 = 12

    remove_item_from_inventory(character, item_id)
    character["gold"] = character.get("gold", 0) + sell_price

    return sell_price

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    """
    Parse item effect string into stat name and value
    """
    # TODO: Implement effect parsing
    # Split on ":"
    # Convert value to integer

    # Expect "stat:value" like "health:20"
    if ":" not in effect_string:
        # Using InvalidItemTypeError here keeps it inside inventory-related errors
        raise InvalidItemTypeError("Invalid effect format; expected 'stat:value'.")

    stat_name, value_str = effect_string.split(":", 1)
    stat_name = stat_name.strip()
    try:
        value = int(value_str.strip())
    except ValueError:
        raise InvalidItemTypeError("Effect value must be an integer.")

    return stat_name, value

def apply_stat_effect(character, stat_name, value):
    """
    Apply a stat modification to character
    """
    # TODO: Implement stat application
    # Add value to character[stat_name]
    # If stat is health, ensure it doesn't exceed max_health

    # Initialize stat if it doesn't exist
    if stat_name not in character:
        character[stat_name] = 0

    character[stat_name] += value

    # Clamp health to max_health so heals don't overflow
    if stat_name == "health":
        max_hp = character.get("max_health", character["health"])
        if character["health"] > max_hp:
            character["health"] = max_hp

def display_inventory(character, item_data_dict):
    """
    Display character's inventory in formatted way
    """
    # TODO: Implement inventory display
    # Count items (some may appear multiple times)
    # Display with item names from item_data_dict

    inventory = character.get("inventory", [])

    if not inventory:
        print("Inventory is empty.")
        return

    # Count each unique item
    printed = set()
    print("Inventory:")
    for item_id in inventory:
        if item_id in printed:
            continue
        qty = count_item(character, item_id)
        data = item_data_dict.get(item_id, {})
        name = data.get("name", item_id)
        item_type = data.get("type", "unknown")
        print(f"- {name} (id={item_id}, type={item_type}) x{qty}")
        printed.add(item_id)

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    
    # Test adding items
    # test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}
    # 
    # try:
    #     add_item_to_inventory(test_char, "health_potion")
    #     print(f"Inventory: {test_char['inventory']}")
    # except InventoryFullError:
    #     print("Inventory is full!")
    
    # Test using items
    # test_item = {
    #     'item_id': 'health_potion',
    #     'type': 'consumable',
    #     'effect': 'health:20'
    # }
    # 
    # try:
    #     result = use_item(test_char, "health_potion", test_item)
    #     print(result)
    # except ItemNotFoundError:
    #     print("Item not found")
