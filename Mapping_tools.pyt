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
        self.tools = [SlrtQaQc]


class SlrtQaQc(object):
    def __init__(self):
        self.label = "SLRT Data Quality"
        self.description = "Tool for recording SLRT data quality to database"
        self.config = config.Config(test_flag)
        self.model_catalog = ModelCatalog(self.config)
        self.modelcatalogdataio = ModelCatalogDbDataIo(self.config)
        self.model_dataio = ModelDataIo(self.config, self.modelcatalogdataio)
        # Need to create list of model objects from model catalog

    def getParameterInfo(self):
        model_id = arcpy.Parameter(
            displayName="Model ID",
            name="model_id",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        model_id.filter.type = "ValueList"
        model_id.filter.list = [1, 2, 3] #TODO Need to get list of final calibration models, purpose, paths

        station_id = arcpy.Parameter(
            displayName="Station ID",
            name="station_id",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        station_id.filter.list = [1, 2, 3] #TODO Need to get list of station ids

        h2_id = arcpy.Parameter(
            displayName="H2 ID",
            name="h2_id",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        h2_id.filter.list = [1, 2, 3] #TODO Need to get list of h2 id for station

        location_qualifier = arcpy.Parameter(
            displayName="Location Qualifier",
            name="location_qualifier",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        location_qualifier.filter.list = [1, 2, 3] #TODO Need to get list of location qualifiers for h2 id

        simulations_qa_qc = arcpy.Parameter(
            displayName='Observed Data Quality',
            name='qaqc_table',
            datatype='GPValueTable', # this is the combo box
            parameterType='Required',
            direction='Input')



        simulations_qa_qc.columns = [['String', 'Simulation'], ['String', 'Depth QC'], ['String', 'Flow QC']]
        simulations_qa_qc.values = [["sim1" , "Good","Fair"]]
        simulations_qa_qc.filters[1].type = 'ValueList'
        simulations_qa_qc.filters[1].list = ["Good", "Fair", "Poor", "NA"]
        simulations_qa_qc.filters[2].list = ["Good", "Fair", "Poor", "NA"]

        calculated_data_quality = arcpy.Parameter(
            displayName="Calculated Data Quality (Automatically Calculated)",
            name="calculated_data_quality",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        calculated_data_quality.filter.list = ["Good", "Fair", "Poor"]
        calculated_data_quality.value = "Good" #TODO this will need to calculated in the updateParameters
        calculated_data_quality.enabled = False

        override_data_quality = arcpy.Parameter(
            displayName="Data Quality Override",
            name="override_data_quality",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        override_data_quality.filter.list = ["Good", "Fair", "Poor"]

        params = [model_id, station_id, h2_id, location_qualifier, simulations_qa_qc, calculated_data_quality,
                  override_data_quality]
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


