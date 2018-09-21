from rehab_data_io import RehabDataIO
from config import Config
import arcpy

config = Config()
rehab_data_io = RehabDataIO(config)


print("starting copy data management for branches")
rehab_data_io.create_branches_feature_class()
print("copy data management for branches complete, Starting pipe selection")

rehab_data_io.select_nbcr_data_pipes()
print("Pipe Selection complete, starting copy data management for pipes")

rehab_data_io.create_pipe_feature_class()
print("data management for pipes complete, starting delete field")

rehab_data_io.delete_nbcr_data_bpw_field()
print("pipe delete field complete, Starting add BPW from Branches")

rehab_data_io.add_bpw_from_branches()
print("Add BPW from Branches complete, Starting Append pipe to rehab results")

rehab_data_io.append_whole_pipes_to_rehab_results()
print "Append pipes to rehab results complete"




#arcpy.clearWorkspaceCache_management()
