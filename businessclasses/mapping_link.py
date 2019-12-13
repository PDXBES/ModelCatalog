from mapping_object import MappingObject
from collections import OrderedDict
from mapping_snapshot_exception import MaxFlowIsNoneException
from mapping_snapshot_exception import DesignFlowIsNoneException
import datetime

class MappingLink(MappingObject):

    def __init__(self, config):
        self.config = config
        self.global_id = None
        self.rehab_id = None
        self.mortality_BPW = None
        self.failure_year = None
        self.integer_condition_grade = None
        self.last_inspection_date = None
        self.integer_root_grade = None
        self.design_flow_cfs = None
        self.max_flow_cfs = None
        self.material = None
        self.cross_section_id = None
        self.link_flow_type = None
        self.link_symbology = None
        self.geometry = None
        self.rrad_rehab_result_id = None
        self.emgaats_link_id = None

        self.rrad_link_id = None
        self.input_field_attribute_lookup = MappingLink.input_field_attribute_lookup()
        super(MappingLink, self).__init__(config)

    @property
    def flow_ratio(self):
        try:
            flow_ratio = float(self.max_flow_cfs) / float(self.design_flow_cfs)
        except:
            flow_ratio = None
        return flow_ratio

    @property
    def hydraulically_deficient(self):
        hydraulically_deficient_threshold = 1.2
        if self.max_flow_cfs is None:
            raise MaxFlowIsNoneException
        if self.design_flow_cfs is None:
            raise DesignFlowIsNoneException
        if self.design_flow_cfs == 0:
            return False
        if self.flow_ratio >= hydraulically_deficient_threshold:
            return True
        return False

    @property
    def last_inspection_year(self):
        try:
            last_inspection_year = int(self.last_inspection_date.strftime('%Y'))
        except:
            last_inspection_year = None
        return last_inspection_year

    #TODO: verify that these match the RRAD - capacity links and rehab results
    @staticmethod
    def input_field_attribute_lookup():
        field_attribute_lookup = OrderedDict()
        field_attribute_lookup["dme_global_id"] = "global_id"
        field_attribute_lookup["Rehab_ID"] = "rehab_id"
        field_attribute_lookup["BPW"] = "mortality_BPW"
        field_attribute_lookup["FailureYear"] = "failure_year"
        field_attribute_lookup["Integer_Condition_Grade"] = "integer_condition_grade"
        field_attribute_lookup["Last_Inspection_Year"] = "last_inspection_year"
        field_attribute_lookup["Last_Inspection_Date"] = "last_inspection_date"
        field_attribute_lookup["Integer_Root_Grade"] = "integer_root_grade"
        field_attribute_lookup["material"] = "material"
        field_attribute_lookup["cross_section_id"] = "cross_section_id"
        field_attribute_lookup["link_flow_type"] = "link_flow_type"
        field_attribute_lookup["link_symbology"] = "link_symbology"
        field_attribute_lookup["DesignFlowCfs"] = "design_flow_cfs"
        field_attribute_lookup["MaxFlowCfs"] = "max_flow_cfs"
        field_attribute_lookup["Pipe_Flow_Ratio"] = "flow_ratio"
        field_attribute_lookup["Hydraulically_Deficient"] = "hydraulically_deficient"
        field_attribute_lookup["sim_desc"] = "sim_desc"
        field_attribute_lookup["Shape@"] = "geometry"
        field_attribute_lookup["rrad_link_id"] = "rrad_link_id"
        field_attribute_lookup["link_id"] = "emgaats_link_id"
        field_attribute_lookup["rrad_mapping_link_id"] = "id"
        field_attribute_lookup.update(MappingObject.mapping_object_field_attribute_lookup())
        return field_attribute_lookup

#TODO rewrite all of these, make sure these match RRAD_MAPPING - links
    @staticmethod
    def rrad_field_attribute_lookup():
        rrad_field_attribute_lookup = OrderedDict()
        rrad_field_attribute_lookup["RRAD.GIS.in_memory\\mapping_link_in_memory_table.link_id"] = "emgaats_link_id"
        rrad_field_attribute_lookup["RRAD.GIS.in_memory\\mapping_link_in_memory_table.dme_global_id"] = "global_id"
        rrad_field_attribute_lookup["RRAD.GIS.in_memory\\rehab_links_in_memory_table.Rehab_ID"] = "rehab_id"
        rrad_field_attribute_lookup["RRAD.GIS.in_memory\\rehab_links_in_memory_table.rrad_rehab_result_id"] = "rrad_rehab_result_id"
        rrad_field_attribute_lookup["RRAD.GIS.in_memory\\rehab_links_in_memory_table.BPW"] = "mortality_BPW"
        rrad_field_attribute_lookup["RRAD.GIS.in_memory\\rehab_links_in_memory_table.FailureYear"] = "failure_year"
        rrad_field_attribute_lookup["RRAD.GIS.in_memory\\rehab_links_in_memory_table.Integer_Condition_Grade"] = "integer_condition_grade"
        rrad_field_attribute_lookup["RRAD.GIS.in_memory\\rehab_links_in_memory_table.Last_Inspection_Date"] = "last_inspection_date"
        rrad_field_attribute_lookup["RRAD.GIS.in_memory\\rehab_links_in_memory_table.Integer_Root_Grade"] = "integer_root_grade"
        rrad_field_attribute_lookup["RRAD.GIS.in_memory\\mapping_link_in_memory_table.material"] = "material"
        rrad_field_attribute_lookup["RRAD.GIS.in_memory\\mapping_link_in_memory_table.cross_section_id"] = "cross_section_id"
        rrad_field_attribute_lookup["RRAD.GIS.in_memory\\mapping_link_in_memory_table.link_flow_Type"] = "link_flow_type"
        rrad_field_attribute_lookup["RRAD.GIS.in_memory\\mapping_link_in_memory_table.link_symbology"] = "link_symbology"
        rrad_field_attribute_lookup["RRAD.GIS.in_memory\\mapping_link_in_memory_table.DesignFlowCfs"] = "design_flow_cfs"
        rrad_field_attribute_lookup["RRAD.GIS.in_memory\\mapping_link_in_memory_table.MaxFlowCfs"] = "max_flow_cfs"
        rrad_field_attribute_lookup["Shape@"] = "geometry"
        rrad_field_attribute_lookup["RRAD.GIS.in_memory\\mapping_link_in_memory_table.Simulation_ID"] = "simulation_id"
        rrad_field_attribute_lookup["RRAD.GIS.in_memory\\mapping_link_in_memory_table.rrad_link_id"] = "rrad_link_id"
        return rrad_field_attribute_lookup

