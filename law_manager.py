
# Dictionary to store law references and their descriptions
law_dictionary = {}

# Load laws from a text file into the law dictionary
def load_data():
    try:
        with open("laws.txt", "r") as file:
            for line in file:
                law_code, law_description = line.split(" ", 1)
                law_dictionary[law_code] = law_description.strip()
    except FileNotFoundError:
        print("File does not exist! Starting with an empty dictionary.")

# Save updated law dictionary to the file
def save_data():
    try:
        with open("laws.txt", "w") as file:
            for law_code, law_description in law_dictionary.items():
                file.write(f"{law_code} {law_description}\n")
    except Exception as e:
        print(f"Error saving data: {e}")

# Function to get all law codes sorted alphabetically
def get_sorted_law_codes():
    """Return the law codes sorted alphabetically."""
    return sorted(law_dictionary.keys())

# Function to get the description of a specific law code
def get_law_description(law_code):
    """Return the description of the law code."""
    return law_dictionary.get(law_code, "Description not available.")
