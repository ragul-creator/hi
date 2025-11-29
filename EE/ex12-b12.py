from machine import Pin, time_pulse_us
import time

trigPin=Pin(23,Pin.OUT)
echoPin=Pin(22,Pin.IN)
M1=Pin(2,Pin.OUT)#led or motor pin
while True:
    #ensure trigger is low
    trigPin.value(0)
    time.sleep_us(2)
    
    #send trigger pulse
    trigPin.value(1)
    time.sleep_us(10)
    trigPin.value(0)
    
    furation=time_pulse_us(echoPin,1,30000)
    
    distance=(duration*0.03430)/2
    
    if distance<=13:
        M1.value(1)
    else:
        M1.value(0)
    print('distance:',distance,'cm')
    