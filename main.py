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
    with open(f'data/{file}', 'r', encoding="utf-8") as f:
        network = json.load(f)
        for json_path in network:
            if "source" not in json_path or "target" not in json_path or "share" not in json_path:
                print(f"Warning: Skipping malformed entry: {json_path}")
                continue
            paths.append(Path(json_path)) 

    focus_id,focus_name = calculate_ownership(paths)
    pretty_print_paths(paths, focus_id,focus_name)


    # Save updated paths back to the same file
    updated_network = [
        {
            "id": path.id,
            "source": path.source,
            "source_name": path.source_name,
            "source_depth": path.source_depth,
            "target": path.target,
            "target_name": path.target_name,
            "target_depth": path.target_depth,
            "share": path.share,
            "real_lower_share": path.real_lower_share,
            "real_average_share": path.real_average_share,
            "real_upper_share": path.real_upper_share,
            "active": path.active,
        }
        for path in paths
    ]

    # Save to the same file, overwriting the original
    with open(f'data/{file}', 'w', encoding="utf-8") as f:
        json.dump(updated_network, f, ensure_ascii=False, indent=4)

except (ValueError, IndexError) as e:
    print(f"Error: {e}. Please provide a valid file number.")

except FileNotFoundError:
    print("Error: 'data' directory or the selected file was not found.")

except json.JSONDecodeError:
    print("Error: Failed to decode the JSON file. Ensure the file is properly formatted.")
