import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    # 本项目自带的一份 slam_toolbox 参数（已按 fishbot 雷达量程和车体尺寸调过）
    default_params_file = os.path.join(
        get_package_share_directory("fishbot_description"),
        "config",
        "mapper_params_online_async.yaml",
    )
    default_slam_launch = os.path.join(
        get_package_share_directory("slam_toolbox"), "launch", "online_async_launch.py"
    )

    use_sim_time = LaunchConfiguration("use_sim_time")
    slam_params_file = LaunchConfiguration("slam_params_file")

    return LaunchDescription([
        DeclareLaunchArgument(
            "use_sim_time",
            default_value="true",
            description="使用仿真/Gazebo 时钟",
        ),
        DeclareLaunchArgument(
            "slam_params_file",
            default_value=default_params_file,
            description="slam_toolbox 参数文件路径",
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(default_slam_launch),
            launch_arguments={
                "use_sim_time": use_sim_time,
                "slam_params_file": slam_params_file,
            }.items(),
        ),
    ])