import easygui as eg
import multiprocessing as mp 
import time

value = False

def user_input():
    us = eg.ynbox('How do you feel ')
    return us

def check(value):
    while True:
        if check == True:
            return True
        else: 
            return False
        

if __name__ == '__main__':
    queue = mp.Queue()
    process_1 = mp.Process(target=user_input, )
    process_1 = mp.Process(target=check, args=(value, ))