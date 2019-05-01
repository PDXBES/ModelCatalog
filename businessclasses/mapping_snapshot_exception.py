class MappingSnapshotException(Exception):
    pass

class InvalidMappingSnapshotException(MappingSnapshotException):
    pass

class DuplicateMappingSnapshotException(MappingSnapshotException):
    pass

class NoSimulationsInMappingSnapshotException(MappingSnapshotException):
    pass