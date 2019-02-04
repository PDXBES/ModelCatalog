from dataio.rehab_data_io import RehabDataIO
from businessclasses.rehab import Rehab
from businessclasses.config import Config
from dataio.rrad_data_io import RradDbDataIo
import datetime
import time

config = Config()

rrad_data_io = RradDbDataIo(config)
rehab_data_io = RehabDataIO(config)
rehab = Rehab(config)

# TODO: Rehab tracking table is not versioned, these need to be wrapped in edit sessions

t1 = time.time()
print "getting rehab id"
rehab_id = rrad_data_io.retrieve_current_rehab_id()
rehab.id = rehab_id
rehab.extract_date = datetime.datetime.today()
rehab.last_inspection_date = datetime.datetime.today()
rehab.purpose = "test"
rrad_data_io.add_rehab(rehab)
t2 = time.time()
print str(t2-t1) + " seconds"

print "nbcr_data_to_table"
rehab_data_io.convert_nbcr_data_to_table()
t3 = time.time()
print str(t3-t2) + " seconds"

print "create_pipes"
rehab.pipes = rehab_data_io.create_pipes(rehab_id)
t4 = time.time()
print str(t4-t3) + " seconds"

print "calculate_apw"
rehab.calculate_apw()
t5 = time.time()
print str(t5-t4) + " seconds"

print "calculate_capital_cost"
rehab.calculate_capital_cost()
t6 = time.time()
print str(t6-t5) + " seconds"

print "write_pipes_to_table"
rehab_data_io.write_pipes_to_table(rehab)
t7 = time.time()
print str(t7-t6) + " seconds"

print "delete_fields_except_compkey_from_feature"
rehab_data_io.delete_fields_except_compkey_from_feature()
t8 = time.time()
print str(t8-t7) + " seconds"

print "join_output_pipe_table_and_geometry"
rehab_data_io.join_output_pipe_table_and_geometry()
t9 = time.time()
print str(t9-t8) + " seconds"

print "append_whole_pipes_to_rehab_results"
rehab_data_io.append_whole_pipes_to_rehab_results()
t10 = time.time()
print str(t10-t9) + " seconds"
print "Append pipes to rehab results complete"
