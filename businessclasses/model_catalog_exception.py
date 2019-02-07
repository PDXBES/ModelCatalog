

class ModelCatalogException(Exception):
    pass


class FieldNamesLengthDoesNotMatchRowLengthException(ModelCatalogException):
    pass


class InvalidModelException(ModelCatalogException):
    pass


class DuplicateModelException(ModelCatalogException):
    pass


class DuplicatesInInputModeList(ModelCatalogException):
    pass

class InvalidModelPathException(ModelCatalogException):
    pass

class InvalidCalibrationStormSimulationDescription(ModelCatalogException):
    pass

