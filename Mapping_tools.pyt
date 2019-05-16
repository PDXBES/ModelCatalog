import arcpy
from businessclasses.model_catalog import ModelCatalog
from dataio.model_catalog_db_data_io import ModelCatalogDbDataIo
from dataio.rrad_mapping_db_data_io import RradMappingDbDataIo
from dataio.mapping_snapshot_data_io import MappingSnapshotDataIo
from businessclasses.mapping_snapshot import MappingSnapshot
from businessclasses.rrad_mapping import RradMapping
from businessclasses.config import Config
from ui.characterization_reporting import CharacterizationReporting

import getpass
import datetime
from dataio import utility

reload(arcpy)
reload(utility)

test_flag = "TEST"
config = Config(test_flag)
model_catalog = ModelCatalog(config)
model_catalog_db_data_io = ModelCatalogDbDataIo(config)
arcpy.AddMessage("in the init")
characterization_reporting = CharacterizationReporting(config,
                                                       model_catalog,
                                                       model_catalog_db_data_io)
characterization_reporting.create_characterization_model_dictionary()

class Toolbox(object):
    def __init__(self):
        with open(r"C:\Users\sgould\pydebug.txt", 'a') as file:
            file.write("in toolbox init \n")
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        arcpy.AddMessage("in toolbox init")
        self.label = "Mapping tools"
        self.alias = "Model Catalog Tools"

        # List of tool classes associated with this toolbox
        self.tools = [CharacterizationReportingTool]


class CharacterizationReportingTool(object):
    def __init__(self):
        with open(r"C:\Users\sgould\pydebug.txt", 'a') as file:
            file.write("in init \n")
        self.label = "Characterization Reporting"
        self.description = "Tool to create characterization snapshot for mapping"

    def getParameterInfo(self):
        with open(r"C:\Users\sgould\pydebug.txt", 'a') as file:
            file.write("in get parameter \n")

        characterization_models = arcpy.Parameter(
            displayName="Characterization Models",
            name="characterization_models",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            multiValue=True)
        characterization_models.filter.type = "ValueList"
        characterization_models.filter.list = characterization_reporting.characterization_model.keys()

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
        with open(r"C:\Users\sgould\pydebug.txt", 'a') as file:
            file.write("in is licensed \n")
        return True

    def updateParameters(self, parameters):
        with open(r"C:\Users\sgould\pydebug.txt", 'a') as file:
            file.write("in update parameter \n")

    def updateMessages(self, parameters):
        with open(r"C:\Users\sgould\pydebug.txt", 'a') as file:
            file.write("in update messages \n")
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""

        return

    def execute(self, parameters, messages):
        with open(r"C:\Users\sgould\pydebug.txt", 'a') as file:
            file.write("in execute \n")

        characterization_model_descriptions = parameters[0].values
        requested_by = parameters[1].valueAsText

        rrad_mapping = RradMapping(config)
        rrad_mapping_db_data_io = RradMappingDbDataIo(config)
        mapping_snapshot_data_io = MappingSnapshotDataIo(config,RradMappingDbDataIo)
        mapping_snapshot = MappingSnapshot.initialize_with_current_id(config, rrad_mapping_db_data_io)

        mapping_snapshot.snapshot_type_id = config.mapping_snapshot_type_id["Characterization"]
        mapping_snapshot.logic = "User Defined"
        mapping_snapshot.requested_by = requested_by
        mapping_snapshot.created_by = getpass.getuser()
        mapping_snapshot.create_date = datetime.datetime.today()
        mapping_snapshot.simulations = characterization_reporting.get_simulations_from_selected_models(characterization_model_descriptions)

        rrad_mapping.add_mapping_snapshot(mapping_snapshot)
        mapping_snapshot = rrad_mapping.mapping_snapshots[0]
        rrad_mapping_db_data_io.add_mapping_snapshot(mapping_snapshot, mapping_snapshot_data_io)



