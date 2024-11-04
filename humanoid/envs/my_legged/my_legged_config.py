from humanoid.envs.base.legged_robot_config import LeggedRobotCfg, LeggedRobotCfgPPO

class MyLeggedRobotCfg(LeggedRobotCfg):
    class env(LeggedRobotCfg.env):
        frame_stack = 66
        short_frame_stack = 5
        c_frame_stack = 3
        num_single_obs = 47
        num_observations = int(frame_stack * num_single_obs)
        single_num_privileged_obs = 73
        single_linvel_index = 53
        num_privileged_obs = int(c_frame_stack * single_num_privileged_obs)
        num_actions = 12
        num_envs = 4096
        episode_length_s = 24 #episode length in seconds
        use_ref_actions = False
        num_commands = 5 # sin_pos cos_pos vx vy vz
    class safty :
        pos_limiot = 1.0
        vel_limit = 1.0
        torque_limit = 0.85
    class asset(LeggedRobotCfg.asset):
        