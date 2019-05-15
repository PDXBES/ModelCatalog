class MappingSnapshotException(Exception):
    pass

class InvalidMappingSnapshotException(MappingSnapshotException):
    pass

class DuplicateMappingSnapshotException(MappingSnapshotException):
    pass

class NoSimulationsInMappingSnapshotException(MappingSnapshotException):
    pass

class MaxFlowIsNoneException(MappingSnapshotException):
    pass

class DesignFlowIsNoneException(MappingSnapshotException):
    pass