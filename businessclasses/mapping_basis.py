class MappingBasis(object):

    def __init__(self, config):
        self.config = config
        self.mapping_snapshots = []

    def add_mapping_snapshot(self, mapping_snapshot):
        if mapping_snapshot.valid:
            if mapping_snapshot not in self.mapping_snapshots:
                self.mapping_snapshots.append(mapping_snapshot)


    #TODO Get current ids for each object type