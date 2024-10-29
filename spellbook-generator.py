import random
import csv

def load_spells_from_csv(filename):
    """
    Load spells from a CSV file.
    Each line in the file represents a spell level, with spells comma-separated.
    
    :param filename: Name of the CSV file
    :return: Dictionary with spell levels as keys and lists of spells as values
    """
    spells_by_level = {1: [], 2: [], 3: []}
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for index, row in enumerate(reader, start=1):
            if index <= 3:  # Only process first 3 levels
                spells_by_level[index] = [spell.strip() for spell in row if spell.strip()]
    return spells_by_level

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

def generate_spellbook(spells_by_level, char_level, int_modifier):
    """
    Generate a spellbook for a magic-user based on their character level and INT modifier.
    
    :param spells_by_level: Dictionary of spells organized by level
    :param char_level: Character level of the magic-user
    :param int_modifier: Intelligence modifier of the magic-user
    :return: Dictionary of selected spells organized by level
    """
    spellbook = {1: ["Read Magic"], 2: [], 3: []}
    
    for level in range(1, char_level + 1):
        spells_to_add = max(1, 1 + int_modifier)  # Minimum 1 spell per level
        available_levels = get_available_spell_levels(level)
        
        for _ in range(spells_to_add):
            spell_level = random.choice(available_levels)
            available_spells = [spell for spell in spells_by_level[spell_level] if spell not in spellbook[spell_level]]
            if available_spells:
                new_spell = random.choice(available_spells)
                spellbook[spell_level].append(new_spell)
    
    return {level: spells for level, spells in spellbook.items() if spells}

def print_spellbook(spellbook):
    """
    Print the generated spellbook in a compact, single-line format.
    
    :param spellbook: Dictionary of spells organized by level
    """
    output = []
    for level in sorted(spellbook.keys()):
        if spellbook[level]:
            spells = ", ".join(spellbook[level])
            output.append(f"{level}: {spells}")
    
    formatted_output = "; ".join(output)
    print(f"{formatted_output}.")

# Main execution
if __name__ == "__main__":
    filename = "black-magic-spells.csv"
    spells_by_level = load_spells_from_csv(filename)

    while True:
        try:
            char_level = int(input("Enter the level of the Magic-User (1-6), or 0 to quit: "))
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
            
            generated_spellbook = generate_spellbook(spells_by_level, char_level, int_modifier)
            print(f"\nGenerated Spellbook for level {char_level} Magic-User with INT modifier {int_modifier}:")
            print_spellbook(generated_spellbook)
            print()  # Add a blank line for readability
        except ValueError:
            print("Please enter valid numbers.")