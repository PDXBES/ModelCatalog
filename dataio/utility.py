import os
from businessclasses.config import Config
import ctypes
from ctypes import wintypes
import arcpy
from businessclasses.model_catalog_exception import InvalidModelPathException

class Utility:

    config = Config()

    def convert_mapped_letter_drive_to_unc_path(self, path):
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

    def check_path(self, path):
        try:
            if ":" in path:
                drive_letter = path[:2]
                network_path = self.convert_mapped_letter_drive_to_unc_path(drive_letter)
                path = network_path + path[2:]

            return path

        except:
            arcpy.AddMessage("Path provided is not a valid path for Model Registration")
            arcpy.AddMessage("Note that local files and paths can not be registered, check your path: ")
            arcpy.AddMessage(path)
            raise InvalidModelPathException


    def model_catalog_test_data_cleanup(self):
        feature_class_list = [config.model_tracking_sde_path, config.model_alt_bc_sde_path,
                              config.model_alt_hydraulic_sde_path, config.model_alt_hydrologic_sde_path,
                              config.project_type_sde_path, config.required_simulations_sde_path]
        for feature_class in feature_class_list:
            arcpy.DeleteRows_management(feature_class)

    # def rrad_test_data_cleanup(self):
    #     feature_class_list = [config.rehab_tracking_sde_path, config.rehab_results_sde_path,
    #                           config.area_results_sde_path, config.link_results_sde_path,
    #                           config.node_results_sde_path, config.flooding_results_sde_path,
    #                           config.directors_sde_path]
    #     for feature_class in feature_class_list:
    #         arcpy.DeleteRows_management(feature_class)

