import pigpio
import time


pin = 2
pi = pigpio.pi()
pi.set_mode(pin, pigpio.OUTPUT)


print ("mode: ", pi.get_mode(pin))

def unlock(pin, stall): #spins a servo to unlock it 
    min_servo = 500 #servo position as vars so it's easy to tune
    time.sleep(1)
    pi.set_servo_pulsewidth(pin, min_servo)
    time.sleep(1)
    pi.set_servo_pulsewidth(pin, 0)#stops the servo 
    time.sleep(1)
    stall['status'] = False

def lock(pin, stall ):
    max_servo= 2500
    time.sleep(1)
    pi.set_servo_pulsewidth(pin, max_servo)
    time.sleep(1)
    pi.set_servo_pulsewidth(pin, 0) #stops the servo 
    time.sleep(1)
    stall['status'] = True

def rack_read(stall_list):
    for i in stall_list: 
        if stall_list.get('status') == True: 
            bar_signal = pi.read(i.get('bar_in'))
            cable_signal = pi.read(i.get('cable_in'))

    if bar_signal == 1: 
        print('Current lost from locking bar' + i.get('name'))
        return bar_signal
    elif cable_signal == 1: 
        print('Current lost from cable at stall' + i.get('name'))
        return cable_signal
    
    else: 
        return True

for i in range(100):
    unlock(pin, {})
    #time.sleep(1)
    lock(pin, {})
    


