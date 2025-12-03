"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: Bryant Clarke

AI Usage: AI helped with syntax formatting and error checking

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    """
    # TODO: Implement this function
    # Must handle:
    # - FileNotFoundError → raise MissingDataFileError
    # - Invalid format → raise InvalidDataFormatError
    # - Corrupted/unreadable data → raise CorruptedDataError

    if not os.path.exists(filename):
        # Matches test_missing_data_file_exception: they expect MissingDataFileError
        raise MissingDataFileError(f"Quest file '{filename}' not found.")

    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        # Just in case file disappears between exists() and open()
        raise MissingDataFileError(f"Quest file '{filename}' not found.")
    except OSError:
        # Any low-level I/O problem is treated as corrupted
        raise CorruptedDataError(f"Quest file '{filename}' is corrupted or unreadable.")

    quests = {}
    current_block = []

    # We group lines into "blocks" separated by blank lines; each block = one quest
    for line in lines:
        if line.strip() == "":
            if current_block:
                quest = parse_quest_block(current_block)
                quests[quest["quest_id"]] = quest
                current_block = []
        else:
            current_block.append(line.rstrip("\n"))

    # Handle last block if file doesn't end with a blank line
    if current_block:
        quest = parse_quest_block(current_block)
        quests[quest["quest_id"]] = quest

    return quests

def load_items(filename="data/items.txt"):
    """
    Load item data from file
    """
    # TODO: Implement this function
    # Must handle same exceptions as load_quests

    if not os.path.exists(filename):
        raise MissingDataFileError(f"Item file '{filename}' not found.")

    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise MissingDataFileError(f"Item file '{filename}' not found.")
    except OSError:
        raise CorruptedDataError(f"Item file '{filename}' is corrupted or unreadable.")

    items = {}
    current_block = []

    # Same block-based parsing as for quests
    for line in lines:
        if line.strip() == "":
            if current_block:
                item = parse_item_block(current_block)
                items[item["item_id"]] = item
                current_block = []
        else:
            current_block.append(line.rstrip("\n"))

    if current_block:
        item = parse_item_block(current_block)
        items[item["item_id"]] = item

    return items

def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    """
    # TODO: Implement validation
    # Check that all required keys exist
    # Check that numeric values are actually numbers

    required_fields = [
        "quest_id",
        "title",
        "description",
        "reward_xp",
        "reward_gold",
        "required_level",
        "prerequisite",
    ]

    for key in required_fields:
        if key not in quest_dict:
            # Tests expect InvalidDataFormatError when something is missing
            raise InvalidDataFormatError(f"Missing quest field: {key}")

    # Ensure numeric types are actually ints (loaders convert them)
    numeric_fields = ["reward_xp", "reward_gold", "required_level"]
    for key in numeric_fields:
        if not isinstance(quest_dict[key], int):
            raise InvalidDataFormatError(f"Quest field '{key}' must be an integer.")

    return True

def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    """
    # TODO: Implement validation

    required_fields = [
        "item_id",
        "name",
        "type",
        "effect",
        "cost",
        "description",
    ]

    for key in required_fields:
        if key not in item_dict:
            raise InvalidDataFormatError(f"Missing item field: {key}")

    # Check type is valid
    valid_types = {"weapon", "armor", "consumable"}
    if item_dict["type"] not in valid_types:
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}")

    # Cost must be integer
    if not isinstance(item_dict["cost"], int):
        raise InvalidDataFormatError("Item 'cost' must be an integer.")

    return True

def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    # TODO: Implement this function
    # Create data/ directory if it doesn't exist
    # Create default quests.txt and items.txt files
    # Handle any file permission errors appropriately

    os.makedirs("data", exist_ok=True)
    os.makedirs("data/save_games", exist_ok=True)  # Helpful for saves later

    quests_path = os.path.join("data", "quests.txt")
    items_path = os.path.join("data", "items.txt")

    # Only create defaults if files are missing, so we don't overwrite instructor data
    if not os.path.exists(quests_path):
        # Include 'first_steps' because tests use that quest ID in the full workflow
        default_quests = """QUEST_ID: first_steps
TITLE: First Steps
DESCRIPTION: Your adventure begins with a simple task.
REWARD_XP: 50
REWARD_GOLD: 25
REQUIRED_LEVEL: 1
PREREQUISITE: NONE
"""
        with open(quests_path, "w") as f:
            f.write(default_quests)

    if not os.path.exists(items_path):
        # Include 'health_potion' because tests buy this item by ID
        default_items = """ITEM_ID: health_potion
NAME: Health Potion
TYPE: consumable
EFFECT: health:20
COST: 25
DESCRIPTION: Restores 20 health.
"""
        with open(items_path, "w") as f:
            f.write(default_items)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    """
    # TODO: Implement parsing logic
    # Split each line on ": " to get key-value pairs
    # Convert numeric strings to integers
    # Handle parsing errors gracefully

    quest = {}

    for line in lines:
        if ":" not in line:
            # This is exactly what the bad-data test creates
            raise InvalidDataFormatError("Quest line missing ':' separator.")

        key, value = line.split(":", 1)
        key = key.strip().upper()
        value = value.strip()

        if key == "QUEST_ID":
            quest["quest_id"] = value
        elif key == "TITLE":
            quest["title"] = value
        elif key == "DESCRIPTION":
            quest["description"] = value
        elif key == "REWARD_XP":
            try:
                quest["reward_xp"] = int(value)
            except ValueError:
                raise InvalidDataFormatError("REWARD_XP must be an integer.")
        elif key == "REWARD_GOLD":
            try:
                quest["reward_gold"] = int(value)
            except ValueError:
                raise InvalidDataFormatError("REWARD_GOLD must be an integer.")
        elif key == "REQUIRED_LEVEL":
            try:
                quest["required_level"] = int(value)
            except ValueError:
                raise InvalidDataFormatError("REQUIRED_LEVEL must be an integer.")
        elif key == "PREREQUISITE":
            quest["prerequisite"] = value
        else:
            # Ignore unknown keys, or could raise depending on design
            pass

    # Make sure structure is correct
    validate_quest_data(quest)
    return quest

def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    """
    # TODO: Implement parsing logic

    item = {}

    for line in lines:
        if ":" not in line:
            raise InvalidDataFormatError("Item line missing ':' separator.")

        key, value = line.split(":", 1)
        key = key.strip().upper()
        value = value.strip()

        if key == "ITEM_ID":
            item["item_id"] = value
        elif key == "NAME":
            item["name"] = value
        elif key == "TYPE":
            item["type"] = value
        elif key == "EFFECT":
            item["effect"] = value
        elif key == "COST":
            try:
                item["cost"] = int(value)
            except ValueError:
                raise InvalidDataFormatError("COST must be an integer.")
        elif key == "DESCRIPTION":
            item["description"] = value
        else:
            pass

    validate_item_data(item)
    return item

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    # create_default_data_files()
    
    # Test loading quests
    # try:
    #     quests = load_quests()
    #     print(f"Loaded {len(quests)} quests")
    # except MissingDataFileError:
    #     print("Quest file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid quest format: {e}")
    
    # Test loading items
    # try:
    #     items = load_items()
    #     print(f"Loaded {len(items)} items")
    # except MissingDataFileError:
    #     print("Item file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid item format: {e}")
