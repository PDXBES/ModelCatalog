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

    @staticmethod
    def input_field_attribute_lookup():
        field_attribute_lookup = OrderedDict()
        field_attribute_lookup["Global_ID"] = "global_id"
        field_attribute_lookup["Rehab_ID"] = "rehab_id"
        field_attribute_lookup["BPW"] = "mortality_BPW"
        field_attribute_lookup["Failure_Year"] = "failure_year"
        field_attribute_lookup["Integer_Condition_Grade"] = "integer_condition_grade"
        field_attribute_lookup["Last_Inspection_Year"] = "last_inspection_year"
        field_attribute_lookup["Root_Grade"] = "root_grade"
        field_attribute_lookup["DesignFlowCFS"] = "design_flow_cfs"
        field_attribute_lookup["MaxFlowCFS"] = "max_flow_cfs"
        field_attribute_lookup["Material"] = "material"
        field_attribute_lookup["Cross_Section_ID"] = "cross_section_id"
        field_attribute_lookup["Link_Flow_Type"] = "link_flow_type"
        field_attribute_lookup["Link_Symbology"] = "link_symbology"
        field_attribute_lookup.update(MappingObject.mapping_object_field_attribute_lookup())
        return field_attribute_lookup

#TODO rewrite all of these, make sure these match the RRAd
    @staticmethod
    def rrad_rehab_field_attribute_lookup():
        rrad_rehab_field_attribute_lookup = OrderedDict()
        return rrad_rehab_field_attribute_lookup

    @staticmethod
    def rrad_capacity_field_attribute_lookup():
        rrad_capacity_field_attribute_lookup = OrderedDict()
        return rrad_capacity_field_attribute_lookup

