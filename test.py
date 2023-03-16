import time


global stall_list

stall_list = [
    {'name':1 ,'user': '', 'assigned': False, 'bar_out': 2, 'bar_in': 20,  'cable_in': 21, 'switch': 26}
] 



def find_index(stall):
    count = 0 
    for i in stall_list:
        if i == stall: 
            return count
        else:
            count += 1 
    



def unlock(stall): #spins a servo to unlock it 
    pin = stall.get('bar_out')

    min_servo = 500 #servo position as vars so it's easy to tune

    
    time.sleep(1)
    pi.set_servo_pulsewidth(pin, min_servo)
    time.sleep(1)
    pi.set_servo_pulsewidth(pin, 0)#stops the servo 
    time.sleep(1)

    
    
    stall_list[find_index(stall)]['assigned'] = False #changes the value in the dictionary, stall is not assigned to a user
   

def lock(stall):
    pin = stall.get('bar_out')
    switch = pi.read(stall.get('limit')) # reads value of limit switch
    complete = False
    switch = 1

    
    
    while complete == False: #checks if locking is complete 
        if switch == 1:
            max_servo= 2500
            pi.set_servo_pulsewidth(pin, max_servo)
            time.sleep(1)
            pi.set_servo_pulsewidth(pin, 0) #stops the servo 
            time.sleep(1)
            
            
            complete = True
        else: 
           switch = pi.read(stall.get('limit'))
    
    stall_list[find_index(stall)]['assigned'] = True #changes the value in the dictionary, stall is  assigned to a user

