from mapping_object import MappingObject
from collections import OrderedDict


class MappingLink(MappingObject):

    def __init__(self, config):
        self.config = config
        self.global_id = None
        self.rehab_id = None
        self.mortality_BPW = None
        self.failure_year = None
        self.integer_condition_grade = None
        self.last_inspection_year = None
        self.last_inspection_date = None
        self.root_grade = None
        self.flow_ratio = None
        self.hydraulically_deficient = None
        self.design_flow_cfs = None
        self.max_flow_cfs = None
        self.material = None
        self.cross_section_id = None
        self.link_flow_type = None
        self.link_symbology = None
        self.geometry = None
        self.input_field_attribute_lookup = MappingLink.input_field_attribute_lookup()
    #TODO: verify that these match the RRAD - capacity links and rehab results
    @staticmethod
    def input_field_attribute_lookup():
        field_attribute_lookup = OrderedDict()
        field_attribute_lookup["GLOBALID"] = "global_id"
        field_attribute_lookup["Rehab_ID"] = "rehab_id"
        field_attribute_lookup["BPW"] = "mortality_BPW"
        field_attribute_lookup["FailureYear"] = "failure_year"
        field_attribute_lookup["Integer_Condition_Grade"] = "integer_condition_grade"
        field_attribute_lookup["Last_Inspection_Year"] = "last_inspection_year"
        field_attribute_lookup["Root_Grade"] = "root_grade"
        field_attribute_lookup["material"] = "material"
        field_attribute_lookup["cross_section_id"] = "cross_section_id"
        field_attribute_lookup["link_flow_type"] = "link_flow_type"
        field_attribute_lookup["link_symbology"] = "link_symbology"
        field_attribute_lookup["DesignFlowCfs"] = "design_flow_cfs"
        field_attribute_lookup["MaxFlowCfs"] = "max_flow_cfs"
        field_attribute_lookup.update(MappingObject.mapping_object_field_attribute_lookup())
        return field_attribute_lookup

#TODO rewrite all of these, make sure these match RRAD_MAPPING - links
    @staticmethod
    def rrad_field_attribute_lookup():
        rrad_field_attribute_lookup = OrderedDict()
        rrad_field_attribute_lookup["Rehab_ID"] = "rehab_id"
        rrad_field_attribute_lookup["BPW"] = "bpw"
        rrad_field_attribute_lookup["FailureYear"] = "failure_year"
        rrad_field_attribute_lookup["Integer_Condition_Grade"] = "integer_condition_grade"
        rrad_field_attribute_lookup["Last_Inspection_Date"] = "last_inspection_date"
        rrad_field_attribute_lookup["Integer_Root_Grade"] = "integer_root_grade"
        rrad_field_attribute_lookup["material"] = "material"
        rrad_field_attribute_lookup["cross_section_id"] = "cross_section_id"
        rrad_field_attribute_lookup["link_flow_Type"] = "link_flow_type"
        rrad_field_attribute_lookup["link_symbology"] = "link_symbology"
        rrad_field_attribute_lookup["DesignFlowCfs"] = "design_flow_cfs"
        rrad_field_attribute_lookup["MaxFlowCfs"] = "max_flow_cfs"
        return rrad_field_attribute_lookup

