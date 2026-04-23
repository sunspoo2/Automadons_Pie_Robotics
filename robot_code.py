motor = "6_948929816730218549"
sensor = "2_2564895989332655657"
backward = "dpad_up"
left = "dpad_left"
forward = "dpad_down"
right = "dpad_right"

def autonomous():
    # helper inside autonomous (allowed)
    def clamp(x, lo=-1.0, hi=1.0):
        return max(lo, min(hi, x))

    # Motor configuration
    Robot.set_value(motor, "invert_a", True)
    Robot.set_value(motor, "pid_enabled_a", False)
    Robot.set_value(motor, "pid_enabled_b", False)

    # PID constants (starter values)
    Kp = 0.6
    Ki = 0.0          # keep 0 until Kp/Kd feels stable
    Kd = 0.10

    dt = 0.02
    base_speed = 0.5

    # Sensor calibration (YOU MUST SET floor_val)
    line_val = 0.96527
    floor_val = 0.30   # <-- replace with your measured floor reading
    target = (line_val + floor_val) / 2

    last_error = 0.0
    integral = 0.0

    while True:
        reading = Robot.get_value(sensor, "middle")

        # If sensor reading fails, stop briefly (safe)
        if reading is None:
            Robot.set_value(motor, "velocity_a", 0.0)
            Robot.set_value(motor, "velocity_b", 0.0)
            Robot.sleep(dt)
            continue

        # Lost-line/simple safety: if reading is extremely low, slow + gentle search
        # (tweak thresholds once you know floor reading)
        if reading < min(line_val, floor_val) + 0.02:
            Robot.set_value(motor, "velocity_a", 0.2)
            Robot.set_value(motor, "velocity_b", -0.2)
            Robot.sleep(dt)
            continue

        # Higher value = more on the line (your sensor behavior)
        error = reading - target

        # Integral with anti-windup clamp
        integral = clamp(integral + error * dt, -0.3, 0.3)

        # Derivative scaled by dt
        derivative = (error - last_error) / dt

        correction = (Kp * error) + (Ki * integral) + (Kd * derivative)

        left_speed = clamp(base_speed + correction)
        right_speed = clamp(base_speed - correction)

        Robot.set_value(motor, "velocity_a", left_speed)
        Robot.set_value(motor, "velocity_b", right_speed)

        last_error = error
        Robot.sleep(dt)
        
def teleop():
    Robot.set_value(motor, "invert_a", True)
    Robot.set_value(motor, "pid_enabled_a", False)
    Robot.set_value(motor, "pid_enabled_b", False)
    while True: 
        if Gamepad.get_value(forward):
            Robot.set_value(motor, "velocity_a", 1)
            Robot.set_value(motor, "velocity_b", 1)
            if Gamepad.get_value(left):
                Robot.set_value(motor, "velocity_a", 1)
                Robot.set_value(motor, "velocity_b", 0.2)
            if Gamepad.get_value(right):
                Robot.set_value(motor, "velocity_a", 0.2)
                Robot.set_value(motor, "velocity_b", 1)
        elif Gamepad.get_value(left):
            Robot.set_value(motor, "velocity_b", -1)
            Robot.set_value(motor, "velocity_a", 1)
        elif Gamepad.get_value(right):
            Robot.set_value(motor, "velocity_a", -1)
            Robot.set_value(motor, "velocity_b", 1)
        elif Gamepad.get_value(backward):
            Robot.set_value(motor, "velocity_a", -1)
            Robot.set_value(motor, "velocity_b", -1)
        else:
            Robot.set_value(motor, "velocity_a", 0)
            Robot.set_value(motor, "velocity_b", 0)
        Robot.sleep(0.2)
