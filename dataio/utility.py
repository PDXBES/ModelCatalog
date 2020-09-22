import os
#from businessclasses.config import Config
import ctypes
from ctypes import wintypes
import arcpy
from businessclasses.model_catalog_exception import InvalidModelPathException
from datetime import date

class Utility:


    def __init__(self, config):

        self.config = config

    @staticmethod
    def convert_mapped_letter_drive_to_unc_path(path):
        #https://stackoverflow.com/questions/34801315/get-full-computer-name-from-a-network-drive-letter-in-python
        mpr = ctypes.WinDLL('mpr')
        ERROR_SUCCESS = 0x0000
        ERROR_MORE_DATA = 0x00EA
        wintypes.LPDWORD = ctypes.POINTER(wintypes.DWORD)
        mpr.WNetGetConnectionW.restype = wintypes.DWORD
        mpr.WNetGetConnectionW.argtypes = (wintypes.LPCWSTR,
                                           wintypes.LPWSTR,
                                           wintypes.LPDWORD)

        length = (wintypes.DWORD * 1)()
        result = mpr.WNetGetConnectionW(path, None, length)
        if result != ERROR_MORE_DATA:
            raise ctypes.WinError(result)
        remote_name = (wintypes.WCHAR * length[0])()
        result = mpr.WNetGetConnectionW(path, remote_name, length)
        if result != ERROR_SUCCESS:
            raise ctypes.WinError(result)
        return remote_name.value

    @staticmethod
    def check_path(path):
        try:
            if ":" in path:
                drive_letter = path[:2]
                network_path = Utility.convert_mapped_letter_drive_to_unc_path(drive_letter)
                path = network_path + path[2:]

            return path

        except:
            arcpy.AddError("Path provided is not a valid path for Model Registration")
            arcpy.AddError("Note that local files and paths can not be registered, check your path: ")
            arcpy.AddError(path)
            raise InvalidModelPathException

    @staticmethod
    def format_date(date_object):
        return date_object.strftime("%m/%d/%Y %H:%M %p")

    def model_catalog_test_data_cleanup(self):
        if self.config.test_flag == "TEST":
            feature_class_list = [self.config.model_tracking_sde_path, self.config.model_alt_bc_sde_path,
                                  self.config.model_alt_hydraulic_sde_path, self.config.model_alt_hydrologic_sde_path,
                                  self.config.project_type_sde_path, self.config.simulation_sde_path,
                                  self.config.geometry_nodes_sde_path, self.config.geometry_areas_sde_path,
                                  self.config.geometry_links_sde_path,
                                  self.config.results_area_sde_path, self.config.results_link_sde_path,
                                  self.config.results_node_sde_path, self.config.results_node_flooding_sde_path,
                                  self.config.storage_sde_path,
                                  self.config.director_sde_path]
            for feature_class in feature_class_list:
                try:
                    arcpy.TruncateTable_management(feature_class)
                except:
                    print("unable to truncate, using Delete Rows")
                    arcpy.DeleteRows_management(feature_class)
        else:
            print("Config set to other than TEST, data will not be deleted")

    # TODO write test
    def set_current_ids_to_zero(self, current_id_table_sde_path):
        if self.config.test_flag == "TEST":
            field_names = ["Current_ID"]
            cursor = arcpy.da.UpdateCursor(current_id_table_sde_path, field_names)
            for row in cursor:
                row[0] = 0
                cursor.updateRow(row)
            del cursor
        else:
            print("Config set to other than TEST, data will not be deleted")


