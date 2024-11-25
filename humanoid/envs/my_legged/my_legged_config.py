from humanoid.envs.base.legged_robot_config import LeggedRobotCfg, LeggedRobotCfgPPO

class MyLeggedCfg(LeggedRobotCfg):
    """
    Configuration class for robot.
    """
    class env(LeggedRobotCfg.env):
        # change the observation dim
        frame_stack = 66      #all histroy obs num
        short_frame_stack = 5   #short history step
        c_frame_stack = 3  #all histroy privileged obs num
        num_single_obs = 41
        num_observations = int(frame_stack * num_single_obs)
        single_num_privileged_obs = 65
        single_linvel_index = 53
        num_privileged_obs = int(c_frame_stack * single_num_privileged_obs)
        num_actions = 10
        num_envs = 4096
        episode_length_s = 24 #episode length in seconds
        use_ref_actions = False
        num_commands = 5 # sin_pos cos_pos vx vy vz

    class safety:
        # safety factors
        pos_limit = 1.0
        vel_limit = 1.0
        torque_limit = 0.85


    class asset(LeggedRobotCfg.asset):
        file = '{LEGGED_GYM_ROOT_DIR}/resources/robots/my_legged/urdf/urdf.urdf'
        #xml_file = '{LEGGED_GYM_ROOT_DIR}/resources/robots/x1/mjcf/xyber_x1_flat.xml'
        #用于sim2sim到mujoco
    
        name = "my_legged"
        foot_name = "ankle_roll"
        knee_name = "knee_pitch"

        terminate_after_contacts_on = ['base_link'] #指定机器人中某些部件（如 base_link）触地后是否终止仿真，例如用于训练中防止不合理动作。
        penalize_contacts_on = ["base_link"] #penalize_contacts_on: 指定机器人中哪些部件的接触会被惩罚，例如用来优化接触行为。
        self_collisions = 1  # 1 to disable, 0 to enable...bitwise filter 自碰撞开关
        flip_visual_attachments = False #是否反转视觉附件方向
        replace_cylinder_with_capsule = False #是否用胶囊代替圆柱
        fix_base_link = False #是否固定 base_link，固定后机器人无法移动。通常用于调试或需要静态测试时。

    class terrain(LeggedRobotCfg.terrain):
        # mesh_type = 'plane'
        mesh_type = 'trimesh'
        curriculum = False
        # rough terrain only:
        measure_heights = False
        static_friction = 0.6
        dynamic_friction = 0.6
        terrain_length = 8.
        terrain_width = 8.
        num_rows = 20  # number of terrain rows (levels)
        num_cols = 20  # number of terrain cols (types)
        max_init_terrain_level = 5  # starting curriculum state
        platform = 3.
        terrain_dict = {"flat": 0.3, 
                        "rough flat": 0.2,
                        "slope up": 0.2,
                        "slope down": 0.2, 
                        "rough slope up": 0.0,
                        "rough slope down": 0.0, 
                        "stairs up": 0., 
                        "stairs down": 0.,
                        "discrete": 0.1, 
                        "wave": 0.0,}
        terrain_proportions = list(terrain_dict.values())

        rough_flat_range = [0.005, 0.01]  # meter
        slope_range = [0, 0.1]   # rad
        rough_slope_range = [0.005, 0.02]
        stair_width_range = [0.25, 0.25]
        stair_height_range = [0.01, 0.1]
        discrete_height_range = [0.0, 0.01]
        restitution = 0.

    class noise(LeggedRobotCfg.noise):
        add_noise = True
        noise_level = 1.0    # scales other values

        class noise_scales(LeggedRobotCfg.noise.noise_scales):
            dof_pos = 0.01
            dof_vel = 1.0 
            ang_vel = 0.1   
            lin_vel = 0.1   
            quat = 0.1
            gravity = 0.05
            height_measurements = 0.05


    class init_state(LeggedRobotCfg.init_state):
        pos = [0.0, 0.0, 0.7]

        default_joint_angles = {  # = target angles [rad] when action = 0.0
            'left_hip_pitch_joint': 0,
            'left_hip_roll_joint': 0,
            'left_knee_pitch_joint': 0,
            'left_ankle_pitch_joint': 0,
            'left_ankle_roll_joint': 0,
            'right_hip_pitch_joint': 0,
            'right_hip_roll_joint': 0,
            'right_knee_pitch_joint': 0,
            'right_ankle_pitch_joint': 0, 
            'right_ankle_roll_joint': 0,
        }

    class control(LeggedRobotCfg.control):
        # PD Drive parameters:
        control_type = 'P'

        stiffness = {'hip_pitch_joint': 30,'hip_roll_joint': 35,
                     'knee_pitch_joint': 100, 'ankle_pitch_joint': 35, 'ankle_roll_joint': 35}
        damping = {'hip_pitch_joint': 3,'hip_roll_joint': 4, 
                   'knee_pitch_joint': 10, 'ankle_pitch_joint': 0.5, 'ankle_roll_joint': 0.5}

        # action scale: target angle = actionScale * action + defaultAngle
        action_scale = 0.2
        # decimation: Number of control action updates @ sim DT per policy DT
        decimation = 10  # 50hz 100hz

    class sim(LeggedRobotCfg.sim):
        dt = 0.001  # 200 Hz 1000 Hz
        substeps = 1  # 2
        up_axis = 1  # 0 is y, 1 is z
     
        class physx(LeggedRobotCfg.sim.physx):
            num_threads = 10
            solver_type = 1  # 0: pgs, 1: tgs
            num_position_iterations = 4
            num_velocity_iterations = 0
            contact_offset = 0.01  # [m]
            rest_offset = 0.0   # [m]
            bounce_threshold_velocity = 0.5  # 0.5 #0.5 [m/s]
            max_depenetration_velocity = 1.0
            max_gpu_contact_pairs = 2**23  # 2**24 -> needed for 8000 envs and more
            default_buffer_size_multiplier = 5
            # 0: never, 1: last sub-step, 2: all sub-steps (default=2)
            contact_collection = 2

    class domain_rand(LeggedRobotCfg.domain_rand):
        randomize_friction = True
        friction_range = [0.2, 1.3]
        restitution_range = [0.0, 0.4]

        # push
        push_robots = True
        push_interval_s = 4 # every this second, push robot
        update_step = 2000 * 24 # after this count, increase push_duration index
        push_duration = [0, 0.05, 0.1, 0.15, 0.2, 0.25] # increase push duration during training
        max_push_vel_xy = 0.2
        max_push_ang_vel = 0.2

        randomize_base_mass = True
        added_mass_range = [-3, 3] # base mass rand range, base mass is all fix link sum mass

        randomize_com = True
        com_displacement_range = [[-0.05, 0.05],
                                  [-0.05, 0.05],
                                  [-0.05, 0.05]]

        randomize_gains = True
        stiffness_multiplier_range = [0.8, 1.2]  # Factor
        damping_multiplier_range = [0.8, 1.2]    # Factor

        randomize_torque = True
        torque_multiplier_range = [0.8, 1.2]

        randomize_link_mass = True
        added_link_mass_range = [0.9, 1.1]

        randomize_motor_offset = True
        motor_offset_range = [-0.035, 0.035] # Offset to add to the motor angles
        
        randomize_joint_friction = True
        randomize_joint_friction_each_joint = False
        joint_friction_range = [0.01, 1.15]
        joint_1_friction_range = [0.01, 1.15]
        joint_2_friction_range = [0.01, 1.15]
        joint_3_friction_range = [0.01, 1.15]
        joint_4_friction_range = [0.5, 1.3]
        joint_5_friction_range = [0.5, 1.3]
        joint_6_friction_range = [0.01, 1.15]
        joint_7_friction_range = [0.01, 1.15]
        joint_8_friction_range = [0.01, 1.15]
        joint_9_friction_range = [0.5, 1.3]
        joint_10_friction_range = [0.5, 1.3]

        randomize_joint_damping = True
        randomize_joint_damping_each_joint = False
        joint_damping_range = [0.3, 1.5]
        joint_1_damping_range = [0.3, 1.5]
        joint_2_damping_range = [0.3, 1.5]
        joint_3_damping_range = [0.3, 1.5]
        joint_4_damping_range = [0.9, 1.5]
        joint_5_damping_range = [0.9, 1.5]
        joint_6_damping_range = [0.3, 1.5]
        joint_7_damping_range = [0.3, 1.5]
        joint_8_damping_range = [0.3, 1.5]
        joint_9_damping_range = [0.9, 1.5]
        joint_10_damping_range = [0.9, 1.5]

        randomize_joint_armature = True
        randomize_joint_armature_each_joint = False
        joint_armature_range = [0.0001, 0.05]     # Factor
        joint_1_armature_range = [0.0001, 0.05]
        joint_2_armature_range = [0.0001, 0.05]
        joint_3_armature_range = [0.0001, 0.05]
        joint_4_armature_range = [0.0001, 0.05]
        joint_5_armature_range = [0.0001, 0.05]
        joint_6_armature_range = [0.0001, 0.05]
        joint_7_armature_range = [0.0001, 0.05]
        joint_8_armature_range = [0.0001, 0.05]
        joint_9_armature_range = [0.0001, 0.05]
        joint_10_armature_range = [0.0001, 0.05]

        add_lag = False
        randomize_lag_timesteps = False
        randomize_lag_timesteps_perstep = False
        lag_timesteps_range = [5, 40]
        
        add_dof_lag = False
        randomize_dof_lag_timesteps = False
        randomize_dof_lag_timesteps_perstep = False
        dof_lag_timesteps_range = [0, 40]
        
        add_dof_pos_vel_lag = False
        randomize_dof_pos_lag_timesteps = False
        randomize_dof_pos_lag_timesteps_perstep = False
        dof_pos_lag_timesteps_range = [7, 25]
        randomize_dof_vel_lag_timesteps = False
        randomize_dof_vel_lag_timesteps_perstep = False
        dof_vel_lag_timesteps_range = [7, 25]
        
        add_imu_lag = False
        randomize_imu_lag_timesteps = False
        randomize_imu_lag_timesteps_perstep = False
        imu_lag_timesteps_range = [1, 10]
        
        randomize_coulomb_friction = False
        joint_coulomb_range = [0.1, 0.9]
        joint_viscous_range = [0.05, 0.1]
        
    class commands(LeggedRobotCfg.commands):
        curriculum = True
        max_curriculum = 1.5
        # Vers: lin_vel_x, lin_vel_y, ang_vel_yaw, heading (in heading mode ang_vel_yaw is recomputed from heading error)
        num_commands = 4
        resampling_time = 25.  # time before command are changed[s]
        gait = ["walk_omnidirectional","stand","walk_omnidirectional"] # gait type during training
        # proportion during whole life time
        gait_time_range = {"walk_sagittal": [2,6],
                           "walk_lateral": [2,6],
                           "rotate": [2,3],
                           "stand": [2,3],
                           "walk_omnidirectional": [4,6]}

        heading_command = False  # if true: compute ang vel command from heading error
        stand_com_threshold = 0.05 # if (lin_vel_x, lin_vel_y, ang_vel_yaw).norm < this, robot should stand
        sw_switch = True # use stand_com_threshold or not

        class ranges:
            lin_vel_x = [-0.4, 1.2] # min max [m/s] 
            lin_vel_y = [-0.4, 0.4]   # min max [m/s]
            ang_vel_yaw = [-0.6, 0.6]    # min max [rad/s]
            heading = [-3.14, 3.14]

    class rewards:
        soft_dof_pos_limit = 0.98
        soft_dof_vel_limit = 0.9
        soft_torque_limit = 0.9
        base_height_target = 0.61
        foot_min_dist = 0.2
        foot_max_dist = 1.0

        # final_swing_joint_pos = final_swing_joint_delta_pos + default_pos
        final_swing_joint_delta_pos = [0.25, -0.11, 0.35, -0.16, 0.0, -0.25, 0.11, 0.35, -0.16, 0.0]
        target_feet_height = 0.03 
        target_feet_height_max = 0.2
        feet_to_ankle_distance = 0.041
        cycle_time = 0.7
        # if true negative total rewards are clipped at zero (avoids early termination problems)
        only_positive_rewards = True
        # tracking reward = exp(-error*sigma)
        tracking_sigma = 5 
        max_contact_force = 700  # forces above this value are penalized
        
        class scales:
            ref_joint_pos = 2.2
            feet_clearance = 1.
            feet_contact_number = 2.0
            # gait
            feet_air_time = 1.2
            foot_slip = -0.1
            feet_distance = 0.2
            knee_distance = 0.2
            # contact 
            feet_contact_forces = -0.01
            # vel tracking
            tracking_lin_vel = 1.8
            tracking_ang_vel = 1.1
            vel_mismatch_exp = 0.5  # lin_z; ang x,y
            low_speed = 0.2
            track_vel_hard = 0.5
            # base pos
            default_joint_pos = 1.0
            orientation = 1.
            feet_rotation = 0.3
            base_height = 0.2
            base_acc = 0.2
            # energy
            action_smoothness = -0.002
            torques = -8e-9
            dof_vel = -2e-8
            dof_acc = -1e-7
            collision = -1.
            stand_still = 2.5
            # limits
            dof_vel_limits = -1
            dof_pos_limits = -10.
            dof_torque_limits = -0.1

    class normalization:
        class obs_scales:
            lin_vel = 2.
            ang_vel = 1.
            dof_pos = 1.
            dof_vel = 0.05
            quat = 1.
            height_measurements = 5.0
        clip_observations = 100.
        clip_actions = 100.


