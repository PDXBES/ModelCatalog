

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

class InvalidStormNameOrStormTypeInRequiredSimulationsTable(ModelCatalogException):
    pass

class InvalidDevScenarioInRequiredSimulationsTable(ModelCatalogException):
    pass

class InvalidModelPurposeException(ModelCatalogException):
    pass

class InvalidProjectPhase(ModelCatalogException):
    pass

class InvalidModelRegistrationFileException(ModelCatalogException):
    pass

class InvalidParentModelPurposeException(ModelCatalogException):
    def __init__(self, parent_model_purpose):
        self.parent_model_purpose = parent_model_purpose

class AppendModelAlterationsException(ModelCatalogException):
    pass