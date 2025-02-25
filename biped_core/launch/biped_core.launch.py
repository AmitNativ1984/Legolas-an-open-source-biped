from launch import LaunchDescription
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution, LaunchConfiguration

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition



def generate_launch_description():
    # Get URDF via xacro

    urdf_path = get_package_share_directory('biped_core') + '/description/robot.urdf.xacro'
    
    robot_description = DeclareLaunchArgument("robot_description", default_value=urdf_path,
                                             description="Path to robot description file")
    
    state_publish_freq = DeclareLaunchArgument("state_publish_freq", default_value="50.0", 
                                         description="Frequency of publishing joint states")
    
    joint_publish_freq = DeclareLaunchArgument("joint_publish_freq", default_value="50.0",
                                         description="Frequency of publishing joint states")
    
    joint_state_topic = DeclareLaunchArgument("joint_state_topic", default_value="/joint_states",
                                              description="Topic name for joint states")
    
    publish_joint_state = DeclareLaunchArgument("publish_joint_state", default_value="false",
                                                description="Publish joint states")
    
    
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{
            'robot_description': Command([FindExecutable(name='xacro'), ' ', LaunchConfiguration('robot_description')]),
            'publish_frequency': LaunchConfiguration('state_publish_freq'),
            'use_tf_static': True
        }],
        remappings=[('/joint_states', LaunchConfiguration('joint_state_topic'))]
    )

    joint_state_publisher_node = Node(
        condition=IfCondition(LaunchConfiguration('publish_joint_state')),
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{
            'robot_description': Command([FindExecutable(name='xacro'), ' ', LaunchConfiguration('robot_description')]),
            'rate': LaunchConfiguration('joint_publish_freq'),
            'publish_default_positions': True
        }]
    )

    launch_me = LaunchDescription()
    launch_me.add_action(robot_description)
    launch_me.add_action(state_publish_freq)
    launch_me.add_action(joint_publish_freq)
    launch_me.add_action(joint_state_topic)
    launch_me.add_action(publish_joint_state)
    launch_me.add_action(robot_state_publisher_node)
    launch_me.add_action(joint_state_publisher_node)

    return launch_me
