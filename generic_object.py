
class GenericObject():
    def __init__(self):
        self.id = None
        self.name = None
        self.parent_id = None
        self.field_attribute_lookup = None

    @property
    def valid(self):
        # type: () -> bool
        return False
