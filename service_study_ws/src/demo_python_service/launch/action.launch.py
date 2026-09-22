import os

import launch
import launch_ros
import launch.launch_description_sources
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    #动作1-启动其他launch文件
    multisim_launch_path = os.path.join(
        get_package_share_directory('turtlesim'), 'launch', 'multisim.launch.py'
    )
    action_include_launch = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource(
            multisim_launch_path
        )
    )
    #动作2-打印数据
    action_log_info = launch.actions.LogInfo(
        msg=['包含的launch文件路径: ', multisim_launch_path]
    )
    #动作3-执行进程（同一个动作对象只能执行一次，需要执行两次要创建两个对象）
    action_topic_list = launch.actions.ExecuteProcess(
        cmd=['ros2', 'topic', 'list'],
        output='screen'
    )
    action_topic_list_2 = launch.actions.ExecuteProcess(
        cmd=['ros2', 'topic', 'list'],
        output='screen'
    )
    #动作4-组织动作成组，把多个动作放到一个组
    action_group = launch.actions.GroupAction([
        launch.actions.TimerAction(period=2.0, actions=[action_topic_list]),
        launch.actions.TimerAction(period=4.0, actions=[action_log_info]),
        launch.actions.TimerAction(period=6.0, actions=[action_topic_list_2])
    ])

    return launch.LaunchDescription([
        action_include_launch,
        action_group
    ])
