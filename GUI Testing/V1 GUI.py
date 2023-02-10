#imports 
import PySimpleGUI as sg
import gpiozero as gp

#vars
locking_visibility = False
users = []
keys = []



#functions
def arg_check(Type, *arg):
    for i in arg:
        if type(i) == Type:
            return True
        else: 
            return False







#setup for the layouts 
layout_main = [
        [sg.Text('Welcome! Are you unlocking or locking a bike?')],
        [sg.Button('Locking'), sg.Button('Unlocking')],
            ]

layout_locking = [
        [sg.Text('Please enter information below')], 
        [sg.Input('Name')], 
        [sg.Input('PIN')],
        [sg.Button('Submit')], 

]

layout_unlocking = [
    [sg.Text('Please enter username and pin to unlock stall')],
    [sg.Input('Name')], 
    [sg.Input('PIN')]
]


#create window 
main_window = sg.Window('Bike Rack login page', layout_main).finalize()
main_window.maximize()
#event loop to process events 
while True: 
    event, values = main_window.read()


    if event == 'Locking':
        main_window.close()
        locking_window= sg.Window('name', layout_locking).finalize()
        locking_window.maximize()
        event, values = locking_window.read()
        users.append(values[0])
        keys.append(values[1])
    
        


    elif event == 'Unlocking':
        main_window.close()
        unlocking_window = sg.window('name', layout_unlocking).finalize()
        event, values = locking_window.read()
        
        
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


        







    if event == sg.WINDOW_CLOSED:
        break

    
