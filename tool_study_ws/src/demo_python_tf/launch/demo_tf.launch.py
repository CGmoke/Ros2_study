import launch
import launch_ros

def generate_launch_description():
    """产生launch描述"""
    #静态坐标发布：base_link->camera_link
    action_node_static_tf = launch_ros.actions.Node(
        package='demo_python_tf',
        executable='static_tf_broadcaster',
        output='screen'
    )
    #动态坐标发布：base_link->camera_link
    action_node_dynamic_tf = launch_ros.actions.Node(
        package='demo_python_tf',
        executable='dynamic_tf_broadcaster',
        output='screen'
    )
    #坐标监听：查询 base_link -> camera_link
    # action_node_tf_listener = launch_ros.actions.Node(
    #     package='demo_python_tf',
    #     executable='tf_listener',
    #     output='screen'
    # )
    #组织动作成组
    action_group = launch.actions.GroupAction([
        action_node_static_tf,
        action_node_dynamic_tf,
        # action_node_tf_listener
    ])
    return launch.LaunchDescription([
        action_group
    ])