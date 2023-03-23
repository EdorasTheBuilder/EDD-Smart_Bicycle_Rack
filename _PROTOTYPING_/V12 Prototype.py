#setup-----------------------------------
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#imports
import pigpio
import time
from threading import Thread
import os

#-----Vars-----
global stall_list
global email 
global user_pass
global users 

stall_list = [
    {'name':1 ,'user': '', 'assigned': False, 'bar_out': 2, 'bar_in': 20,  'cable_in': 21, 'switch': 26}
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
for stall in stall_list: 
    pass
    pi.set_mode(stall.get('cable_in'), pigpio.INPUT)
    pi.set_mode(stall.get('bar_out'), pigpio.OUTPUT)
    pi.set_mode(stall.get('bar_in'), pigpio.INPUT)
    pi.set_mode(stall.get('switch'), pigpio.INPUT)


#------- functions --------------------------
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$



#random functions
 
def find_index(stall):  #finds the index of the stall dictionary in the stall list, used later to figure out weather or not stall is assigned to a user
    count = 0 
    for i in stall_list:
        if i == stall: 
            return count
        else:
            count += 1 
   
#functions for servo control

def unlock(stall): #spins a servo to unlock it 
    pin = stall.get('bar_out')

    min_servo = 2500 #servo position as vars so it's easy to tune

    
    time.sleep(1)
    pi.set_servo_pulsewidth(pin, min_servo)
    time.sleep(1)
    pi.set_servo_pulsewidth(pin, 0)#stops the servo 
    time.sleep(1)

    
    
    stall_list[find_index(stall)]['assigned'] = False #changes the value in the dictionary, stall is not assigned to a user
   

def lock(stall): #spins the servo to lock it 
    pin = stall.get('bar_out')
    switch = pi.read(stall.get('switch')) # reads value of limit switch
    complete = False

    
    
    while complete == False: #checks if locking is complete 
        if switch == 1: #checks if the limit switch is pressed
            max_servo= 500
            pi.set_servo_pulsewidth(pin, max_servo)
            time.sleep(1)
            pi.set_servo_pulsewidth(pin, 0) #stops the servo 
            time.sleep(1)
            
            
            complete = True
        else: 
           switch = pi.read(stall.get('switch'))
    
    stall_list[find_index(stall)]['assigned'] = True #changes the value in the dictionary, stall is  assigned to a user


#functions for reading values of a GPIO pin on a raspberry pi 

def rack_read(stall):
    
    # reads the signal from the bar 
    bar_signal = pi.read(stall.get('bar_in'))
    cable_signal = pi.read(stall.get('cable_in')) 
    secure = True
    
    #evaluates the signal from the gbar
    if bar_signal == 0 and cable_signal == 0:
        print('Current lost from locking bar and cable at stall ' + str(stall.get('name')))
        secure = False
    elif bar_signal == 0: 
        print('Current lost from locking bar at stall' + str(stall.get('name')))
        secure = False
    elif cable_signal == 0: 
        print('Current lost from cable at stall ' + str(stall.get('name')))
        secure = False
    

    else:  
        return secure

    




#user info setup 


def user_info(email, user_pin, email_status = True, user_pass_status=True, mode = True): #gets the user's input 
    #set email status or user pass status to false to bypass that check
    #mode is weather or not you are locking or unlocking, true for locking and false for unlocking

   
    if email_status == True:
        email = input('Please enter your email:\n')

    if user_pass_status == True:

        if mode == True:
            print('Please create a 6 digit numerical pin. \nYou will use this pin to unlock your bike later \n' )   

        user_pin = input('Please enter your pin \n')


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
    if prefix_location != 0 and prefix_location != (len(email) - 1):
        prefix = True

    #checks for any spaces 
    no_spaces = False
    if ' ' not in email: 
        no_spaces = True


    #checks the users email
    if '@' in email and prefix == True and domain == True and no_spaces == True: 
        print('Valid Email')
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
    use = input("""Welcome! 
                    This is a smart bicycle rack that eliminates your need to carry a lock! \n
                    It has several anti-theft features! \n 
                    T


    
                
                \n Are you locking or unlocking your bicycle? \n Please type "L" for locking or "U" for unlocking. \n""")

    #locking 
    if use == "L" or use == 'l':
        
        count = 0 #used to figure out weather or not there is a free stall 
        
        for stall in stall_list:
            if stall.get('assigned') == True: 
                count += 1
        
        if count == len(stall_list):
                print('Sorry... There are no free stalls at this time :(')
                return 
                

        
        email, user_pin = user_info(email, user_pin)  

        email_check, pin_check = user_setup_check(email, user_pin)

        while email_check == False or pin_check == False: #checks the users input 
           
            if email_check == False: #adjusts what it asks the user based on if passed the check 
                email, user_pin = user_info(email, user_pin, user_pass_status=False) 
                email_check, pin_check = user_setup_check(email,user_pin)
            
            if pin_check == False: 
                email, user_pin = user_info(email, user_pin, email_status=False)
                email_check, pin_check = user_setup_check(email, user_pin)
        

        users[email] = user_pin # assigns valid user and password to dictionary 
        print('User created: ' + email)


        #assign a stall 
        
        
        for stall in stall_list:
            if stall.get('assigned') == False:
                
                unlock(stall)
                
                print(""" To lock your bicycle: 
                1. Slide the metal bar through your frame. \n 
                2. Wrap the cable through your wheel. \n
                3. Push the bar through the loop at the end of the cable \n 
                4. Push the bar to the end. \n   
                5. You are done! Enjoy knowing your bicycle is secure. \n
                
                """)

                print('Please proceede to stall #' + str(stall.get('name')))

                
                lock(stall)
                
                stall['user'] = email
                
        
        


    ######### unlocking            
    elif use == 'U' or use == 'u':
        print(""" Welcome back! \n
        To unlock your bicycle, please slide the bar back and remove your bicycle. 
        Please be polite and slide the bar back in once your bicycle is free!
        


        """)

        user_info(email, user_pin, mode=False)
   
        verify = user_verify(users, email, user_pin, stall_list)
        
        if verify == True:
            
            for stall in stall_list:
                
                if stall.get('user') == email:
                    unlock(stall)
                
                    
                    time.sleep(2)
                    
                    
    else:
        print("Error! Are you sure you typed your answer correctly?")
                 








    
#main code-------------------------------------------------------------------------------------------------------------------------------------------------
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    

#take a user input

#start(users, stall_list, email, user_pin) 


thread_running = True

def main_thread():
    global thread_running
    start_time = time.time()

    # run this while there is no input
    while thread_running:
        time.sleep(0.5)
        
        if time.time() - start_time >= 5:
            start_time = time.time()
            
            for stall in stall_list:
                if stall.get('assigned')== True: 
                    rack_read(stall)
                 

def take_input():
    while thread_running == True: 
        start(users, stall_list, email, user_pin)
        time.sleep(1)
        os.system('clear') #hopefully it clears the OS
        # doing something with the input
        


if __name__ == '__main__':
    t1 = Thread(target=take_input)
    t2 = Thread(target=main_thread)

    t1.start()
    t2.start()
