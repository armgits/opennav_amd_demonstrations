from launch import LaunchDescription
from launch.actions import GroupAction

from launch_ros.actions import LoadComposableNodes, Node
from launch_ros.descriptions import ComposableNode

def generate_launch_description():
    depth_pointcloud_proc = GroupAction([
        Node(
            name='depth_pointcloud_proc_container',
            package='rclcpp_components',
            executable='component_container_isolated',
            parameters=[],
            arguments=['--ros-args', '--log-level', 'info'],
            output='screen'),
        
        LoadComposableNodes(
            target_container='depth_pointcloud_proc_container',
            composable_node_descriptions =[
                ComposableNode(
                    package='depth_image_proc',
                    plugin='depth_image_proc::RegisterNode',
                    name='depth_register',
                    namespace='sensors',
                    remappings=[
                        ('depth/image_rect',             '/sensors/camera_0/depth/image'),
                        ('depth/camera_info',            '/sensors/camera_0/depth/camera_info'),
                        ('rgb/camera_info',              '/sensors/camera_0/color/camera_info'),
                        ('depth_registered/image_rect',  '/sensors/camera_0/depth_registered/image'),
                        ('depth_registered/camera_info', '/sensors/camera_0/depth_registered/camera_info'),
                    ],
                ),

                ComposableNode(
                    package='depth_image_proc',
                    plugin='depth_image_proc::PointCloudXyzNode',
                    name='point_cloud_xyz',
                    namespace='sensors',
                    remappings=[
                        ('image_rect',  '/sensors/camera_0/depth_registered/image'),
                        ('camera_info', '/sensors/camera_0/depth_registered/camera_info'),
                        ('points',      '/sensors/camera_0/points'),
                    ],
                ),

                # ComposableNode(
                #     package='image_proc',
                #     plugin='image_proc::ResizeNode',
                #     name='mask_resize',
                #     remappings=[
                #         ('/image/image_raw',    '/sam3_inference/label_mask'),
                #         ('/sam3_inference/camera_info',    '/sensors/camera_0/color/camera_info'),
                #         # /image/camera_info actually changes namespace to whatever /image/image_raw gets remapped to. 
                #         ('/resize/image_raw',   '/sam3_inference_post/label_mask'),
                #         ('/sam3_inference_post/camera_info',    '/sensors/camera_0/color/camera_info_resized'),
                #         # /resize/camera_info actually changes namespace to whatever /resize/image_raw gets remapped to.
                #     ],
                #     parameters=[{
                #         'use_scale':     False,
                #         'width':         424,
                #         'height':        240,
                #         'interpolation': 0,  # NEAREST — required for label masks
                #     }],
                # ),
            ],
        ),
    ])

    return LaunchDescription([depth_pointcloud_proc])