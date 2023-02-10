#setup-----------------------------------

#imports
import pigpio
import time


#-----Vars-----
stall_list = [
    {'name':1 ,'status': False, 'bar_out': 2, 'bar_in': 6, 'cable_out': 27, 'cable_in': 22, }
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
def user_info(email, user_pass, email_status = True, user_pass_status=True ): #gets the user's input 
    if email_status == True:
        email = input('Please enter your email:\n')
    if user_pass_status == True:
        user_pass = input('Please create a 6 digit numerical pin. \nYou will use this pin to unlock your bike later \n' ) 
    return email,user_pass
    
def user_check(email, user_pass):# checks that the users input is valid 
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

def settle(pin):
    pi.set_servo_pulsewidth(pin, 0)
    time.sleep(.5) 

def unlock(pin): #spins a servo to unlock it 
    min_servo = 500 #servo speeds as vars so it's easy to tune

    pi.set_servo_pulsewidth(pin, min_servo)
    time.sleep(1)
    settle(pin)


def lock(pin):
    max_servo= 2500
    pi.set_servo_pulsewidth(pin, max_servo)
    time.sleep(1)
    settle(pin)
    


    
#main code-----------------------------
#take a user input 
email, user_pass = user_info(email, user_pass)  
email_check, pin_check = user_check(email, user_pass)

while email_check == False or pin_check == False: #checks the users input 
    if email_check == False:
        email, user_pass = user_info(email, user_pass, user_pass_status=False)
        email_check, pin_check = user_check(email,user_pass)
    
    if pin_check == False: 
        email, user_pass = user_info(email, user_pass, email_status=False)
        email_check, pin_check = user_check(email, user_pass)


users[email] = user_pass # assigns valid user and password to dictionary 
print('User created: ' + email)


#assign a stall 
for i in stall_list:
    if i.get('status') == False:
        print('Please proceede to stall #' + str(i.get('name')))
        unlock(i.get('bar_out'))
        unlock(i.get('cable_out'))
        time.sleep(1)
        lock(i.get('bar_out'))
        lock(i.get('cable_out'))
        time.sleep(1)
        i['status'] = True













