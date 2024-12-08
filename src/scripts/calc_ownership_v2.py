from typing import List, Dict, Tuple, Set
from src.models.path import Path, parse_share_range

def calculate_ownership(paths: List[Path]) -> None:
    """
    Calculate real ownership for each company leading to the focus company with depth = 0.
    """
    # Identify the focus company (depth = 0)
    focus_nodes = [path for path in paths if path.target_depth == 0]
    if not focus_nodes:
        raise ValueError("No company with depth = 0 found.")
    
    focus_node = focus_nodes[0]
    focus_name = focus_node.target_name
    focus_id = focus_node.target

    # Ownership tracking: {source: (lower, average, upper)}
    ownership: Dict[int, Tuple[float, float, float]] = {}
    # Ownership tracking: {tracking: (lower, average, upper)}
    owneeship: Dict[int, Tuple[float, float, float]] = {}
    visited: Set[int] = set()  # Track visited nodes to avoid infinite loops


    def set_real_rates(current_source, ship, path):
            lower, avg, upper = parse_share_range(path.share)
            # Calculate propagated ownership

            try: #if it exists in owenershop alrady
                current_lower, current_avg, current_upper = ownership[current_source] if ship=="owned" else owneeship[current_source]
                current_lower = current_lower * (lower / 100)
                current_avg = current_avg * (avg / 100)
                current_upper = current_upper * (upper / 100)
                if(ship == "owns"):
                    owneeship[current_source] = ((current_lower), (current_avg), (current_upper))
                else:
                    ownership[current_source] = ((current_lower), (current_avg), (current_upper))
            except KeyError:
                if(ship == "owns"):
                    owneeship[current_source] = ((lower / 100), (avg / 100), (upper / 100))
                else:
                    ownership[current_source] = ((lower / 100), (avg / 100), (upper / 100))

    def propagate_ownership():
        for path in paths:
            visited: Set[int] = set()  # Track visited nodes to avoid infinite loops
            if(path.target_depth >=0):
                set_real_rates(path.source, "owned", path)
                current_shipper = path.source
                next_source = path.target
                if(path.target_depth == 0):
                    continue
                current_node = next((path_i for path_i in paths if path_i.source == next_source and path_i.target_depth == path.target_depth-1), None)
                current_target_depth = current_node.target_depth
                while(current_target_depth >= 0):
                    # if current_node in visited:
                    #     return  # Prevent infinite recursion due to cycles
                    # visited.add(current_node)
                    set_real_rates(current_shipper, "owned", current_node)
            
                    next_source = current_node.target
                    current_node = next((path_i for path_i in paths if path_i.source == next_source and path_i.target_depth == current_node.target_depth-1), None)
                    if current_node:
                        current_target_depth = current_node.target_depth
                    else:
                        break

            else:
                set_real_rates(path.target, "owns", path)
                current_shipper = path.target
                next_target = path.source
                current_node = next((path_i for path_i in paths if path_i.target == next_target and path_i.target_depth == path.target_depth+1), None)
                if(current_node):
                    current_source_depth = current_node.source_depth
                    while(current_source_depth <= 0):
                        # if current_node in visited:
                        #     return  # Prevent infinite recursion due to cycles
                        # visited.add(current_node)
                        set_real_rates(current_shipper, "owns", current_node)
                
                        next_target = current_node.source
                        current_node = next((path_i for path_i in paths if path_i.target == next_target and path_i.target_depth == path.target_depth+1), None)
                        if current_node:
                            current_source_depth = current_node.source_depth
                        else:
                            break



    propagate_ownership()

    # Update the real ownership in the Path objects as percentages
    for path in paths:
        if path.source in ownership and path.target_depth>=0:
            real_lower, real_average, real_upper = ownership[path.source]
            path.real_lower_share = f"{real_lower * 100:.2f}%"  # Convert to percentage
            path.real_average_share = f"{real_average * 100:.2f}%"  # Convert to percentage
            path.real_upper_share = f"{real_upper * 100:.2f}%"  # Convert to percentage
        elif path.target in owneeship and path.target_depth<0:
            real_lower, real_average, real_upper = owneeship[path.target]
            path.real_lower_share = f"{real_lower * 100:.2f}%"  # Convert to percentage
            path.real_average_share = f"{real_average * 100:.2f}%"  # Convert to percentage
            path.real_upper_share = f"{real_upper * 100:.2f}%"  # Convert to percentage
            path.owns = True
        else:
            path.real_lower_share = "N/A"
            path.real_average_share = "N/A"
            path.real_upper_share = "N/A"

    return focus_id, focus_name