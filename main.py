import machine
import framebuf
import time
import random
from machine import Pin
import Central_Controller

x = 0

while x != 1:
    Number_of_Mistakes = Central_Controller.Mistakes() #Bara test, men insåg här att det är viktigt att ha delay, typ 0.2 sekunder för annars blir 1 misstag = 1000 misstag, man ska ge den tid att hinna registrera
    time.sleep(0.2)
    print(Central_Controller.Boom(Number_of_Mistakes))
    if Central_Controller.Boom(Number_of_Mistakes) == 1:
        x = 1
print("Boom")