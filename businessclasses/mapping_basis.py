class MappingBasis(object):

    def __init__(self, config):
        self.config = config
        self.mapping_snapshots = []

    def add_mapping_snapshot(self, mapping_snapshot):
        self.mapping_snapshots.append(mapping_snapshot)

    #TODO add snapshot.  create in memory object
    #TODO Get current ids for each object type