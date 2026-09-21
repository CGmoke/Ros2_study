import launch
import launch_ros
import launch.launch_description_sources
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    #动作-启动其他launch
    action_include_launch = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.LaunchDescriptionSource(
            get_package_share_directory('demo_python_service') / 'launch' / 'demo.launch.py'
        ),
        launch_arguments={
            'launch_arg_bg': '150'
        }
    )
    return launch.LaunchDescription([
        action_include_launch
    ])