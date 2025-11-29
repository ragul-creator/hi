from machine import Pin
ir_sensor1=Pin(23,Pin.IN)
in1=Pin(2,Pin.OUT)
while True:
    ir-value=ir_sensor1.value()
    if ir_value==0:
        in1.on()
        print("Obstacle detected!MOTOR ON")
    else:
        in1.off()
        print("No obstacle,MOTOR OFF")
