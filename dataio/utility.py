import os
from stat import S_IREAD, S_IRGRP, S_IROTH
import ctypes
from ctypes import wintypes
import arcpy
from businessclasses.model_catalog_exception import InvalidModelPathException

class Utility:






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
            arcpy.AddMessage("Could Not Convert Mapped Drive Path th UNC Path")
            arcpy.AddMessage(path)
            raise


#

#
# # "https://stackoverflow.com/questions/28492685/change-file-to-read-only-mode-in-python"
# model_path = r"C: \Test"
# for root, directories, filenames in os.walk(model_path):
#     for filename in filenames:
#         filepath = os.path.join(root, filename)
#         os.chmod(filepath, S_IREAD | S_IRGRP | S_IROTH)

