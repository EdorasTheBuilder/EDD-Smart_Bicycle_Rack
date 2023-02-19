import pigpio
import time 


#library setup
pi = pigpio.pi()

#setting modes of pins
stall_list = {}


pi.set_mode(stall_list[0].get('cable_in'), pigpio.INPUT)
pi.set_mode(stall_list[0].get('cable_out'), pigpio.OUTPUT)
pi.set_mode(stall_list[0].get('bar_out'), pigpio.OUTPUT)
pi.set_mode(stall_list[0].get('bar_in'), pigpio.INPUT)

#functions for servo control {

def unlock(pin, stall): #spins a servo to unlock it 
    min_servo = 500 #servo position as vars so it's easy to tune

    pi.set_servo_pulsewidth(pin, min_servo)
    pi.set_servo_pulsewidth(pin, 0)#stops the servo 
    time.sleep(1)
    stall['status'] = False


def lock(pin, stall):
    max_servo= 2500
    pi.set_servo_pulsewidth(pin, max_servo)
    pi.set_servo_pulsewidth(pin, 0)#stops the servo 
    stall['status'] = True
    time.sleep(1)

#}