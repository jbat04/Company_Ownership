from typing import Tuple, List

class Path:
    def __init__(self, json_data):
        self.id = json_data.get("id")
        self.source = json_data.get("source")
        self.source_name = json_data.get("source_name")
        self.source_depth = json_data.get("source_depth")
        self.target = json_data.get("target")
        self.target_name = json_data.get("target_name")
        self.target_depth = json_data.get("target_depth")
        self.share = json_data.get("share")
        self.real_lower_share = json_data.get("real_lower_share")
        self.real_average_share = json_data.get("real_average_share")
        self.real_upper_share = json_data.get("real_upper_share")
        self.active = json_data.get("active")
        self.owns = False

    def __repr__(self):
        return (f"Path(id={self.id}, source={self.source}, source_name={self.source_name}, "
                f"source_depth={self.source_depth}, target={self.target}, target_name={self.target_name}, "
                f"target_depth={self.target_depth}, share={self.share}, real_lower_share={self.real_lower_share}, "
                f"real_average_share={self.real_average_share}, real_upper_share={self.real_upper_share}, "
                f"active={self.active})")

def pretty_print_paths(paths: List[Path], focus_id, focus_name) -> None:
    """
    Pretty print a list of Path objects in a tabular format.
    """
    print("-" * 125)
    print(f"Ownership for: {focus_name}")
    print("-" * 125)
    print(f"{'Entity Name':<80} {'Lower Share':<12} {'Average Share':<15} {'Upper Share':<12}")
    print("-" * 125)
    for path in paths:
        if path.owns:
            print(f"{path.target_name:<80} "
              f"-{path.real_lower_share or 'N/A':<12} "
              f"-{path.real_average_share or 'N/A':<15} "
              f"-{path.real_upper_share or 'N/A':<12}")
        else:
            print(f"{path.source_name:<80} "
              f"{path.real_lower_share or 'N/A':<12} "
              f"{path.real_average_share or 'N/A':<15} "
              f"{path.real_upper_share or 'N/A':<12}")
        # Use target_name if .owns is True, otherwise use source_name
        # entity_name = f"{path.target_name}" if path.owns else path.source_name
        # print(f"{entity_name:<80} "
        #       f"{path.real_lower_share or 'N/A':<12} "
        #       f"{path.real_average_share or 'N/A':<15} "
        #       f"{path.real_upper_share or 'N/A':<12}")
        
def parse_share_range(share) -> Tuple[float, float, float]:
        """
        Parse the share range into lower, average, and upper values.
        """
        if not share:
            return 0, 0, 0
        if share == "<5%":
            return 0, 2.5, 5
        try:
            if "-" in share:
                lower, upper = map(lambda x: float(x.strip("%")), share.split("-"))
                return lower, (lower + upper) / 2, upper
            else:
                # Handle single percentage values like "10%"
                value = float(share.strip("%"))
                return value, value, value
        except ValueError:
            print(f"Warning: Malformed share range '{share}'. Defaulting to 0.")
            return 0, 0, 0