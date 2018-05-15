
import arcpy
import os

dir = r"\\cassio\asm_projects\E10922_taggart\models\Preliminary\BaseR011018V4ic - Copy"
tracking = r"\\besfile1\ccsp\03_WP2_Planning_Support_Tools\03_RRAD\Model_Catalog\ModelCatalog_TEST.gdb\ModelTracking"

# need to get these values from form objects that get returned
param_projType = "Combined"
param_projPhase = "Pre Design"
param_modelPurpose = "Characterization"

# get feature class from model
print "Identifying model feature class"
areas_base = os.path.join(dir, r"EmgaatsModel.gdb\Areas_base")

# create convex hull of areas_base - buffers took way too long for larger model runs
print "Creating bounding polygon around model area"
areas_hull = arcpy.MinimumBoundingGeometry_management(areas_base, r"in_memory\areas_hull", "CONVEX_HULL", "ALL")

# get list of field names
fields = arcpy.ListFields(areas_hull)
field_names = []
for field in fields:
    field_names.append(field.name)

# create field if it does not exist
my_field = "Model_ID"
if my_field not in field_names:
    arcpy.AddField_management(areas_hull, my_field, "LONG")

# get max count of Model_ID from tracking - FOR THIS TO WORK MUST HAVE INITIAL RECORD WITH MODELID == 0
maxlist= []
with arcpy.da.SearchCursor(tracking, ["Model_ID"]) as cursor:
    for row in cursor:
        maxlist.append(row[0])

# update Model ID field + 1
print "Fill Model ID with value + 1"
with arcpy.da.UpdateCursor(areas_hull, my_field) as cursor:
    for row in cursor:
        row[0] = max(maxlist) + 1
        cursor.updateRow(row)

# append result to model tracking db, using model tracking results
print "Appending bounding polygon to Model Tracking"
arcpy.Append_management(areas_hull, tracking, "NO_TEST")

# apply values returned from form inputs to tracking fc
edit_fields = ["Model_ID", "Project_Type", "Project_Phase", "Model_Purpose"]

print "Applying input values to record"
with arcpy.da.UpdateCursor(tracking, edit_fields) as cursor:
    for row in cursor:
        row[1] = param_projType
        row[2] = param_projPhase
        row[3] = param_modelPurpose
        cursor.updateRow(row)