#setup-----------------------------------
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#imports
import pigpio
import time
from threading import Thread

#-----Vars-----
stall_list = [
    {'name':1 ,'user': '', 'status': False, 'bar_out': 2, 'bar_in': 6, 'cable_out': 4, 'cable_in': 22, }
]
#this is a dict of all of the possible stalls. the value for each key is the pinout for the rpi 




#user input vars
email = ''
user_pass = ''
users = {}


#library setup
pi = pigpio.pi()

#setting modes of pins

pi.set_mode(stall_list[0].get('cable_in'), pigpio.INPUT)
pi.set_mode(stall_list[0].get('cable_out'), pigpio.OUTPUT)
pi.set_mode(stall_list[0].get('bar_out'), pigpio.OUTPUT)
pi.set_mode(stall_list[0].get('bar_in'), pigpio.INPUT)


#------- functions --------------------------
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#user info setup 
def user_info(email, user_pass, email_status = True, user_pass_status=True ): #gets the user's input 
    if email_status == True:
        email = input('Please enter your email:\n')
    if user_pass_status == True:
        user_pass = input('Please create a 6 digit numerical pin. \nYou will use this pin to unlock your bike later \n' ) 
    return email,user_pass
    
def user_setup_check(email, user_pass):# checks that the users input is valid 
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
    
    #checks the users email
    if '@' in email and prefix == True and domain == True: 
        print('Email checks out')
        email_check = True
    else: 
        print('Email needs to be an email. Ex: hello@gmail.com')
        
    
    #checks the users pin 
    count = 0 
    for i in user_pass: 
            count += 1

    if user_pass.isnumeric() == True:
        
        if count == 6:
            print('Pin checkes out')
            pin_check = True
            
        elif count > 6:
            print('Your pin has more than 6 digits!')
            

        elif count < 6:
            print('Your pin has less than 6 digits!')
            

    else: 
        print("Your pin doesn't have any numbers")
    
    return email_check, pin_check


##unlock username and pass check 
def user_verify(user_list, email, user_pass, stall_list):
    if user_list.get(email) != None: #checks the user's email 
        print('Email exists')
        
        if user_list.get(email) == user_pass: #checks the user's password 
            print('Correct Password entered')
    
            for stall in stall_list: 
                if stall['user'] == email:
                    print('Stall and user found')
                else: 
                    print('user not bound to a stall')
        else: 
            print('wrong password entered')


    else: 
        print('No email found')





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
    time.sleep(1)
    stall['status'] = True

def stop(pin):
    pi.set_servo_pulsewidth(pin, 0)
    time.sleep(1)

#}

    
#main code-------------------------------------------------------------------------------------------------------------------------------------------------
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#take a user input

email, user_pass = user_info(email, user_pass)  
email_check, pin_check = user_setup_check(email, user_pass)

while email_check == False or pin_check == False: #checks the users input 
    if email_check == False:
        email, user_pass = user_info(email, user_pass, user_pass_status=False)
        email_check, pin_check = user_setup_check(email,user_pass)
    
    if pin_check == False: 
        email, user_pass = user_info(email, user_pass, email_status=False)
        email_check, pin_check = user_setup_check(email, user_pass)


users[email] = user_pass # assigns valid user and password to dictionary 
print('User created: ' + email)


#assign a stall 
for Stall in stall_list:
    if Stall.get('status') == False:
        
        
        unlock(Stall.get('bar_out'), Stall)
        unlock(Stall.get('cable_out'), Stall)
        print('Please proceede to stall #' + str(Stall.get('name')))
        
        lock(Stall.get('bar_out'), Stall)
        lock(Stall.get('cable_out'), Stall)
        
       
        stop(Stall.get('bar_out'))
        stop(Stall.get('cable_out'))
             
        Stall['status'] = True
        Stall['user'] = email
        

#reading the values



