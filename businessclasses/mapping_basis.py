from businessclasses.mapping_snapshot_exception import InvalidMappingSnapshotException
from businessclasses.mapping_snapshot_exception import DuplicateMappingSnapshotException

class MappingBasis(object):

    def __init__(self, config):
        self.config = config
        self.mapping_snapshots = []

    def add_mapping_snapshot(self, mapping_snapshot):
        if mapping_snapshot.valid:
            if mapping_snapshot not in self.mapping_snapshots:
                self.mapping_snapshots.append(mapping_snapshot)
            else:
                raise DuplicateMappingSnapshotException
        else:
            raise InvalidMappingSnapshotException


    #TODO Get current ids for each object type