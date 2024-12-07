import json
import os
from src.models.path import Path, pretty_print_paths
from src.scripts.calc_ownership_v2 import calculate_ownership

# Filter JSON files in the "data" directory
file_index = 1
json_files = [file for file in os.listdir("data") if file.endswith('.json')]

# Display files with numbering
for file in json_files:
    print(f"{file_index}. {file}") 
    file_index += 1

# Handle user input
try:
    input_choice = input("Choose file # (e.g., 1): ")
    choice_index = int(input_choice) - 1

    # Ensure the choice is within the valid range
    if choice_index < 0 or choice_index >= len(json_files):
        raise IndexError("Invalid file number.")
    

    file = json_files[choice_index]
    paths = []

    # Load and process the selected JSON file
    with open(f'data/{file}', 'r') as f:
        network = json.load(f)
        for json_path in network:
            if "source" not in json_path or "target" not in json_path or "share" not in json_path:
                print(f"Warning: Skipping malformed entry: {json_path}")
                continue
            paths.append(Path(json_path)) 

    calculate_ownership(paths)
    pretty_print_paths(paths)

except (ValueError, IndexError) as e:
    print(f"Error: {e}. Please provide a valid file number.")

except FileNotFoundError:
    print("Error: 'data' directory or the selected file was not found.")

except json.JSONDecodeError:
    print("Error: Failed to decode the JSON file. Ensure the file is properly formatted.")
