import pigpio
import time

pi = pigpio.pi()
pi.set_mode(2, pigpio.OUTPUT)

print ("mode: ", pi.get_mode(4))

for i in range(0,1000):
    print("setting to: ",pi.set_servo_pulsewidth(2, 1000))
    print("set to: ",pi.get_servo_pulsewidth(2))

    time.sleep(1)

    print("setting to: ",pi.set_servo_pulsewidth(2, 2000))
    print("set to: ",pi.get_servo_pulsewidth(2))

    time.sleep(1)

pi.stop()