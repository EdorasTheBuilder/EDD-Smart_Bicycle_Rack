import pigpio

pi = pigpio.pi()

bar_in = 5 #signal in from bar
bar_out = 6 #signal out from bar

pi.set_mode(bar_in, pigpio.INPUT)
pi.set_  mode(bar_out, pigpio.OUTPUT)


while True: 
    print(pi.read(bar_in))



