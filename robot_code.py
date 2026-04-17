motor = "6_948929816730218549"
forward = "w"
left = "a"
backward = "s"
right = "d"

def autonomous():
    Robot.set_value(motor, "invert_a", True)
    Robot.set_value(motor, "pid_enabled_a", False)
    Robot.set_value(motor, "pid_enabled_b", False)

    # Line follower device ID from DAWN.
    line_sensor = "2_2564895989332655657"

    # Tune these at the field: this version is based on relative contrast
    # so it works better when line colors vary (red/blue/green/yellow).
    line_is_dark = True
    min_contrast = 0.06
    confidence_margin = 0.025
    forward_speed = 0.58
    gentle_turn = 0.26
    hard_turn = 0.42
    lost_turn = 0.34

    # Keep track of which side saw the line most recently.
    # -1 = left, 0 = center/unknown, +1 = right
    last_side = 0

    while True:
        left_sensor = Robot.get_value(line_sensor, "left")
        center_sensor = Robot.get_value(line_sensor, "center")
        right_sensor = Robot.get_value(line_sensor, "right")

        # Use relative differences instead of absolute threshold so different
        # tape colors are still detectable.
        if line_is_dark:
            left_score = -left_sensor
            center_score = -center_sensor
            right_score = -right_sensor
        else:
            left_score = left_sensor
            center_score = center_sensor
            right_score = right_sensor

        best_score = max(left_score, center_score, right_score)
        worst_score = min(left_score, center_score, right_score)
        contrast = best_score - worst_score

        # If contrast is weak, assume line is lost.
        if contrast < min_contrast:
            left_on = False
            center_on = False
            right_on = False
        else:
            left_on = left_score >= best_score - confidence_margin
            center_on = center_score >= best_score - confidence_margin
            right_on = right_score >= best_score - confidence_margin

        # Center sensor locked => drive forward.
        if center_on and not left_on and not right_on:
            left_speed = forward_speed
            right_speed = forward_speed
            last_side = 0

        # Line is drifting left of robot => steer left.
        elif left_on and not right_on:
            left_speed = gentle_turn
            right_speed = forward_speed + 0.06
            last_side = -1

        # Line is drifting right of robot => steer right.
        elif right_on and not left_on:
            left_speed = forward_speed + 0.06
            right_speed = gentle_turn
            last_side = 1

        # Large offset or branch: use a hard correction toward the stronger side.
        elif left_on and center_on and not right_on:
            left_speed = hard_turn
            right_speed = forward_speed + 0.08
            last_side = -1
        elif right_on and center_on and not left_on:
            left_speed = forward_speed + 0.08
            right_speed = hard_turn
            last_side = 1

        # All sensors see line (cross/intersection): keep moving through.
        elif left_on and center_on and right_on:
            left_speed = forward_speed
            right_speed = forward_speed
            last_side = 0

        # No sensor sees line: recover by turning toward last seen direction.
        else:
            if last_side <= 0:
                left_speed = lost_turn
                right_speed = -0.12
            else:
                left_speed = -0.12
                right_speed = lost_turn

        Robot.set_value(motor, "velocity_a", left_speed)
        Robot.set_value(motor, "velocity_b", right_speed)

        Robot.sleep(0.02)  # 50 Hz update
    
def teleop():
    Robot.set_value(motor, "invert_a", True)
    Robot.set_value(motor, "pid_enabled_a", False)
    Robot.set_value(motor, "pid_enabled_b", False)
    while True: 
        if Keyboard.get_value(forward):
            Robot.set_value(motor, "velocity_a", 1)
            Robot.set_value(motor, "velocity_b", 1)
            if Keyboard.get_value(left):
                Robot.set_value(motor, "velocity_a", 1)
                Robot.set_value(motor, "velocity_b", 0.2)
            if Keyboard.get_value(right):
                Robot.set_value(motor, "velocity_a", 0.2)
                Robot.set_value(motor, "velocity_b", 1)
        elif Keyboard.get_value(left):
            Robot.set_value(motor, "velocity_b", -1)
            Robot.set_value(motor, "velocity_a", 1)
        elif Keyboard.get_value(right):
            Robot.set_value(motor, "velocity_a", -1)
            Robot.set_value(motor, "velocity_b", 1)
        elif Keyboard.get_value(backward):
            Robot.set_value(motor, "velocity_a", -1)
            Robot.set_value(motor, "velocity_b", -1)
        else:
            Robot.set_value(motor, "velocity_a", 0)
            Robot.set_value(motor, "velocity_b", 0)
