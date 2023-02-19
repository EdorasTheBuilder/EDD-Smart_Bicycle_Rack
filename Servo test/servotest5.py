import pigpio
import time

pi = pigpio.pi()
pi.set_mode(2, pigpio.OUTPUT)

print ("mode: ", pi.get_mode(4))

for i in range(0,1000):
    print("setting to: ",pi.set_servo_pulsewidth(2, 500))
    print("set to: ",pi.get_servo_pulsewidth(2))

    time.sleep(1)

    print("setting to: ",pi.set_servo_pulsewidth(2, 2500))
    print("set to: ",pi.get_servo_pulsewidth(2))

    time.sleep(1)
    
    print("setting to: ",pi.set_servo_pulsewidth(2, 0))
    print("set to: ",pi.get_servo_pulsewidth(2))
    
    time.sleep(1)
    

pi.stop()
