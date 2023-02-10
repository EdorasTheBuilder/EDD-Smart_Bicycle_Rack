from gpiozero import Servo as sv
from time import sleep as sl

servo = sv(4)


sl(1)
servo.min()
sl(1)
servo.max()
sl(1)
servo.mid()