class MyLeggedCfgPPO(LeggedRobotCfgPPO):
    seed = 5
    runner_class_name = 'DHOnPolicyRunner'   # DWLOnPolicyRunner

    class policy:
        init_noise_std = 1.0
        actor_hidden_dims = [512, 256, 128]
        critic_hidden_dims = [768, 256, 128]
        state_estimator_hidden_dims=[256, 128, 64]
        
        #for long_history cnn only
        kernel_size=[6, 4]
        filter_size=[32, 16]
        stride_size=[3, 2]
        lh_output_dim= 64   #long history output dim
        in_channels = MyLeggedCfg.env.frame_stack

    class algorithm(LeggedRobotCfgPPO.algorithm):
        entropy_coef = 0.001
        learning_rate = 1e-5
        num_learning_epochs = 2
        gamma = 0.994
        lam = 0.9
        num_mini_batches = 4
        if MyLeggedCfg.terrain.measure_heights:
            lin_vel_idx = (MyLeggedCfg.env.single_num_privileged_obs + MyLeggedCfg.terrain.num_height) * (MyLeggedCfg.env.c_frame_stack - 1) + MyLeggedCfg.env.single_linvel_index
        else:
            lin_vel_idx = MyLeggedCfg.env.single_num_privileged_obs * (MyLeggedCfg.env.c_frame_stack - 1) + MyLeggedCfg.env.single_linvel_index

    class runner:
        policy_class_name = 'ActorCriticDH'
        algorithm_class_name = 'DHPPO'
        num_steps_per_env = 24  # per iteration
        max_iterations = 20000  # number of policy updates

        # logging
        save_interval = 100  # check for potential saves every this many iterations
        experiment_name = 'my_legged'
        run_name = ''
        # load and resume
        resume = False
        load_run = -1  # -1 = last run
        checkpoint = -1  # -1 = last saved model
        resume_path = None  # updated from load_run and chkpt
