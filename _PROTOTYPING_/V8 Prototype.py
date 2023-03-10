#setup-----------------------------------
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#imports
import pigpio
import time
import threading as Thread

#-----Vars-----
global stall_list
global email 
global user_pass
global users 

stall_list = [
    {'name':1 ,'user': '', 'assigned': False, 'bar_out': 2, 'bar_in': 20,  'cable_in': 21, }
]
#this is a dict of all of the possible stalls. the value for each key is the pinout for the rpi 
#assigned is weather or not the stall is locked 



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


#------- functions --------------------------
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$



#functions for servo control {

def unlock(pin, stall): #spins a servo to unlock it 
    min_servo = 500 #servo position as vars so it's easy to tune
    time.sleep(1)
    pi.set_servo_pulsewidth(pin, min_servo)
    time.sleep(1)
    pi.set_servo_pulsewidth(pin, 0)#stops the servo 
    time.sleep(1)
    stall['assigned'] = False

def lock(pin, stall):

    max_servo= 2500
    time.sleep(1)
    pi.set_servo_pulsewidth(pin, max_servo)
    time.sleep(1) #waits program to so servo has time to move 
    pi.set_servo_pulsewidth(pin, 0) #stops the servo 
    time.sleep(1)
    stall['assigned'] = True



#functions for reading servo values 

def rack_read(stall):
    
    # reads the signal from the bar 
    bar_signal = pi.read(stall.get('bar_in'))
    cable_signal = pi.read(stall.get('cable_in'))
    
    read_lst = {'bar' : 1, 'cable' :1}
    secure = True
    
    #evaluates the signal from the gbar
    if bar_signal == 0: 
        print('Current lost from locking bar' + str(stall.get('name')))
        read_lst['bar'] = 0
        secure = False
    elif cable_signal == 0: 
        print('Current lost from cable at stall' + str(stall.get('name')))
        read_lst['cable'] = 0
        secure = False
    else:  
        return secure


    #determines weather or not to return read_lst
    return secure
    




#user info setup 


def user_info(email, user_pin, email_status = True, user_pass_status=True ): #gets the user's input 
    #set email status or user pass status to false to bypass that check
    
    if email_status == True:
        email = input('Please enter your email:\n')
    if user_pass_status == True:
        user_pin = input('Please create a 6 digit numerical pin. \nYou will use this pin to unlock your bike later \n' ) 
    return email,user_pin
    
def user_setup_check(email, user_pin):# checks that the users input is valid 
    email_check = False
    pin_check = False
    
    #checks to see if there's a domain 
    domain = False
    domain_location = email.find('.') + 1
    if len(email) - domain_location >=3:
        domain = True
    
    #checks for prefix

    prefix = False
    prefix_location = email.find('@')
    if prefix_location != 0: 
        prefix = True

    #checks for any spaces 
    no_spaces = False
    if ' ' not in email: 
        no_spaces = True


    #checks the users email
    if '@' in email and prefix == True and domain == True and no_spaces == True: 
        print('Email checks out')
        email_check = True
    else: 
        print('Email needs to be an email. Ex: hello@gmail.com')
        
    
    #checks the users pin 
    count = 0 
    for i in user_pin: 
            count += 1

    if user_pin.isnumeric() == True:
        
        if count == 6:
            print('Pin checkes out')
            pin_check = True
            
        elif count > 6:
            print('Your pin has more than 6 digits!')
            

        elif count < 6:
            print('Your pin has less than 6 digits!')
            

    else: 
        print("Your pin must be all numbers")
    
    return email_check, pin_check


##unlock username and pass check 
def user_verify(user_list, email, user_pin, stall_list):
    if user_list.get(email) != None: #checks the user's email 
        print('Email exists')
        
        if user_list.get(email) == user_pin: #checks the user's password 
            print('Correct Password entered')
    
            for stall in stall_list: 
                if stall['user'] == email:
                    print('Stall and user found')
                    return True
                else: 
                    print('user not bound to a stall')
        else: 
            print('wrong password entered')


    else: 
        print('No email found')


    


#figures out if the user wants to lock or unlock a bike.
def start(users, stall_list, email, user_pin):
    use = input('Welcome! \n Are you locking or unlocking your bicycle? \n Please type your answer and press enter.\n')


    if use == 'Locking':
        
        email, user_pin = user_info(email, user_pin)  

        email_check, pin_check = user_setup_check(email, user_pin)

        while email_check == False or pin_check == False: #checks the users input 
            if email_check == False:
                email, user_pin = user_info(email, user_pin, user_pass_status=False)
                email_check, pin_check = user_setup_check(email,user_pin)
            
            if pin_check == False: 
                email, user_pin = user_info(email, user_pin, email_status=False)
                email_check, pin_check = user_setup_check(email, user_pin)


        users[email] = user_pin # assigns valid user and password to dictionary 
        print('User created: ' + email)


        #assign a stall 
        for Stall in stall_list:
            if Stall.get('assigned') == False:
                
                
                unlock(Stall.get('bar_out'), Stall)
                
                print('Please proceede to stall #' + str(Stall.get('name')))
                
                
                lock(Stall.get('bar_out'), Stall)
                
                
       
        
                Stall['user'] = email



                
    if use == 'Unlocking':
        email = input('Please enter your email')
        user_pin = input('Please enter your PIN')
        verify = user_verify(users, email, user_pin, stall_list)
        
        if verify == True:
            
            for stall in stall_list:
                
                if stall.get('user') == email:
                    unlock(stall.get('bar_out'), stall)
                
                    
                    time.sleep(2)
                    
                    lock(stall.get('bar_out'), stall)
                 








    
#main code-------------------------------------------------------------------------------------------------------------------------------------------------
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    

#take a user input

start(users, stall_list, email, user_pin) 


thread_running = True

def main_thread():
    global thread_running
    start_time = time.time()

    # run this while there is no input
    while thread_running:
        time.sleep(0.1)
        
        if time.time() - start_time >= 1:
            start_time = time.time()
            
            for stall in stall_list:
                if stall.get('assigned')== True: 
                    rack_read(stall)


def take_input():
    start(users, stall_list, email, user_pin) 
    # doing something with the input
    #print('The user input is: ', user_input)


if __name__ == '__main__':
    t1 = Thread(target=main_thread)
    t2 = Thread(target=take_input)

    t1.start()
    t2.start()

    t2.join()  # interpreter will wait until your process get completed or terminated
    thread_running = False
    print('error')