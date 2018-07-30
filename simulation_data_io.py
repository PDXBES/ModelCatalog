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
            insert_row = row + (model.Model_ID,
                                simulation.storm_id,
                                simulation.scenario_id,
                                0)
            insert.insertRow(insert_row)
            pass


