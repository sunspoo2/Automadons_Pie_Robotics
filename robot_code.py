motor = "6_948929816730218549"
forward = "w"
left = "a"
backward = "s"
right = "d"

def autonomous():
    Robot.set_value(motor, "invert_a", True)
    Robot.set_value(motor, "velocity_a", 1)
    Robot.set_value(motor, "velocity_b", 1)
    
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