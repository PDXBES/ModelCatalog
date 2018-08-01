import arcpy, os

class SimulationDataIO:
    def __init__(self):
        connections = r"\\besfile1\ccsp\03_WP2_Planning_Support_Tools\03_RRAD\Model_Catalog\Dev\connection_files"
        RRAD_sde = r"BESDBTEST1.RRAD_write.sde"
        self.RRAD = os.path.join(connections, RRAD_sde)
        self.area_output_table = self.RRAD + r"\RRAD.GIS.AreaResults"
        self.field_lookup = {"SHAPE_Area": "SHAPE.STArea()", "SHAPE_Length": "SHAPE.STLength()"}  # source model: RRAD

#TODO: add test for in_path
    def copy_area_results(self, simulation, model):
        """

        :param simulation:
        :param model:
        :return:
        """
        path = self.area_results_path(simulation)
        field_names, field_names_extended = self.modify_field_names_for_RRAD(path)
        cursor = arcpy.da.SearchCursor(path, field_names)
        row_number = 0
        for row in cursor:
            if row_number%100 == 0:
                print row_number
            row_number += 1
            insert = arcpy.da.InsertCursor(self.area_output_table, field_names_extended)
            insert_row = row + (model.Model_ID,
                                simulation.storm_id,
                                simulation.scenario_id,
                                0)
            insert.insertRow(insert_row)
            pass

    def modify_field_names_for_RRAD(self, path):
        fields = arcpy.ListFields(path)
        field_names = []
        field_names_extended = []
        for field in fields:
            if field.name == "SHAPE_Area" or field.name == "SHAPE_Length" or field.name == "OBJECTID" or field.name == "SHAPE":
                pass
            else:
                field_names.append(field.name)
                field_names_extended.append(field.name)
        field_names_extended.append("SHAPE@")
        field_names_extended.append("Model_ID")
        field_names_extended.append("Storm_ID")
        field_names_extended.append("Dev_Scenario_ID")
        field_names_extended.append("Is_Orphaned")
        field_names.append("SHAPE@")
        return field_names, field_names_extended

    def area_results_path(self, simulation):
        sim_path = simulation.path()
        path = sim_path + "\\" + "results.gdb" + "\\" + "AreaResults"
        return path

