#setup
import pigpio 
import os 
import time 
os.system('sudo pigpio')# starts pigpio 

#vars
main_pin = 4




#running
pi = pigpio.pi()
pi.set_mode(main_pin, pigpio.OUTPUT)

print ("mode: ", pi.get_mode(main_pin))


print("setting to: ",pi.set_servo_pulsewidth(4, 1000))
print("set to: ",pi.get_servo_pulsewidth(main_pin))



print("setting to: ",pi.set_servo_pulsewidth(4, 2000))
print("set to: ",pi.get_servo_pulsewidth(main_pin))



