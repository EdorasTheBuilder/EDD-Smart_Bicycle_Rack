from multiprocessing import Process, Queue
import time 

check = False

def f(queue, check):
    while True:
        if check == True:
            queue.put([42, None, 'hello'])
        else: 
            queue.put([False])
    
if __name__ == '__main__':
    queue = Queue()
    p = Process(target=f, args=(queue, check))
    p.start()
    print(queue.get())    # prints "[42, None, 'hello']"
    time.sleep(1)
    #p.terminate() 

