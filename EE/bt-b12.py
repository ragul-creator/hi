from machine imprt Pin,URAT
import time


bt=URAT(1,baudrate=9600,tx=17,rx=16)

led=Pin(2,Pin.OUT)

while True:
    if bt.any():
        incoming_value=bt.read(1)
        try:
            incoming_value.decode('utf-8')
        except:
            char_value=''
        print(char_value)
        
        if char_value=='1':
            led.value(1)
        elif char_value=='0':
            led.value(0)
            
    time.sleep(0.01)
            