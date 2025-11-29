from machine import Pin, PWM
import time

# === Settings & Pins ===
spd, fwd = 800, 0   # spd = motor speed (PWM duty), fwd = forward flag (0/1)

# Motors: left forward, left backward, right forward, right backward
lf, lb, rf, rb = [PWM(Pin(p), freq=1000) for p in (13, 27, 26, 25)]

# Servo + Ultrasonic pins
servo = PWM(Pin(15), freq=50)     # Servo on pin 15 (50Hz)
TRIG  = Pin(23, Pin.OUT)          # Ultrasonic trigger
ECHO  = Pin(22, Pin.IN)           # Ultrasonic echo

# === Controls ===
def set_motor(v):
    for m, x in zip((lf, lb, rf, rb), v):
        m.duty(x)

def drive(F=0, B=0, L=0, R=0):
    global fwd
    fwd = F
    set_motor(
        (spd,0,spd,0) if F else
        (0,spd,0,spd) if B else
        (spd,0,0,spd) if L else
        (0,spd,spd,0) if R else
        (0,0,0,0)
    )

def turn(L=1):
    drive(L=L, R=not L)
    time.sleep_ms(1000)
    drive()

def set_servo(a):
    servo.duty(int(a/180*75+40))

# === Sensors ===
def read_dist():
    """Read distance in cm from ultrasonic sensor."""
    TRIG.off(); time.sleep_us(2)
    TRIG.on();  time.sleep_us(10)
    TRIG.off()

    t0 = time.ticks_us()
    ps = pe = 0  # predefine variables

    # Wait for ECHO to go HIGH (start pulse)
    while not ECHO.value():
        if time.ticks_diff(time.ticks_us(), t0) > 30000:
            print("Timeout waiting for echo start")
            return 250  # max distance
    ps = time.ticks_us()

    # Wait for ECHO to go LOW (end pulse)
    while ECHO.value():
        pe = time.ticks_us()
        if time.ticks_diff(pe, ps) > 30000:
            print("Timeout waiting for echo end")
            return 250

    dist = int(time.ticks_diff(pe, ps) / 58)
    print("Distance:", dist, "cm")  # <<< print distance
    return dist

def look(a):
    set_servo(a)
    time.sleep_ms(500)
    d = read_dist()
    set_servo(90)
    time.sleep_ms(300)
    return d

# === Init ===
set_servo(90)
time.sleep(2)
[read_dist() for _ in range(2)]   # warm up

# === Main Loop ===
while True:
    time.sleep_ms(50)
    dist = read_dist()

    if dist <= 20:   # obstacle detected
        drive(); time.sleep_ms(600)
        drive(B=1); time.sleep_ms(800)
        drive(); time.sleep_ms(600)

        # Look left & right, decide turn
        turn(look(10) < look(170))
        fwd = 0
    else:
        drive(F=1)