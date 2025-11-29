from machine import Pin,PWM
from time  import sleep_ms

#ir sensor digital pins
irLeft=Pin(23,Pin.IN)
irRight=Pin(22,Pin.IN)

#motor control pins
in1=Pin(14,Pin.OUT)
in2=Pin(27,Pin.OUT)
in3=Pin(26,Pin.OUT)
in4=Pin(25,Pin.OUT)

#speed control pwn pins
ena_pwm=PWM(Pin(2),freq=1000)

PWM_MIN=1023

SLOW_ON_TIME=100
SLOW_OFF_TIME=100

def analogWrite(pwm,duty):
    pwn.duty(duty)

def slowForward():
    print("moving: forward")
    in1.value(1)
    in2.value(0)
    in3.value(1)
    in4.value(0)
    analogWrite(ena_pwm,PWM_MIN)
    analogWrite(enb_pwm,PWM_MIN)
    sleep_ms(SLOW_ON_TIME)
    analogWrite(ena_pwm,0)
    analogWrite(enb_pwm,0)
    sleep_ms(SLOW_OFF_TIME)
    
def pivotTurnLeft():
    print("turning: left")
    in1.value(0)
    in2.value(1)
    in3.value(1)
    in4.value(0)
    analogWrite(ena_pwm,PWM_MIN)
    analogWrite(enb_pwm,PWM_MIN)
    sleep_ms(SLOW_ON_TIME)
    analogWrite(ena_pwm,0)
    analogWrite(enb_pwm,0)
    sleep_ms(SLOW_OFF_TIME)
    
def pivotTurnRight():
    print("turning: Right")
    in1.value(1)
    in2.value(0)
    in3.value(0)
    in4.value(1)
    analogWrite(ena_pwm,PWM_MIN)
    analogWrite(enb_pwm,PWM_MIN)
    sleep_ms(SLOW_ON_TIME)
    analogWrite(ena_pwm,0)
    analogWrite(enb_pwm,0)
    sleep_ms(SLOW_OFF_TIME)

def stopMotors():
    print("Motors: Stopped")
    in1.value(0)
    in2.value(0)
    in3.value(0)
    in4.value(0)
    analogWrite(ena_pwm,0)
    analogWrite(enb_pwm,0)

while True:
    leftIR= irLeft.value()
    rightIR=irRight.value()
    
    print("IR left:","detected" if leftIR==0 else "NOT detected","| IR Right:","detected" if rightIR==0 else "not detected")
    
    if leftIR==0 and rightIR==0:
        slowForward()
    elif leftIR==1 and rightIR==0:
        pivotTurnRight()
    elif leftIR==0 and rightIR==1:
        pivotTurnLeft()
    else:
        stopMotors()
    
    sleep_ms(100)
    
    
