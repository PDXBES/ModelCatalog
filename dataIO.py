import arcpy


class DataIO():
    def __init__(self):
        pass

    # Not sure how to iterate through rows
    def add_model(self, model, location, field_names):
        cursor = arcpy.da.UpdateCursor(location, field_names)
        row = [model.Parent_Model_ID, model.Model_Request_ID]
        cursor.updateRow(row)
        pass

    def insert_model(self, model, location, field_names):
        cursor = arcpy.da.InsertCursor(location, field_names)
        row = [model.Parent_Model_ID, model.Model_Request_ID]
        cursor.insertRow(row)
        pass

    #Doesn't work with unit test (It seems to be related to the with and as)
    def insert_model1(self, model, location, field_names):
        with arcpy.da.InsertCursor(location, field_names) as cursor:
            row = [model.Parent_Model_ID, model.Model_Request_ID]
            cursor.insertRow(row)
        pass
