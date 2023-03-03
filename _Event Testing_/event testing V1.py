#https://realpython.com/intro-to-python-threading/

from threading import Thread
import time
import random


global thread_running
thread_running = True



def my_forever_while():
    
    start_time = time.time()

    # run this while there is no input
    while thread_running:
        time.sleep(0.1)
        
        if time.time() - start_time >= 5:
            start_time = time.time() 
            print(random.randint(0,1))
            print('Another 5 seconds has passed')  
             


def take_input():
    h = input('hello')
    # doing something with the input
    print(h)
    thread_running = False

if __name__ == '__main__':
    t1 = Thread(target=my_forever_while)
    t2 = Thread(target=take_input)

    
    t1.start()
    t2.start()

    