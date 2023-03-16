import time


stall_list = [
    {'name':1 ,'user': '', 'assigned': False, 'bar_out': 2, 'bar_in': 20,  'cable_in': 21, 'switch': 26}
] 
def unlock(pin, stall): #spins a servo to unlock it 
    min_servo = 500 #servo position as vars so it's easy to tune
    time.sleep(1)
    #pi.set_servo_pulsewidth(pin, min_servo)
    time.sleep(1)
    #pi.set_servo_pulsewidth(pin, 0)#stops the servo 
    time.sleep(1)
    stall['assigned'] = False

def lock(pin, stall ):
    #switch = pi.read(stall.get('limit')) # reads value of limit switch
    complete = False
    switch = 1
    
    while complete == False: #checks if locking is complete 
        if switch == 1:
            max_servo= 2500
            #pi.set_servo_pulsewidth(pin, max_servo)
            time.sleep(1)
            #pi.set_servo_pulsewidth(pin, 0) #stops the servo 
            time.sleep(1)
            stall['status'] = True
            
            complete = True
        else: 
           #switch = pi.read(stall.get('limit'))
           pass

for i in stall_list: 
    unlock(i.get())