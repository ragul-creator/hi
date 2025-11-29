from machine import Pin, PWM
from time import sleep_ms

# IR sensor digital pins
irLeft = Pin(23, Pin.IN)
irRight = Pin(22, Pin.IN)

# Motor control pins
in1 = Pin(14, Pin.OUT)
in2 = Pin(27, Pin.OUT)
in3 = Pin(26, Pin.OUT)
in4 = Pin(25, Pin.OUT)

# Speed control (PWM) pins
ena_pwm = PWM(Pin(2), freq=1000)
enb_pwm = PWM(Pin(15), freq=1000)

# Set minimum working speed
PWM_MIN = 1023  # Range: 0–1023 for ESP32 (MicroPython)

# Pulse timing for slow simulation
SLOW_ON_TIME = 100   # milliseconds
SLOW_OFF_TIME = 100  # milliseconds

def analogWrite(pwm, duty):
    pwm.duty(duty)

def slowForward():
    print("Moving: Forward")
    in1.value(1)
    in2.value(0)
    in3.value(1)
    in4.value(0)
    analogWrite(ena_pwm, PWM_MIN)
    analogWrite(enb_pwm, PWM_MIN)
    sleep_ms(SLOW_ON_TIME)
    analogWrite(ena_pwm, 0)
    analogWrite(enb_pwm, 0)
    sleep_ms(SLOW_OFF_TIME)

def pivotTurnLeft():
    print("Turning: Left")
    in1.value(0)
    in2.value(1)
    in3.value(1)
    in4.value(0)
    analogWrite(ena_pwm, PWM_MIN)
    analogWrite(enb_pwm, PWM_MIN)
    sleep_ms(SLOW_ON_TIME)
    analogWrite(ena_pwm, 0)
    analogWrite(enb_pwm, 0)
    sleep_ms(SLOW_OFF_TIME)

def pivotTurnRight():
    print("Turning: Right")
    in1.value(1)
    in2.value(0)
    in3.value(0)
    in4.value(1)
    analogWrite(ena_pwm, PWM_MIN)
    analogWrite(enb_pwm, PWM_MIN)
    sleep_ms(SLOW_ON_TIME)
    analogWrite(ena_pwm, 0)
    analogWrite(enb_pwm, 0)
    sleep_ms(SLOW_OFF_TIME)

def stopMotors():
    print("Motors: Stopped")
    in1.value(0)
    in2.value(0)
    in3.value(0)
    in4.value(0)
    analogWrite(ena_pwm, 0)
    analogWrite(enb_pwm, 0)

# Main loop
while True:
    leftIR = irLeft.value()
    rightIR = irRight.value()

    # Sensor status print
    print("IR Left:", "Detected" if leftIR == 0 else "Not Detected", "| IR Right:", "Detected" if rightIR == 0 else "Not Detected")

    # Movement logic
    if leftIR == 0 and rightIR == 0:
        slowForward()
    elif leftIR == 1 and rightIR == 0:
        pivotTurnRight()
    elif leftIR == 0 and rightIR == 1:
        pivotTurnLeft()
    else:
        stopMotors()

    sleep_ms(100)  # Small delay for serial stability