"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: Bryant Clarke

AI Usage: AI helped with syntax formatting and error checking

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display main menu and get player choice
    """
    # TODO: Implement main menu display
    # Show options
    # Get user input
    # Validate input (1-3)
    # Return choice

    while True:
        print("\n=== MAIN MENU ===")
        print("1. New Game")
        print("2. Load Game")
        print("3. Exit")

        choice_str = input("Choose an option (1-3): ").strip()

        try:
            choice = int(choice_str)
        except ValueError:
            print("Please enter a number between 1 and 3.")
            continue

        if choice in (1, 2, 3):
            return choice
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

def new_game():
    """
    Start a new game
    """
    global current_character
    
    # TODO: Implement new game creation
    # Get character name from user
    # Get character class from user
    # Try to create character with character_manager.create_character()
    # Handle InvalidCharacterClassError
    # Save character
    # Start game loop

    print("\n=== NEW GAME ===")
    name = input("Enter your character's name: ").strip()

    while True:
        print("\nChoose a class: Warrior, Mage, Rogue, Cleric")
        char_class = input("Class: ").strip()

        try:
            current_character = character_manager.create_character(name, char_class)
            break
        except InvalidCharacterClassError as e:
            # If player types bad class, loop until they give a valid one
            print(f"Error: {e}. Please choose a valid class.")

    # Save the brand new character
    try:
        character_manager.save_character(current_character)
        print("Character created and saved.")
    except Exception as e:
        print(f"Warning: Could not save character: {e}")

    # Enter the main game loop
    game_loop()

def load_game():
    """
    Load an existing saved game
    """
    global current_character
    
    # TODO: Implement game loading
    # Get list of saved characters
    # Display them to user
    # Get user choice
    # Try to load character with character_manager.load_character()
    # Handle CharacterNotFoundError and SaveFileCorruptedError
    # Start game loop

    print("\n=== LOAD GAME ===")
    saved_names = character_manager.list_saved_characters()

    if not saved_names:
        print("No saved characters found.")
        return

    # Show numbered list
    for idx, name in enumerate(saved_names, start=1):
        print(f"{idx}. {name}")

    while True:
        choice_str = input("Select a character by number (or 0 to cancel): ").strip()

        try:
            choice = int(choice_str)
        except ValueError:
            print("Please enter a valid number.")
            continue

        if choice == 0:
            return

        if 1 <= choice <= len(saved_names):
            chosen_name = saved_names[choice - 1]
            try:
                current_character = character_manager.load_character(chosen_name)
                print(f"Loaded character: {chosen_name}")
                game_loop()
                return
            except CharacterNotFoundError:
                print("Save file not found.")
                return
            except SaveFileCorruptedError:
                print("Save file is corrupted and cannot be loaded.")
                return
            except InvalidSaveDataError as e:
                print(f"Invalid save data: {e}")
                return
        else:
            print("Invalid choice. Try again.")

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character
    
    game_running = True
    
    # TODO: Implement game loop
    # While game_running:
    #   Display game menu
    #   Get player choice
    #   Execute chosen action
    #   Save game after each action

    if current_character is None:
        print("No character loaded.")
        return

    while game_running:
        choice = game_menu()

        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print("Game saved. Exiting to main menu.")
            break

def game_menu():
    """
    Display game menu and get player choice
    """
    # TODO: Implement game menu

    while True:
        print("\n=== GAME MENU ===")
        print("1. View Character Stats")
        print("2. View Inventory")
        print("3. Quest Menu")
        print("4. Explore (Find Battles)")
        print("5. Shop")
        print("6. Save and Quit")

        choice_str = input("Choose an option (1-6): ").strip()

        try:
            choice = int(choice_str)
        except ValueError:
            print("Please enter a valid number between 1 and 6.")
            continue

        if 1 <= choice <= 6:
            return choice
        else:
            print("Invalid choice. Try again.")

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character
    
    # TODO: Implement stats display
    # Show: name, class, level, health, stats, gold, etc.
    # Use character_manager functions
    # Show quest progress using quest_handler

    if current_character is None:
        print("No character loaded.")
        return

    c = current_character
    print("\n=== CHARACTER STATS ===")
    print(f"Name: {c.get('name')}")
    print(f"Class: {c.get('class')}")
    print(f"Level: {c.get('level')}")
    print(f"Health: {c.get('health')}/{c.get('max_health')}")
    print(f"Strength: {c.get('strength')}")
    print(f"Magic: {c.get('magic')}")
    print(f"Gold: {c.get('gold')}")

    # Simple quest progress display using stored lists
    print(f"Active Quests: {c.get('active_quests', [])}")
    print(f"Completed Quests: {c.get('completed_quests', [])}")

def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    
    # TODO: Implement inventory menu
    # Show current inventory
    # Options: Use item, Equip weapon/armor, Drop item
    # Handle exceptions from inventory_system

    if current_character is None:
        print("No character loaded.")
        return

    print("\n=== INVENTORY ===")
    inventory_system.display_inventory(current_character, all_items)

    # For now, keep it simple: just display. No interactive use/equip here.
    # (Tests don't require interactive menu from main.)

def quest_menu():
    """Quest management menu"""
    global current_character, all_quests
    
    # TODO: Implement quest menu
    # Show:
    #   1. View Active Quests
    #   2. View Available Quests
    #   3. View Completed Quests
    #   4. Accept Quest
    #   5. Abandon Quest
    #   6. Complete Quest (for testing)
    #   7. Back
    # Handle exceptions from quest_handler

    if current_character is None:
        print("No character loaded.")
        return

    while True:
        print("\n=== QUEST MENU ===")
        print("1. View Active Quests")
        print("2. View Available Quests")
        print("3. View Completed Quests")
        print("4. Accept Quest")
        print("5. Abandon Quest")
        print("6. Complete Quest (for testing)")
        print("7. Back")

        choice_str = input("Choose an option (1-7): ").strip()

        try:
            choice = int(choice_str)
        except ValueError:
            print("Enter a number 1-7.")
            continue

        if choice == 1:
            active = quest_handler.get_active_quests(current_character)
            print("Active quests:", active)
        elif choice == 2:
            available = quest_handler.get_available_quests(current_character, all_quests)
            print("Available quests:", available)
        elif choice == 3:
            print("Completed quests:", current_character.get("completed_quests", []))
        elif choice == 4:
            quest_id = input("Enter quest ID to accept: ").strip()
            try:
                quest_handler.accept_quest(current_character, quest_id, all_quests)
                print(f"Accepted quest '{quest_id}'.")
            except QuestError as e:
                print(f"Could not accept quest: {e}")
        elif choice == 5:
            quest_id = input("Enter quest ID to abandon: ").strip()
            try:
                quest_handler.abandon_quest(current_character, quest_id)
                print(f"Abandoned quest '{quest_id}'.")
            except QuestError as e:
                print(f"Could not abandon quest: {e}")
        elif choice == 6:
            quest_id = input("Enter quest ID to complete: ").strip()
            try:
                quest_handler.complete_quest(current_character, quest_id, all_quests)
                print(f"Completed quest '{quest_id}'.")
            except QuestError as e:
                print(f"Could not complete quest: {e}")
        elif choice == 7:
            break
        else:
            print("Invalid choice.")

def explore():
    """Find and fight random enemies"""
    global current_character
    
    # TODO: Implement exploration
    # Generate random enemy based on character level
    # Start combat with combat_system.SimpleBattle
    # Handle combat results (XP, gold, death)
    # Handle exceptions

    if current_character is None:
        print("No character loaded.")
        return

    print("\n=== EXPLORING... ===")
    # Create a level-appropriate enemy
    enemy = combat_system.get_random_enemy_for_level(current_character.get("level", 1))
    print(f"You encountered a {enemy['name']}!")

    battle = combat_system.SimpleBattle(current_character, enemy)
    try:
        result = battle.start_battle()
    except CharacterDeadError:
        print("You were already dead...")
        return

    print(f"Battle finished! Winner: {result['winner']}")

    if result["winner"] == "player":
        # Apply rewards using character_manager functions
        xp = result["xp_gained"]
        gold = result["gold_gained"]
        print(f"You gained {xp} XP and {gold} gold!")
        try:
            character_manager.gain_experience(current_character, xp)
        except CharacterDeadError:
            # Shouldn't happen here, but just in case
            print("Cannot gain XP; character is dead.")
        character_manager.add_gold(current_character, gold)
    else:
        handle_character_death()

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    
    # TODO: Implement shop
    # Show available items for purchase
    # Show current gold
    # Options: Buy item, Sell item, Back
    # Handle exceptions from inventory_system

    if current_character is None:
        print("No character loaded.")
        return

    while True:
        print("\n=== SHOP ===")
        print(f"Your gold: {current_character.get('gold', 0)}")
        print("Items for sale:")
        for item_id, data in all_items.items():
            print(f"- {item_id} ({data.get('name')}) - Cost: {data.get('cost')}")

        print("\nOptions:")
        print("1. Buy item")
        print("2. Sell item")
        print("3. Back")

        choice_str = input("Choose an option (1-3): ").strip()

        try:
            choice = int(choice_str)
        except ValueError:
            print("Enter a number 1-3.")
            continue

        if choice == 1:
            item_id = input("Enter item ID to buy: ").strip()
            if item_id not in all_items:
                print("That item does not exist.")
                continue
            try:
                inventory_system.purchase_item(current_character, item_id, all_items[item_id])
                print(f"Purchased {item_id}.")
            except (InsufficientResourcesError, InventoryFullError) as e:
                print(f"Could not purchase item: {e}")
        elif choice == 2:
            item_id = input("Enter item ID to sell: ").strip()
            if item_id not in all_items:
                print("That item does not exist in the item list.")
                continue
            try:
                gold_received = inventory_system.sell_item(current_character, item_id, all_items[item_id])
                print(f"Sold {item_id} for {gold_received} gold.")
            except ItemNotFoundError as e:
                print(f"Could not sell item: {e}")
        elif choice == 3:
            break
        else:
            print("Invalid choice.")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    
    # TODO: Implement save
    # Use character_manager.save_character()
    # Handle any file I/O exceptions

    if current_character is None:
        print("No character to save.")
        return

    try:
        character_manager.save_character(current_character)
        print("Game saved successfully.")
    except Exception as e:
        print(f"Could not save game: {e}")

def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    
    # TODO: Implement data loading
    # Try to load quests with game_data.load_quests()
    # Try to load items with game_data.load_items()
    # Handle MissingDataFileError, InvalidDataFormatError
    # If files missing, create defaults with game_data.create_default_data_files()

    # Let MissingDataFileError / InvalidDataFormatError bubble up
    # so main() can handle them in one place, as already written.
    all_quests = game_data.load_quests("data/quests.txt")
    all_items = game_data.load_items("data/items.txt")

def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    
    # TODO: Implement death handling
    # Display death message
    # Offer: Revive (costs gold) or Quit
    # If revive: use character_manager.revive_character()
    # If quit: set game_running = False

    print("\nYou have fallen in battle!")
    if current_character is None:
        game_running = False
        return

    # Simple logic: if player has at least 50 gold, offer revive
    if current_character.get("gold", 0) >= 50:
        choice = input("Spend 50 gold to revive? (y/n): ").strip().lower()
        if choice == "y":
            current_character["gold"] -= 50
            character_manager.revive_character(current_character)
            print("You have been revived!")
            return

    print("Game over.")
    game_running = False

def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()
