#打包时，这些文件需要手动引入以下，否则Pyinstaller打不进包
#这些包都不是显式import的，比如调用__import__引入的
import ui_design.dialog_export
import ui_design.dialog_new_workspace
import ui_design.dialog_scene_setting
import ui_design.main_window
import ui_design.widget_action_property
import ui_design.widget_assignment_property
import ui_design.widget_calculate_property
import ui_design.widget_common_property_comment
import ui_design.widget_common_property_debug
import ui_design.widget_common_property_empty
import ui_design.widget_condition_property
import ui_design.widget_default_property
import ui_design.widget_empty_property
import ui_design.widget_example_property
import ui_design.widget_finish_property
import ui_design.widget_probabilistic_choice_property
import ui_design.widget_subtree_property
import ui_design.widget_wait_property
import ui_design.widget_weight_property
