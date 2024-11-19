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

    def __repr__(self):
        return (f"Path(id={self.id}, source={self.source}, source_name={self.source_name}, "
                f"source_depth={self.source_depth}, target={self.target}, target_name={self.target_name}, "
                f"target_depth={self.target_depth}, share={self.share}, real_lower_share={self.real_lower_share}, "
                f"real_average_share={self.real_average_share}, real_upper_share={self.real_upper_share}, "
                f"active={self.active})")
