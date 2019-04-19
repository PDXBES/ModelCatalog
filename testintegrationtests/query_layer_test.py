import arcpy
from businessclasses.config import Config


config = Config("TEST")
test_data = config.link_results_sde_path

#arcpy.env.workspace = "in_memory"
mylist = [1384]
where_clause = "Simulation_ID in ("
for count, id in enumerate(mylist):
    where_clause += str(id)
    if len(mylist) > 1 and count +1 < len(mylist):
        where_clause += ","
where_clause += ")"

#where_clause = "Simulation_ID in ("{%}")".format(mylist)
arcpy.MakeQueryTable_management(test_data, r"in_memory\ql_test", "", "", "", where_clause)

cursor = arcpy.da.SearchCursor(r"in_memory\ql_test", ["*"])

for row in cursor:
    pass

pass
