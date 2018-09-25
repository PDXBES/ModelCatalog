from rehab_data_io import RehabDataIO
from config import Config
import arcpy

config = Config()
rehab_data_io = RehabDataIO(config)

rehab_data_io.convert_nbcr_data_to_table()


rehab_data_io.append_whole_pipes_to_rehab_results()
print "Append pipes to rehab results complete"




#arcpy.clearWorkspaceCache_management()
