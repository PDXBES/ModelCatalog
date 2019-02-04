from unittest import TestCase
import mock
from testbusinessclasses.mock_config import MockConfig
import arcpy
from dataio.object_data_io import ObjectDataIo
from businessclasses.generic_object import GenericObject
from collections import OrderedDict
from dataio.db_data_io import DbDataIo


class TestObjectDataIo(TestCase):

    def setUp(self):
        mock_config = MockConfig()
        self.config = mock_config.config
        self.parent_id = 1
        self.save_changes = True

        self.mock_db_data_io = mock.MagicMock(DbDataIo)
        self.mock_Editor = mock.MagicMock(arcpy.da.Editor)

        self.object_data_io = ObjectDataIo(self.config, self.mock_db_data_io)
        self.object_class = None
        self.field_names_retrieve_id = ["Object_Type", "Current_ID"]

        self.patch_da_InsertCursor = mock.patch("arcpy.da.InsertCursor")
        self.mock_da_InsertCursor = self.patch_da_InsertCursor.start()

        self.mock_generic_object = mock.MagicMock(GenericObject)
        self.mock_generic_object.id = 1
        self.mock_generic_object.name = "name"
        self.mock_generic_object.valid = False

        self.field_attribute_lookup = OrderedDict()
        self.field_attribute_lookup["id_field"] = "id"
        self.field_attribute_lookup["name"] = "name"

        self.object_table_sde_path = "object_tracking_sde_path"

        self.patch_da_Editor = mock.patch("arcpy.da.Editor")
        self.mock_da_Editor = self.patch_da_Editor.start()
        self.mock_da_Editor.return_value = self.mock_Editor

        self.patch_startEditing = mock.patch("arcpy.da.Editor.startEditing")
        self.mock_startEditing = self.patch_startEditing.start()

        self.patch_startOperation = mock.patch("arcpy.da.Editor.startOperation")
        self.mock_startOperation = self.patch_startOperation.start()

        self.patch_stopOperation = mock.patch("arcpy.da.Editor.stopOperation")
        self.mock_stopOperation = self.patch_stopOperation.start()

        self.patch_stopEditing = mock.patch("arcpy.da.Editor.stopEditing")
        self.mock_stopEditing = self.patch_stopEditing.start()

    def tearDown(self):
        self.mock_da_InsertCursor = self.patch_da_InsertCursor.stop()
        self.mock_da_Editor = self.patch_da_Editor.stop()
        self.mock_startEditing = self.patch_startEditing.stop()
        self.mock_startOperation = self.patch_startOperation.stop()
        self.mock_stopOperation = self.patch_stopOperation.stop()
        self.mock_stopEditing = self.patch_stopEditing.stop()

    def test_add_object_sets_generic_object_parent_id(self):
        self.mock_generic_object.valid = True
        self.mock_generic_object.parent_id = None
        self.object_data_io.add_object(self.parent_id, self.mock_generic_object, self.field_attribute_lookup, self.object_table_sde_path)
        self.assertEqual(self.mock_generic_object.parent_id, 1)

    def test_add_object_calls_db_data_io_add_object_with_correct_arguments(self):
        self.mock_generic_object.valid = True
        self.object_data_io.add_object(self.parent_id, self.mock_generic_object,
                                       self.field_attribute_lookup, self.object_table_sde_path)
        self.mock_db_data_io.add_object.assert_called_with(self.mock_generic_object, self.field_attribute_lookup, self.object_table_sde_path)

    def test_start_editing_session_creates_editor_object(self):
        workspace_path = "workspace_path"
        self.object_data_io.start_editing_session(workspace_path)
        self.mock_da_Editor.assert_called_with(workspace_path)

    def test_start_editing_session_starts_editing(self):
        workspace_path = "workspace_path"
        with_undo = False
        multiuser_mode = True
        editor = self.object_data_io.start_editing_session(workspace_path)
        start_editing_arguments = editor.startEditing.call_args[0]
        self.assertEqual(start_editing_arguments,(with_undo, multiuser_mode))

    def test_start_editing_session_starts_operation(self):
        workspace_path = "workspace_path"
        editor = self.object_data_io.start_editing_session(workspace_path)
        start_operation_called = editor.startOperation.called
        self.assertTrue(start_operation_called)

    def test_stop_editing_session_calls_stop_operation(self):
        self.object_data_io.stop_editing_session(self.mock_Editor, self.save_changes)
        stop_operation_called = self.mock_Editor.stopOperation.called
        self.assertTrue(stop_operation_called)

    def test_stop_editing_session_calls_stop_editing(self):
        self.object_data_io.stop_editing_session(self.mock_Editor, self.save_changes)
        stop_editing_arguments = self.mock_Editor.stopEditing.call_args[0][0]
        self.assertEqual(stop_editing_arguments, self.save_changes)