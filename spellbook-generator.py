import random
import csv
import os
from pathlib import Path
import math

def get_spell_lists():
    """
    Get list of available spell list files from the spell-lists directory.
    
    :return: List of available spell list filenames
    """
    spell_lists_dir = Path('spell-lists')
    if not spell_lists_dir.exists():
        print("Creating spell-lists directory...")
        spell_lists_dir.mkdir(exist_ok=True)
        print("Please add spell list CSV files to the spell-lists directory.")
        return []
    
    return [f.name for f in spell_lists_dir.glob('*.csv')]

def load_spells_from_csv(filename):
    """
    Load spells from a CSV file in the spell-lists directory.
    
    :param filename: Name of the CSV file
    :return: Dictionary with spell levels as keys and lists of spells as values
    """
    spells_by_level = {1: [], 2: [], 3: []}
    filepath = Path('spell-lists') / filename
    
    try:
        with open(filepath, 'r') as file:
            reader = csv.reader(file)
            for index, row in enumerate(reader, start=1):
                if index <= 3:  # Only process first 3 levels
                    spells_by_level[index] = [spell.strip() for spell in row if spell.strip()]
        return spells_by_level
    except FileNotFoundError:
        print(f"Error: Could not find {filename} in the spell-lists directory.")
        return None

def get_available_spell_levels(char_level):
    """
    Determine available spell levels based on character level.
    
    :param char_level: Character level of the magic-user
    :return: List of available spell levels
    """
    if char_level <= 2:
        return [1]
    elif char_level <= 4:
        return [1, 2]
    else:
        return [1, 2, 3]

def generate_spellbook(primary_spells, secondary_spells, char_level, int_modifier):
    """
    Generate a spellbook using spells from both primary and secondary sources.
    
    :param primary_spells: Dictionary of spells from primary source
    :param secondary_spells: Dictionary of spells from secondary source
    :param char_level: Character level of the magic-user
    :param int_modifier: Intelligence modifier of the magic-user
    :return: Dictionary of selected spells organized by level
    """
    spellbook = {1: ["Read Magic"], 2: [], 3: []}
    
    for level in range(1, char_level + 1):
        total_spells = max(1, 1 + int_modifier)  # Minimum 1 spell per level
        primary_count = math.ceil(total_spells * 2/3)
        secondary_count = total_spells - primary_count
        
        available_levels = get_available_spell_levels(level)
        
        # Add spells from primary source
        for _ in range(primary_count):
            spell_level = random.choice(available_levels)
            available_spells = [spell for spell in primary_spells[spell_level] 
                              if spell not in spellbook[spell_level]]
            if available_spells:
                new_spell = random.choice(available_spells)
                spellbook[spell_level].append(new_spell)
        
        # Add spells from secondary source
        for _ in range(secondary_count):
            spell_level = random.choice(available_levels)
            available_spells = [spell for spell in secondary_spells[spell_level] 
                              if spell not in spellbook[spell_level]]
            if available_spells:
                new_spell = random.choice(available_spells)
                spellbook[spell_level].append(new_spell)
    
    return {level: spells for level, spells in spellbook.items() if spells}

def print_spellbook(spellbook):
    """
    Print the generated spellbook in a compact, single-line format.
    """
    output = []
    for level in sorted(spellbook.keys()):
        if spellbook[level]:
            spells = ", ".join(sorted(spellbook[level]))  # Sort spells alphabetically
            output.append(f"{level}: {spells}")
    
    formatted_output = "; ".join(output)
    print(f"{formatted_output}.")
    
def select_spell_list(prompt):
    """
    Prompt user to select a spell list from available options.
    
    :param prompt: Custom prompt message for selection
    :return: Selected spell list filename or None if no valid selection
    """
    spell_lists = get_spell_lists()
    
    if not spell_lists:
        return None
    
    print(f"\n{prompt}")
    for i, filename in enumerate(spell_lists, 1):
        print(f"{i}. {filename}")
    
    while True:
        try:
            choice = int(input("\nSelect a spell list (enter the number): "))
            if 1 <= choice <= len(spell_lists):
                return spell_lists[choice - 1]
            print("Please enter a valid number from the list.")
        except ValueError:
            print("Please enter a valid number.")

# Main execution
if __name__ == "__main__":
    print("D&D Magic-User Spellbook Generator")
    print("----------------------------------")
    
    while True:
        # Select primary spell list
        primary_list = select_spell_list("Select PRIMARY spell list (2/3 of spells will come from this):")
        if not primary_list:
            print("\nNo spell lists available. Please add CSV files to the spell-lists directory.")
            break
        
        # Select secondary spell list
        secondary_list = select_spell_list("Select SECONDARY spell list (1/3 of spells will come from this):")
        if not secondary_list:
            break
            
        primary_spells = load_spells_from_csv(primary_list)
        secondary_spells = load_spells_from_csv(secondary_list)
        if not primary_spells or not secondary_spells:
            break
            
        try:
            char_level = int(input("\nEnter the level of the Magic-User (1-6), or 0 to quit: "))
            if char_level == 0:
                print("Thank you for using the Spellbook Generator. Goodbye!")
                break
            if char_level < 1 or char_level > 6:
                print("Please enter a valid level between 1 and 6.")
                continue
            
            int_modifier = int(input("Enter the Intelligence modifier (-2, -1, 0, +1, or +2): "))
            if int_modifier not in [-2, -1, 0, 1, 2]:
                print("Please enter a valid Intelligence modifier (-2, -1, 0, +1, or +2).")
                continue
            
            print(f"\nUsing primary list: {primary_list}")
            print(f"Using secondary list: {secondary_list}")
            generated_spellbook = generate_spellbook(primary_spells, secondary_spells, char_level, int_modifier)
            print(f"Generated Spellbook for level {char_level} Magic-User with INT modifier {int_modifier}:")
            print_spellbook(generated_spellbook)
            print()
        except ValueError:
            print("Please enter valid numbers.")