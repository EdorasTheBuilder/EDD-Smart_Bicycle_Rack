import pigpio
import time
from threading import Thread

#-----Vars-----
global stall_list
global email 
global user_pass
global users 

stall_list = [
    {'name':1 ,'user': '', 'status': False, 'bar_out': 2, 'bar_in': 14, 'cable_out':19, 'cable_in': 26m  , }
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
    pi.set_mode(Stall.get('cable_out'), pigpio.OUTPUT)
    pi.set_mode(Stall.get('bar_out'), pigpio.OUTPUT)
    pi.set_mode(Stall.get('bar_in'), pigpio.INPUT)
    

while True:
    for Stall in stall_list:
        print(pi.read(Stall.get('bar_in')))
        print(pi.read(Stall.get('cable_in')))

