

class ModelCatalog_exception(Exception):
    pass


class Field_names_length_does_not_match_row_length_exception(ModelCatalog_exception):
    pass


class Invalid_Model_exception(ModelCatalog_exception):
    pass


class Duplicate_model_Exception(ModelCatalog_exception):
    pass


class Duplicates_in_input_model_list(ModelCatalog_exception):
    pass

class Invalid_model_path_exception(ModelCatalog_exception):
    pass


