import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
from launch_ros.parameter_descriptions import ParameterValue
import os 

def generate_launch_description():
    #获取固定的urdf文件路径
    urdf_package_path = get_package_share_directory("fishbot_description")
    default_xacro_path = os.path.join(urdf_package_path, "urdf", "fishbot", "fishbot.urdf.xacro")
    # default_rviz_config_path = os.path.join(urdf_package_path, "config", "display_robot_model.rviz")
    default_gazebo_world_path = os.path.join(urdf_package_path, "world", "custom_room.world")
    #声明一个urdf目录的参数，方便修改
    action_declare_arg_mode_path = launch.actions.DeclareLaunchArgument(
        name = "model",
        default_value=str(default_xacro_path),
        description="加载的模型文件路径",
    )
    #通过文件路径，获取内部内容，并转换成参数值对象，以供传入 robot_state_publisher 节点
    substitutions_command_result  = launch.substitutions.Command(["xacro ", launch.substitutions.LaunchConfiguration("model")])
    robot_description_value = ParameterValue(substitutions_command_result, value_type=str)
    
    action_robot_state_publisher = launch_ros.actions.Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description_value}],
        name="robot_state_publisher",
        output="screen",
    )
    action_launch_gazebo = launch.actions.IncludeLaunchDescription(
        launch_description_source=launch.substitutions.PathJoinSubstitution(
            [get_package_share_directory("gazebo_ros"), "launch", "gazebo.launch.py"]
        ),
        launch_arguments=[("world", default_gazebo_world_path), ("verbose", "true")],
    )
    action_spawn_entity = launch_ros.actions.Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=["-topic", "/robot_description", "-entity", "fishbot"],
        output="screen",
    )
    # 使用 spawner 加载并激活控制器：它会自动等待 controller_manager 就绪，避免与 spawn 的竞态
    load_joint_state_controller = launch.actions.ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
            'fishbot_joint_state_broadcaster'],
        output='screen'
    )
    #加载并激活 fishbot_effort_controller 控制器
    load_fishbot_effort_controller = launch.actions.ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active','fishbot_effort_controller'], 
        output='screen')
    
    load_fishbot_diff_drive_controller = launch.actions.ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active','fishbot_diff_drive_controller'], 
        output='screen')

    return launch.LaunchDescription([
        action_declare_arg_mode_path,
        action_robot_state_publisher,
        action_launch_gazebo,
        action_spawn_entity,
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=action_spawn_entity,
                on_exit=[load_joint_state_controller,],
            )
        ),
        launch.actions.RegisterEventHandler(
                event_handler=launch.event_handlers.OnProcessExit(
                    target_action=load_joint_state_controller,
                    on_exit=[load_fishbot_effort_controller],)
                    ),
        # launch.actions.RegisterEventHandler(
        # event_handler=launch.event_handlers.OnProcessExit(
        #     target_action=load_joint_state_controller,
        #     on_exit=[load_fishbot_diff_drive_controller],)
        #     ),
        

])