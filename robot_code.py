motor = "6_948929816730218549"
forward = "w"
left = "a"
backward = "s"
right = "d"

def autonomous():
    Robot.set_value(motor, "invert_a", True)
    Robot.set_value(motor, "pid_enabled_a", False)
    Robot.set_value(motor, "pid_enabled_b", False)

    last_seen = "center"

    while True:
        left_sensor = Robot.get_value("line_follower", "left")
        center_sensor = Robot.get_value("line_follower", "center")
        right_sensor = Robot.get_value("line_follower", "right")

        left_on = left_sensor > 0.5
        center_on = center_sensor > 0.5
        right_on = right_sensor > 0.5

        if center_on and not left_on and not right_on:
            Robot.set_value(motor, "velocity_a", 0.7)
            Robot.set_value(motor, "velocity_b", 0.7)
            last_seen = "center"

        elif left_on and not center_on:
            Robot.set_value(motor, "velocity_a", 0.75)
            Robot.set_value(motor, "velocity_b", 0.25)
            last_seen = "left"

        elif right_on and not center_on:
            Robot.set_value(motor, "velocity_a", 0.25)
            Robot.set_value(motor, "velocity_b", 0.75)
            last_seen = "right"

        elif left_on and center_on and not right_on:
            Robot.set_value(motor, "velocity_a", 0.7)
            Robot.set_value(motor, "velocity_b", 0.35)
            last_seen = "left"

        elif right_on and center_on and not left_on:
            Robot.set_value(motor, "velocity_a", 0.35)
            Robot.set_value(motor, "velocity_b", 0.7)
            last_seen = "right"

        elif left_on and center_on and right_on:
            Robot.set_value(motor, "velocity_a", 0.65)
            Robot.set_value(motor, "velocity_b", 0.65)
            last_seen = "center"

        else:
            if last_seen == "left":
                Robot.set_value(motor, "velocity_a", 0.7)
                Robot.set_value(motor, "velocity_b", 0.2)
            elif last_seen == "right":
                Robot.set_value(motor, "velocity_a", 0.2)
                Robot.set_value(motor, "velocity_b", 0.7)
            else:
                Robot.set_value(motor, "velocity_a", 0)
                Robot.set_value(motor, "velocity_b", 0)

        Robot.sleep(0.02)
    
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
