class Relationship:
    def __init__(self, parent_name, child_name,share):
        self.parent_name = parent_name
        self.child_name = child_name
        self.share_range = share
        self.low_range = self.share_range
        self.high_range = self.share_range
        self.low_range = (self.low_range + self.high_range)/2

