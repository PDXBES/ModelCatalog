import arcpy
from businessclasses.model_catalog import ModelCatalog
from businessclasses.model import Model
from dataio.model_catalog_db_data_io import ModelCatalogDbDataIo
from dataio.simulation_data_io import SimulationDataIO
from dataio.model_data_io import ModelDataIo
import getpass
import datetime
from dataio import utility
from businessclasses import config
from businessclasses.model_catalog_exception import InvalidModelException
reload(arcpy)
reload(config)
reload(utility)
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
        self.tools = [CharacterizationReporting]


class CharacterizationReporting(object):
    def __init__(self):
        self.label = "Characterization Reporting"
        self.description = "Tool to create characterization snapshot for mapping"
        self.config = config.Config(test_flag)
        self.model_catalog = ModelCatalog(self.config)
        self.modelcatalogdataio = ModelCatalogDbDataIo(self.config)
        self.model_dataio = ModelDataIo(self.config, self.modelcatalogdataio)
        # Need to create list of model objects from model catalog

    def getParameterInfo(self):
        characterization_models = arcpy.Parameter(
            displayName="Characterization Models",
            name="characterization_models",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            multiValue=True)

        characterization_models.filter.type = "ValueList"
        characterization_models.filter.list = ["\\besfile1\CCSP\Models\TAG\2Cali\Final", "\\besfile1\CCSP\Models\TAG\2Cali\Base3" ]
        #TODO:write function to retrieve characterization models from model tracking table

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
        pass


