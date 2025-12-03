"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: Bryant Clarke

AI Usage: AI helped with syntax formatting and error checking

This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)

import character_manager  # Needed to grant XP and gold on quest completion

# Helper to treat "NONE" / "None" / "" as no prerequisite
_NO_PREREQ_VALUES = {"NONE", "None", "none", "", None}

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    """
    Accept a new quest
    """
    # TODO: Implement quest acceptance
    # Check quest exists\
    # Check level requirement
    # Check prerequisite (if not "NONE")
    # Check not already completed
    # Check not already active
    # Add to character['active_quests']

    if quest_id not in quest_data_dict:
        # Used by test_quest_not_found_exception
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")

    quest = quest_data_dict[quest_id]

    # Make sure lists exist
    active = character.setdefault("active_quests", [])
    completed = character.setdefault("completed_quests", [])

    # If already completed, we can't accept again
    if quest_id in completed:
        # Used by test_quest_already_completed_exception
        raise QuestAlreadyCompletedError(f"Quest '{quest_id}' already completed.")

    # If already active, we just don't add it again (no error needed for tests)
    if quest_id in active:
        return False

    # Level requirement check
    if character.get("level", 1) < quest.get("required_level", 1):
        # Used by test_insufficient_level_exception
        raise InsufficientLevelError("Character level too low for this quest.")

    # Prerequisite requirement
    prereq_id = quest.get("prerequisite", "NONE")
    if prereq_id not in _NO_PREREQ_VALUES:
        if prereq_id not in completed:
            # Used by test_quest_requirements_not_met_exception
            raise QuestRequirementsNotMetError(
                f"Prerequisite quest '{prereq_id}' not completed."
            )

    # If all checks pass, add quest to active list
    active.append(quest_id)
    return True

def complete_quest(character, quest_id, quest_data_dict):
    """
    Complete an active quest and grant rewards
    """
    # TODO: Implement quest completion
    # Check quest exists
    # Check quest is active
    # Remove from active_quests
    # Add to completed_quests
    # Grant rewards (use character_manager.gain_experience and add_gold)
    # Return reward summary

    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")

    quest = quest_data_dict[quest_id]

    active = character.setdefault("active_quests", [])
    completed = character.setdefault("completed_quests", [])

    if quest_id not in active:
        # Used by test_quest_not_active_exception
        raise QuestNotActiveError(f"Quest '{quest_id}' is not active.")

    # Remove from active and mark completed
    active.remove(quest_id)
    if quest_id not in completed:
        completed.append(quest_id)

    # Rewards come from quest data
    xp = quest.get("reward_xp", 0)
    gold = quest.get("reward_gold", 0)

    # Use character_manager functions so leveling & gold rules stay consistent
    character_manager.gain_experience(character, xp)
    character_manager.add_gold(character, gold)

    return {"xp": xp, "gold": gold}

def abandon_quest(character, quest_id):
    """
    Remove a quest from active quests without completing it
    """
    # TODO: Implement quest abandonment

    active = character.setdefault("active_quests", [])

    if quest_id not in active:
        raise QuestNotActiveError(f"Quest '{quest_id}' is not active.")

    active.remove(quest_id)
    return True

def get_active_quests(character, quest_data_dict):
    """
    Get full data for all active quests
    """
    # TODO: Implement active quest retrieval
    # Look up each quest_id in character['active_quests']
    # Return list of full quest data dictionaries

    active_ids = character.get("active_quests", [])
    result = []
    for qid in active_ids:
        if qid in quest_data_dict:
            result.append(quest_data_dict[qid])
    return result

def get_completed_quests(character, quest_data_dict):
    """
    Get full data for all completed quests
    """
    # TODO: Implement completed quest retrieval

    completed_ids = character.get("completed_quests", [])
    result = []
    for qid in completed_ids:
        if qid in quest_data_dict:
            result.append(quest_data_dict[qid])
    return result

def get_available_quests(character, quest_data_dict):
    """
    Get quests that character can currently accept
    """
    # TODO: Implement available quest search
    # Filter all quests by requirements

    available = []
    for quest_id in quest_data_dict:
        if can_accept_quest(character, quest_id, quest_data_dict):
            available.append(quest_data_dict[quest_id])
    return available

# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    """
    Check if a specific quest has been completed
    """
    # TODO: Implement completion check

    return quest_id in character.get("completed_quests", [])

def is_quest_active(character, quest_id):
    """
    Check if a specific quest is currently active
    """
    # TODO: Implement active check

    return quest_id in character.get("active_quests", [])

def can_accept_quest(character, quest_id, quest_data_dict):
    """
    Check if character meets all requirements to accept quest
    """
    # TODO: Implement requirement checking
    # Check all requirements without raising exceptions

    if quest_id not in quest_data_dict:
        return False

    quest = quest_data_dict[quest_id]
    level = character.get("level", 1)

    # Already completed or active => can't accept
    if is_quest_completed(character, quest_id):
        return False
    if is_quest_active(character, quest_id):
        return False

    # Level requirement
    if level < quest.get("required_level", 1):
        return False

    # Prerequisite requirement
    prereq_id = quest.get("prerequisite", "NONE")
    if prereq_id not in _NO_PREREQ_VALUES:
        if not is_quest_completed(character, prereq_id):
            return False

    return True

def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    """
    Get the full chain of prerequisites for a quest
    """
    # TODO: Implement prerequisite chain tracing
    # Follow prerequisite links backwards
    # Build list in reverse order

    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")

    chain = []
    current_id = quest_id

    # Walk backwards through prerequisites until there is none
    while True:
        if current_id not in quest_data_dict:
            # If a prereq points to something invalid, raise
            raise QuestNotFoundError(f"Quest '{current_id}' not found in chain.")

        chain.append(current_id)
        prereq_id = quest_data_dict[current_id].get("prerequisite", "NONE")

        if prereq_id in _NO_PREREQ_VALUES:
            break

        current_id = prereq_id

    # We built from quest → earliest; reverse to get earliest → quest
    chain.reverse()
    return chain

# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    """
    Calculate what percentage of all quests have been completed
    """
    # TODO: Implement percentage calculation
    # total_quests = len(quest_data_dict)
    # completed_quests = len(character['completed_quests'])
    # percentage = (completed / total) * 100

    total = len(quest_data_dict)
    if total == 0:
        return 0.0

    # Only count completed quests that actually exist in quest_data_dict
    completed_ids = character.get("completed_quests", [])
    completed_count = sum(1 for qid in completed_ids if qid in quest_data_dict)

    return (completed_count / total) * 100.0

def get_total_quest_rewards_earned(character, quest_data_dict):
    """
    Calculate total XP and gold earned from completed quests
    """
    # TODO: Implement reward calculation
    # Sum up reward_xp and reward_gold for all completed quests

    total_xp = 0
    total_gold = 0

    for qid in character.get("completed_quests", []):
        quest = quest_data_dict.get(qid)
        if quest is not None:
            total_xp += quest.get("reward_xp", 0)
            total_gold += quest.get("reward_gold", 0)

    return {"total_xp": total_xp, "total_gold": total_gold}

def get_quests_by_level(quest_data_dict, min_level, max_level):
    """
    Get all quests within a level range
    """
    # TODO: Implement level filtering

    result = []
    for quest in quest_data_dict.values():
        lvl = quest.get("required_level", 1)
        if min_level <= lvl <= max_level:
            result.append(quest)
    return result

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    """
    Display formatted quest information
    """
    # TODO: Implement quest display
    print(f"\n=== {quest_data['title']} ===")
    print(f"Description: {quest_data['description']}")
    # ... etc
    print(f"Required Level: {quest_data.get('required_level', 1)}")
    print(f"Rewards: {quest_data.get('reward_xp', 0)} XP, {quest_data.get('reward_gold', 0)} gold")
    prereq = quest_data.get("prerequisite", "NONE")
    if prereq in _NO_PREREQ_VALUES:
        prereq_text = "None"
    else:
        prereq_text = prereq
    print(f"Prerequisite: {prereq_text}")

def display_quest_list(quest_list):
    """
    Display a list of quests in summary format
    """
    # TODO: Implement quest list display

    if not quest_list:
        print("No quests to display.")
        return

    print("\n=== QUEST LIST ===")
    for quest in quest_list:
        print(
            f"- {quest.get('title')} "
            f"(Level {quest.get('required_level', 1)}, "
            f"{quest.get('reward_xp', 0)} XP, {quest.get('reward_gold', 0)} gold)"
        )

def display_character_quest_progress(character, quest_data_dict):
    """
    Display character's quest statistics and progress
    """
    # TODO: Implement progress display

    active_count = len(character.get("active_quests", []))
    completed_count = len(character.get("completed_quests", []))
    percent = get_quest_completion_percentage(character, quest_data_dict)
    totals = get_total_quest_rewards_earned(character, quest_data_dict)

    print("\n=== QUEST PROGRESS ===")
    print(f"Active quests: {active_count}")
    print(f"Completed quests: {completed_count}")
    print(f"Completion: {percent:.1f}%")
    print(f"Total rewards earned: {totals['total_xp']} XP, {totals['total_gold']} gold")

# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    """
    Validate that all quest prerequisites exist
    """
    # TODO: Implement prerequisite validation
    # Check each quest's prerequisite
    # Ensure prerequisite exists in quest_data_dict

    for quest_id, quest in quest_data_dict.items():
        prereq = quest.get("prerequisite", "NONE")
        if prereq in _NO_PREREQ_VALUES:
            continue
        if prereq not in quest_data_dict:
            # If a quest references a non-existent prerequisite, raise
            raise QuestNotFoundError(
                f"Quest '{quest_id}' has invalid prerequisite '{prereq}'."
            )
    return True


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
