import pigpio
import time


pin = 2
pi = pigpio.pi()
pi.set_mode(pin, pigpio.OUTPUT)


print ("mode: ", pi.get_mode(pin))

for i in range(0,1000):
    print("setting to: ",pi.set_servo_pulsewidth(pin, 500))
    print("set to: ",pi.get_servo_pulsewidth(pin))

    time.sleep(1)

    print("setting to: ",pi.set_servo_pulsewidth(pin, 2500))
    print("set to: ",pi.get_servo_pulsewidth(pin))

    time.sleep(1)
    
    print("setting to: ",pi.set_servo_pulsewidth(pin, 0))
    print("set to: ",pi.get_servo_pulsewidth(pin))
    
    time.sleep(1)
    

pi.stop()
