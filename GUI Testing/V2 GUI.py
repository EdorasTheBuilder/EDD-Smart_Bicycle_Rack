#imports 
import PySimpleGUI as sg


#globals 
title_key_list = {'welcome title' : 0, 'locking':1, 'unlocking':2, }
locking_vis = False
title_vis = True

#setup 
layout = [
    [sg.Text('Welcome! Are you unlocking or locking a bike?', key=title_key_list['welcome title']), 
sg.Button('Locking', key=title_key_list['locking'], visible=title_vis), 
sg.Button('Unlocking', key=title_key_list['unlocking'], visible=title_vis)
], 
[sg.Text('Locking hello', visible=locking_vis)]
]


#create window 
window = sg.Window('Bike Rack login page', layout).finalize()


#event loop to process events 
while True: 
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break 
    if event == 'Locking':
        title_vis = False
        locking_vis = True
        window.update()
    
