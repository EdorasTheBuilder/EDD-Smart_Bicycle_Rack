import pigpio

pi = pigpio.pi()

bar_in = 6 #signal in from bar

pi.set_mode(bar_in, pigpio.INPUT)



while True: 
    print(pi.read(bar_in))



