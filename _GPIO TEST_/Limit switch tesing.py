import pigpio
import time
from threading import Thread

#-----Vars-----
global stall_list
global email 
global user_pass
global users 

stall_list = [
    {'name':1 ,'user': '', 'status': False, 'bar_out': 2, 'bar_in': 20,  'cable_in': 21, 'limit':26}
]
#this is a dict of all of the possible stalls. the value for each key is the pinout for the rpi 
#status is weather or not the stall is locked 



#user input vars
email = ''
user_pin = ''
users = {}




#library setup
pi = pigpio.pi()

#setting modes of pins
for Stall in stall_list:
    pi.set_mode(Stall.get('cable_in'), pigpio.INPUT)
    pi.set_mode(Stall.get('bar_out'), pigpio.OUTPUT)
    pi.set_mode(Stall.get('bar_in'), pigpio.INPUT)
    pi.set_mode(Stall.get('limit'), pigpio.INPUT)

def unlock(pin, stall): #spins a servo to unlock it 
    min_servo = 500 #servo position as vars so it's easy to tune
    time.sleep(1)
    pi.set_servo_pulsewidth(pin, min_servo)
    time.sleep(1)
    pi.set_servo_pulsewidth(pin, 0)#stops the servo 
    time.sleep(1)
    stall['status'] = False

def lock(pin, stall ):
    switch = pi.read(Stall.get('limit'))
    complete = False
    print(switch)
    
    while complete == False:
        if switch == 1:
            max_servo= 2500
            pi.set_servo_pulsewidth(pin, max_servo)
            time.sleep(1)
            pi.set_servo_pulsewidth(pin, 0) #stops the servo 
            time.sleep(1)
            stall['status'] = True
            
            complete = True
        else: 
           switch = pi.read(Stall.get('limit'))
    
while True:
    unlock(2, stall_list[0])

    lock(2, stall_list[0])
    
