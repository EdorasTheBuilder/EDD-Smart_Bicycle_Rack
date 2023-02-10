import gpiozero as gp 


from time import sleep 

pin_list = [4,27,22,23,24,25,5,6,26,12] #all of the gpio pins that will work 
pin_list.sort()

#turns the pins on 
for i in pin_list:
    temp = gp.LED(i)
    temp.on()

print('all pins should be powered') 
print(pin_list)

#sleeps 

count = 0
while count <= 60: 
    print(count)
    sleep(1)
    count += 1


#turns the pins off
for i in pin_list:
    temp = gp.LED(i)
    temp.off

print('all pins should be off')

