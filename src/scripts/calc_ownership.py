from typing import List, Dict, Tuple, Set
from src.models.path import Path

def calculate_ownership(paths: List[Path]) -> None:
    """
    Calculate real ownership for each company leading to the focus company with depth = 0.
    """
    # Identify the focus company (depth = 0)
    focus_ids = {path.target for path in paths if path.target_depth == 0}
    if not focus_ids:
        raise ValueError("No company with depth = 0 found.")
    if len(focus_ids) > 1:
        raise ValueError("Multiple companies with depth = 0 found.")

    focus_id = focus_ids.pop()

    # Build a graph: {target: [(source, Path)]} (reversed for traversal)
    reverse_graph: Dict[int, List[Tuple[int, Path]]] = {}
    for path in paths:
        if not path.active:
            continue
        if path.target not in reverse_graph:
            reverse_graph[path.target] = []
        reverse_graph[path.target].append((path.source, path))

    # Ownership tracking: {source: (lower, average, upper)}
    ownership: Dict[int, Tuple[float, float, float]] = {focus_id: (1.0, 1.0, 1.0)}

    visited: Set[int] = set()  # Track visited nodes to avoid infinite loops

    def propagate_ownership(node: int):
        """
        Propagate ownership values up the chain, avoiding cycles.
        """
        if node in visited:
            return  # Prevent infinite recursion due to cycles

        visited.add(node)

        if node not in reverse_graph:
            return  # No incoming paths, stop propagation

        for source, path in reverse_graph[node]:
            lower, avg, upper = path.parse_share_range()

            # Calculate propagated ownership
            target_lower, target_avg, target_upper = ownership[node]
            real_lower = target_lower * (lower / 100)
            real_avg = target_avg * (avg / 100)
            real_upper = target_upper * (upper / 100)

            # Update ownership for the source node
            if source not in ownership:
                ownership[source] = (real_lower, real_avg, real_upper)
            else:
                current_lower, current_avg, current_upper = ownership[source]
                ownership[source] = (
                    current_lower + real_lower,
                    current_avg + real_avg,
                    current_upper + real_upper,
                )

            # Recursively propagate ownership
            propagate_ownership(source)

    # Start ownership propagation from the focus company
    propagate_ownership(focus_id)

    # Update the real ownership in the Path objects as percentages
    for path in paths:
        if path.source in ownership:
            real_lower, real_average, real_upper = ownership[path.source]
            path.real_lower_share = f"{real_lower * 100:.2f}%"  # Convert to percentage
            path.real_average_share = f"{real_average * 100:.2f}%"  # Convert to percentage
            path.real_upper_share = f"{real_upper * 100:.2f}%"  # Convert to percentage
        else:
            path.real_lower_share = "N/A"
            path.real_average_share = "N/A"
            path.real_upper_share = "N/A"