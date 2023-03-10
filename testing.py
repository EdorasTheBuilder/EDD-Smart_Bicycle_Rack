import os 
def clear():
    sucess = False
    

    try:
        os.system('clear')
        sucess = True
    except:
        pass

    if sucess == False:
        try:
            os.system('cls')
        except:
            pass    
    
    
print('hello')
clear()
