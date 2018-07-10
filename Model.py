import os


class Model:
    def __init__(self):
        self.Model_ID = 0
        self.Parent_Model_ID = 0
        self.Model_Request_ID = 0
        self.Project_Phase = None
        self.Engine_Type = None
        self.Create_Date = None
        self.Deploy_Date = None
        self.Run_Date = None
        self.Extract_Date = None
        self.Created_by = None
        self.Model_Path = None
        self.Project_Type = None
        self.Model_Purpose = None
        self.Model_Calibration_file = None
        self.Model_Status = None
        self.Model_Alterations = None
        self.Model_Alteration_file = None
        self.Project_Num = None

    def validate_model_path(self):
        valid_model_path = os.path.exists(self.Model_Path)
        return valid_model_path

    def validate_config_file(self):
        config_file_path = self.Model_Path + "\\" + "emgaats.config"
        config_file_valid = os.path.isfile(config_file_path)
        return config_file_valid

    def validate_gdb(self):
        gdb_file_path = self.Model_Path + "\\" + "EmgaatsModel.gdb"
        gdb_file_valid = os.path.exists(gdb_file_path)
        return gdb_file_valid

    def validate_sim(self):
        sim_file_path = self.Model_Path + "\\" + "sim"
        sim_folder_valid = os.path.exists(sim_file_path)
        return sim_folder_valid

    @property
    def valid(self):
        if self.validate_model_path():
            is_model_path_valid = True
        else:
            is_model_path_valid = False

        if self.validate_config_file():
            is_config_file_valid = True
        else:
            is_config_file_valid = False

        if self.validate_gdb():
            is_gdb_valid = True
        else:
            is_gdb_valid = False

        if self.validate_sim():
            is_sim_valid = True
        else:
            is_sim_valid = False

        if not is_model_path_valid or not is_config_file_valid or not is_gdb_valid or not is_sim_valid:
            is_valid = False
        else:
            is_valid = True
        return is_valid
