import arcpy

class SimulationDataIO:
    def copy_area_results(self, simulation, model):
        sim_path = simulation.path()
        path = sim_path + "\\" + "results.gdb" + "\\" + "AreaResults"
        fields = arcpy.ListFields(path)
        field_names = []
        field_names_extended = []
        for field in fields:
            field_names.append(field.name)
            field_names_extended.append(field.name)
        cursor = arcpy.da.SearchCursor(path, field_names)

        field_names_extended.append("Model_ID")
        field_names_extended.append("Storm_ID")
        field_names_extended.append("Scenario_ID")
        field_names_extended.append("Is_Orphaned")
        for row in cursor:
            insert = arcpy.da.InsertCursor(path, field_names_extended)
            insert_row = arcpy.Row()
            for field in field_names:
                insert_row.setValue(field, row.getValue(field))
            insert_row.setValue("Model_ID", model.Model_ID)
            insert_row.setValue("Storm_ID", simulation.storm_id)
            insert_row.setValue("Scenario_ID", simulation.scenario_id)
            insert_row.setValue("Is_Orphaned", 0)
            insert.insertRow(insert_row)



