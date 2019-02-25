from unittest import TestCase
import mock
from testbusinessclasses.mock_config import MockConfig
import arcpy
from dataio.db_data_io import DbDataIo
from collections import OrderedDict
from businessclasses.generic_class_factory import GenericClassFactory


class TestDataIO(TestCase):

    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config

        self.parent_id_to_db_field_mapping = [(1, "id_field_one"), (2, "id_field_two")]
        generic_class_factory = GenericClassFactory(self.config)
        self.db_data_io = DbDataIo(self.config, generic_class_factory)
        self.object_class = None
        self.field_names_retrieve_id = ["Object_Type", "Current_ID"]

        self.mock_row = (1, 2)
        self.field_attribute_lookup_add_object = OrderedDict([("id_db", "id"), ("parent_id_db", "parent_id")])

        self.patch_create_object = mock.patch("businessclasses.generic_class_factory.GenericClassFactory.create_object")
        self.mock_create_object = self.patch_create_object.start()

        self.mock_update_cursor = mock.MagicMock(arcpy.da.UpdateCursor)
        self.mock_update_cursor.__iter__.return_value = iter([("object_1", 44), ("object_2", 55)])

        self.mock_insert_cursor = mock.MagicMock(arcpy.da.InsertCursor)

        self.mock_search_cursor = mock.MagicMock(arcpy.da.SearchCursor)
        self.mock_search_cursor.__iter__.return_value = iter([self.mock_row])

        self.patch_append = mock.patch("arcpy.Append_management")
        self.mock_append = self.patch_append.start()

        self.patch_copy_features_management = mock.patch("arcpy.CopyFeatures_management")
        self.mock_copy_features_management = self.patch_copy_features_management.start()

        self.patch_add_field_management = mock.patch("arcpy.AddField_management")
        self.mock_add_field_management = self.patch_add_field_management.start()

        self.patch_calculate_field = mock.patch("arcpy.CalculateField_management")
        self.mock_calculate_field = self.patch_calculate_field.start()

        self.patch_da_UpdateCursor = mock.patch("arcpy.da.UpdateCursor")
        self.mock_da_UpdateCursor = self.patch_da_UpdateCursor.start()

        self.patch_da_InsertCursor = mock.patch("arcpy.da.InsertCursor")
        self.mock_da_InsertCursor = self.patch_da_InsertCursor.start()

        self.patch_da_SearchCursor = mock.patch("arcpy.da.SearchCursor")
        self.mock_da_SearchCursor = self.patch_da_SearchCursor.start()
        self.mock_da_SearchCursor.return_value = self.mock_search_cursor

        self.patch_create_field_map_for_sde_db = mock.patch.object(self.db_data_io, "_create_field_map_for_sde_db")
        self.mock_create_field_map_for_sde_db = self.patch_create_field_map_for_sde_db.start()

        self.patch_create_feature_class = mock.patch("arcpy.CreateFeatureclass_management")
        self.mock_create_feature_class = self.patch_create_feature_class.start()

        self.mock_da_InsertCursor.return_value = self.mock_insert_cursor

        self.mock_generic_object = mock.MagicMock("GenericObject")
        self.mock_generic_object.id = 1
        self.mock_generic_object.name = "name"
        self.mock_generic_object.valid = False
        self.mock_generic_object.parent_id = 2

        self.field_attribute_lookup_add_object = OrderedDict()
        self.field_attribute_lookup_add_object["id_field"] = "id"
        self.field_attribute_lookup_add_object["name"] = "name"

        self.field_attribute_lookup_create_object = OrderedDict()
        self.field_attribute_lookup_create_object["id_db"] = "id"
        self.field_attribute_lookup_create_object["parent_id_db"] = "parent_id"

        self.field_attribute_lookup_create_table_from_objects = self.field_attribute_lookup_create_object

        self.object_tracking_sde_path = "object_tracking_sde_path"

    def tearDown(self):
        self.mock_da_UpdateCursor = self.patch_da_UpdateCursor.stop()
        self.mock_da_InsertCursor = self.patch_da_InsertCursor.stop()
        self.mock_append = self.patch_append.stop()
        self.mock_copy_features_management = self.patch_copy_features_management.stop()
        self.mock_add_field_management = self.patch_add_field_management.stop()
        self.mock_calculate_field = self.patch_calculate_field.stop()
        self.mock_create_field_map_for_sde_db = self.patch_create_field_map_for_sde_db.stop()
        self.mock_da_SearchCursor = self.patch_da_SearchCursor.stop()
        self.mock_create_object = self.patch_create_object.stop()
        self.mock_create_feature_class = self.patch_create_feature_class.stop()

    def test_retrieve_current_id_calls_update_cursor_with_correct_arguments(self):
        self.mock_da_UpdateCursor.return_value = self.mock_update_cursor
        self.db_data_io.current_id_database_table_path = "current_id_database_table_path"
        self.db_data_io.retrieve_current_id("object_1")
        self.mock_da_UpdateCursor.assert_called_with("current_id_database_table_path",self.field_names_retrieve_id)

    def test_retrieve_current_id_return_current_ID(self):
        self.mock_da_UpdateCursor.return_value = self.mock_update_cursor
        current_id = self.db_data_io.retrieve_current_id("object_1")
        self.assertTrue(current_id == 44)

    def test_retrieve_current_id_update_next_id_of_object_1(self):
        self.mock_da_UpdateCursor.return_value = self.mock_update_cursor
        self.db_data_io.retrieve_current_id("object_1")
        self.assertTrue(self.mock_update_cursor.updateRow.called)
        self.mock_update_cursor.updateRow.assert_called_with(["object_1", 45])

    def test_retrieve_current_id_update_next_id_of_object_2(self):
        self.mock_da_UpdateCursor.return_value = self.mock_update_cursor
        self.db_data_io.retrieve_current_id("object_2")
        self.assertTrue(self.mock_update_cursor.updateRow.called)
        self.mock_update_cursor.updateRow.assert_called_with(["object_2", 56])

    def test_add_object_calls_insert_cursor_with_correct_arguments(self):
        self.mock_generic_object.valid = True
        self.db_data_io.add_object(self.mock_generic_object, self.field_attribute_lookup_add_object, self.object_tracking_sde_path)
        self.mock_da_InsertCursor.assert_called_with("object_tracking_sde_path", ["id_field", "name"])

    def test_add_object_calls_insertRow_with_correct_arguments(self):
        self.mock_generic_object.valid = True
        self.db_data_io.add_object(self.mock_generic_object, self.field_attribute_lookup_add_object, self.object_tracking_sde_path)
        self.mock_insert_cursor.insertRow.assert_called_with([1, "name"])

    def test_create_row_from_object_creates_row_with_correct_values(self):
        row = self.db_data_io.create_row_from_object(self.mock_generic_object, self.field_attribute_lookup_add_object)
        self.assertEquals(row, [1, "name"])

    def test_create_row_from_object_raise_exception_when_attribute_name_does_not_exist(self):
        self.field_attribute_lookup_add_object["color"] = "red"
        with self.assertRaises(AttributeError):
            self.db_data_io.create_row_from_object(self.mock_generic_object, self.field_attribute_lookup_add_object)

    def test_copy_to_memory_calls_copy_features_management_with_correct_arguments(self):
        self.db_data_io.copy_to_memory("input_table", "in_memory_output_table_name", self.parent_id_to_db_field_mapping)
        self.mock_copy_features_management.assert_called_with("input_table", "in_memory\\in_memory_output_table_name")

    def test_copy_calls_add_field_management_with_correct_arguments(self):
        self.db_data_io.copy("input_table", "target", "field_mappings", self.parent_id_to_db_field_mapping)
        self.assertEqual(self.mock_add_field_management.call_args_list[0][0], ("in_memory\copy_table", "id_field_one", "LONG"))
        self.assertEqual(self.mock_add_field_management.call_args_list[1][0], ("in_memory\copy_table", "id_field_two", "LONG"))

    def test_copy_calls_calculate_field_with_correct_arguments(self):
        self.db_data_io.copy("input_table", "target", "field_mappings", self.parent_id_to_db_field_mapping)
        id_1 = 1
        id_2 = 2
        self.assertEqual( self.mock_calculate_field.call_args_list[0][0], ("in_memory\copy_table", "id_field_one", id_1, 'PYTHON_9.3'))
        self.assertEqual( self.mock_calculate_field.call_args_list[1][0], ("in_memory\copy_table", "id_field_two", id_2, 'PYTHON_9.3'))

    def test_copy_if_field_mappings_is_not_None_append_called_with_correct_arguments(self):
        self.db_data_io.copy("input_table", "target", "field_mappings", self.parent_id_to_db_field_mapping)
        self.mock_append.assert_called_with("in_memory\\copy_table", "target", "NO_TEST", "field_mappings")

    def test_copy_if_field_mappings_is_None_append_called_with_correct_arguments(self):
        self.mock_create_field_map_for_sde_db.return_value = "field_mappings"
        self.db_data_io.copy("input_table", "target", None, self.parent_id_to_db_field_mapping)
        self.mock_append.assert_called_with("in_memory\copy_table", "target", "NO_TEST", "field_mappings")

    def test_copy_db_to_db_if_field_mappings_is_not_None_append_called_with_correct_arguments(self):
        self.db_data_io.copy_db_to_db("input_table", "target", "field_mappings", self.parent_id_to_db_field_mapping)
        self.mock_append.assert_called_with("input_table", "target", "NO_TEST", "field_mappings")

    def test_copy_db_to_db_if_field_mappings_is_None_append_called_with_correct_arguments(self):
        self.db_data_io.copy_db_to_db("input_table", "target", None, self.parent_id_to_db_field_mapping)
        self.mock_append.assert_called_with("input_table", "target", "NO_TEST")

    def test_copy_db_to_db_calls_calculate_field_with_correct_arguments(self):
        self.db_data_io.copy_db_to_db("input_table", "target", "field_mappings", self.parent_id_to_db_field_mapping)
        id_1 = 1
        id_2 = 2
        self.assertEqual(self.mock_calculate_field.call_args_list[0][0], ("target", "id_field_one", id_1))
        self.assertEqual(self.mock_calculate_field.call_args_list[1][0], ("target", "id_field_two", id_2))

    def test_create_object_from_row_creates_object_with_correct_attributes(self):
        self.mock_generic_object.id = None
        self.mock_generic_object.parent_id = None
        self.db_data_io.create_object_from_row(self.mock_generic_object, self.field_attribute_lookup_create_object, self.mock_row)
        self.assertEqual(self.mock_generic_object.id, 1)
        self.assertEqual(self.mock_generic_object.parent_id, 2)

    def test_create_objects_from_table_calls_search_cursor_with_correct_arguments(self):
        self.db_data_io.create_objects_from_table("table", "area", self.field_attribute_lookup_create_object)
        self.mock_da_SearchCursor.assert_called_with("table", self.field_attribute_lookup_create_object.keys())

    def test_create_objects_from_table_returns_list_with_correct_object(self):
        self.patch_create_object.return_value = self.mock_generic_object
        list_of_objects = self.db_data_io.create_objects_from_table("table", "area", self.field_attribute_lookup_create_object)
        object_1 = list_of_objects[0]
        self.assertEqual(object_1.id, 1)
        self.assertEqual(object_1.parent_id, 2)

    def test_create_feature_class_from_objects_calls_create_table_with_correct_arguments(self):
        self.db_data_io.workspace = "in_memory"
        output_feature_class_name = "output_feature_class_name"
        object_list = ["obj1", "obj2"]
        field_attribute_lookup = OrderedDict()
        template_feature_class_path = "template_feature_class_path"
        self.db_data_io.create_feature_class_from_objects(output_feature_class_name, object_list, field_attribute_lookup, template_feature_class_path)
        self.mock_create_feature_class.assert_called_with("in_memory", "output_feature_class_name", "", "template_feature_class_path", "", "", "template_feature_class_path")

    def test_create_feature_class_from_objects_calls_insert_cursor_with_correct_arguments(self):
        self.db_data_io.workspace = "in_memory"
        output_feature_class_name = "output_feature_class_name"
        object_list = [self.mock_generic_object]
        template_feature_class_path = "template_feature_class_path"
        field_list = ["id_db", "parent_id_db"]
        self.db_data_io.create_feature_class_from_objects(output_feature_class_name, object_list, self.field_attribute_lookup_create_table_from_objects, template_feature_class_path)
        self.mock_da_InsertCursor.assert_called_with("in_memory\\output_feature_class_name", field_list)

    def test_create_feature_class_from_objects_calls_insert_row_with_correct_arguments(self):
        self.db_data_io.workspace = "in_memory"
        output_feature_class_name = "output_feature_class_name"
        object_list = [self.mock_generic_object]
        template_feature_class_path = "template_feature_class_path"
        self.db_data_io.create_feature_class_from_objects(output_feature_class_name, object_list, self.field_attribute_lookup_create_table_from_objects, template_feature_class_path)
        self.mock_insert_cursor.insertRow.assert_called_with([1, 2])

    def test_append_feature_class_to_db_calls_create_feature_class_from_objects_with_correct_arguments(self):
        with mock.patch.object(self.db_data_io, "create_feature_class_from_objects") as mock_create_feature_class_from_objects:
            self.db_data_io.workspace = "in_memory"
            output_feature_class_name = "intermediate_feature_class_to_append"
            object_list = [self.mock_generic_object]
            field_attribute_lookup = OrderedDict()
            template_feature_class_path = "template_feature_class_path"
            target_path = "target_path"
            self.db_data_io.append_feature_class_to_db(object_list, field_attribute_lookup, template_feature_class_path, target_path)
            mock_create_feature_class_from_objects.assert_called_with(output_feature_class_name, object_list, field_attribute_lookup, template_feature_class_path)

    def test_append_feature_class_to_db_calls_append_with_correct_arguments(self):
        with mock.patch.object(self.db_data_io, "create_feature_class_from_objects") as mock_create_feature_class_from_objects:
            with mock.patch.object(self.db_data_io, "_create_field_map_for_sde_db") as mock_create_field_map_for_sde_db:
                self.db_data_io.workspace = "in_memory"
                output_feature_class_name = "intermediate_feature_class_to_append"
                object_list = [self.mock_generic_object]
                field_attribute_lookup = OrderedDict()
                template_feature_class_path = "template_feature_class_path"
                target_path = "target_path"
                mock_create_field_map_for_sde_db.return_value = "field_mapping_for_sde_db"

                self.db_data_io.append_feature_class_to_db(object_list, field_attribute_lookup, template_feature_class_path,
                                                           target_path)
                self.mock_append.assert_called_with("in_memory\\intermediate_feature_class_to_append", "target_path", "NO_TEST", "field_mapping_for_sde_db")







