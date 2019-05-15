import arcpy
from businessclasses.model_catalog import ModelCatalog
from businessclasses.model import Model
from dataio.model_catalog_db_data_io import ModelCatalogDbDataIo
from businessclasses.mapping_snapshot import MappingSnapshot
from businessclasses.rrad_mapping import RradMapping
from dataio.rrad_mapping_db_data_io import RradMappingDbDataIo
from dataio.simulation_data_io import SimulationDataIO
from dataio.model_data_io import ModelDataIo
import getpass
import datetime
from dataio import utility
from businessclasses import config
from ui import characterization_reporting
from businessclasses.model_catalog_exception import InvalidModelException
reload(arcpy)
reload(config)
reload(utility)
reload(characterization_reporting)
# reload(ModelCatalog)
# reload(Model)
# reload(ModelCatalogDbDataIo)
# reload(ModelDataIo)
# reload(SimulationDataIO)

test_flag = "TEST"

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Mapping tools"
        self.alias = "Model Catalog Tools"

        # List of tool classes associated with this toolbox
        self.tools = [CharacterizationReportingTool]


class CharacterizationReportingTool(object):
    def __init__(self):
        self.label = "Characterization Reporting"
        self.description = "Tool to create characterization snapshot for mapping"
        self.config = config.Config(test_flag)
        self.model_catalog = ModelCatalog(self.config)
        self.model_catalog_db_data_io = ModelCatalogDbDataIo(self.config)

        self.characterization_reporting = characterization_reporting.CharacterizationReporting(self.config,
                                                                                               self.model_catalog,
                                                                                               self.model_catalog_db_data_io)

        self.characterization_reporting.create_characterization_model_dictionary()
        self.rrad_mapping_db_data_io = RradMappingDbDataIo(self.config)

    def getParameterInfo(self):
        characterization_models = arcpy.Parameter(
            displayName="Characterization Models",
            name="characterization_models",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            multiValue=True)
        characterization_models.filter.type = "ValueList"
        characterization_models.filter.list = self.characterization_reporting.characterization_model.keys()

        requested_by = arcpy.Parameter(
            displayName="Requested By",
            name="requested_by",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )

        params = [characterization_models, requested_by]
        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        pass

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""

        return

    def execute(self, parameters, messages):
        characterization_models = parameters[0].values
        requested_by = parameters[1].valuesAsText

        self.mapping_snapshot = MappingSnapshot.initialize_with_current_id(self.config, self.rrad_mapping_db_data_io)
        self.mapping_snapshot.snapshot_type_id = self.config.mapping_snapshot_type_id("Characterization")
        self.mapping_snapshot.logic = "User Defined"
        self.mapping_snapshot.requested_by = requested_by
        self.mapping_snapshot.created_by = getpass.getuser()
        self.mapping_snapshot.


