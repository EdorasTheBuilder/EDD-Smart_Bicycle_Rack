#imports 
import PySimpleGUI as sg
import pigpio 
import time 
import subprocess



#vars
locking_visibility = False
users = ['test']
keys = ['test']
min_servo = 500 
max_servo= 2500
event = False #prevents an error. 
main_pin = 4   #pin for main servo output 


#functions
def arg_check(Type, *arg):
    for i in arg:
        if type(i) == Type:
            return True
        else: 
            return False

def close_all(window): 
    try: 
        for i in window: 
            i.close()
    except Exception as close_error: 
        print(close_error)



#setup for the layouts 
layout_main = [
        [sg.Text('Welcome! Are you unlocking or locking a bike?')],
        [sg.Button('Locking'), sg.Button('Unlocking')],
            ]

layout_locking = [
        [sg.Text('Please enter information below')], 
        [sg.Input('Email')], 
        [sg.Input('creat a PIN')],
        [sg.Button('Submit')], 

]

layout_unlocking = [
    [sg.Text('Please enter username and pin to unlock stall')],
    [sg.Input('Name')], 
    [sg.Input('PIN')],
    [sg.Button('Submit')]
]


#create window 
main_window = sg.Window('Bike Rack login page', layout_main).finalize()
#main_window.maximize()

#setup for servos 
'''
subprocess.Popen('sudo pigpiod')
pi = pigpio.pi()
pi.set_mode(main_pin, pigpio.OUTPUT)
print ("mode: ", pi.get_mode(main_pin))
pi.set_servo_pulsewidth(main_pin, min_servo)'''


#event loop to process events 

while True: 
    if event != sg.WINDOW_CLOSED:
        event, values = main_window.read()

        

    if event == 'Locking':
        main_window.close()
        locking_window= sg.Window('name', layout_locking).finalize()
        #locking_window.maximize()
        event, values = locking_window.read()    
        if event == 'Submit':
            users.append(values[0])
            keys.append(values[1])
            locking_window.close()
        
         
    
    elif event == 'Unlocking':
        main_window.close()
        unlocking_window = sg.Window('name', layout_unlocking).finalize()
        event, values = unlocking_window.read()
        if event == 'Submit':       
        
        #checks the username and password 
            count = 0 
            for i in users:
                if i == values[0]: 
                    if keys[count] == values[1]:
                        print('found user and correct password')
                    else: 
                        print('wrong pin')


                else: 
                    print('No user found!')
        unlocking_window.close()
    
    
   
        
        


    if event == sg.WINDOW_CLOSED:
        print('somehow the window closed')
        break

        
  

    
