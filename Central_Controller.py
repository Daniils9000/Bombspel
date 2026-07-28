
#Viktigt att påpeka att jag skriver denna kod jättesent och är pisstrött, många funktioner går säkert att kombinera till en men whatever, det kan man göra imorn :skull: 



import machine
import framebuf
import time
import random
from machine import Pin
import utime
from ssd1306 import SSD1306_I2C

i2c = machine.I2C(sda=Pin(16), scl=Pin(17))
print(i2c.scan())


from ssd1306 import SSD1306_I2C
oled = SSD1306_I2C(128, 64, i2c)


module_1 = Pin(9, Pin.IN) 
module_2 = Pin(11, Pin.IN)
module_3 = Pin(13, Pin.IN) # modules siffror är definerade som om man hade läst en bok, timern är upp åt vänster, så module 1 är i mitten och upp, module 2 är höger upp, module 3 är ner vänster osv
module_4 = Pin(22, Pin.IN)
module_5 = Pin(20, Pin.IN)

mistake_pin = Pin(15, Pin.IN) #Pin in i pico som är kopplad till alla modulers "damn de fucka upp" pin

completed_1 = Pin(10, Pin.IN)
completed_2 = Pin(12, Pin.IN) 
completed_3 = Pin(14, Pin.IN) #Pinsen som är inkopplade till "jag är löst" output pinen på varje modul
completed_4 = Pin(21, Pin.IN)
completed_5 = Pin(19, Pin.IN)


module_list = [module_1, module_2, module_3, module_4, module_5] #Lista med alla moduler, kopplade och okopplade
mistake_list = [] 


def connected_modules(): 
    connected_modules_list = []
    for i in range(0,len(module_list)): #checkar vilka moduler är inkopplade och skapar en lista som representerar detta, om inkopplade moduler = 1, 3, 4, då blir listan [1,0,1,1,0]...

        if module_list[i].value() == 1:   #så kan man sen jämföra tex om bomben är klar genom att se om avklarade modul listan är samma som modul listan
            connected_modules_list.append(1)

        else:
            connected_modules_list.append(0)
    return connected_modules_list
        

def completed_modules():
    completed_list = [completed_1.value(), completed_2.value(), completed_3.value(), completed_4.value(), completed_5.value()] #Skapar en lista med värden 0 och 1 som man kan sen jämföra med "kopplade moduler" listan                                                                                                      # är dem samma så är bomben löst, för alla tillgängliga moduler är lösta liksom, 
    return completed_list                                                                                                      #Behöver checkas hela tiden så är innuti funktionen

def solved(completed_list, connected_modules):
    if completed_list == connected_modules and connected_modules != [0,0,0,0,0]: #Jämför Klara moduler med kopplade moduler, är alla moduler som är kopplade klara? Ja -> bomben e löst
        #gör nått här idunno
        print("Bomb is solved")
        return 1

def mistakes():
    if mistake_pin.value() == 1:  #när pico pinen kopplad till mistag pinnen på modulerna är HIGH -> Lägg till ett misstag till listan        
        mistake_list.append("X")
        time.sleep(0.5)
        print(mistake_list)
    return len(mistake_list) #1, 2, 3 misstag i nummer istället för att krånga med en list
 
def boom(mistakes):
    if mistakes == 3: # Om 3 misstag sker ger den ut en etta
        return 0 #stänger av spelet


#print("Connected Modules:", connected_Modules()) # printar vilka moduler är inkopplade
#print("Completed Modules:", Completed_modules()) # printar vilka moduler är avklarade
#Solved(Completed_modules(),connected_Modules())
#ha en loop som minskar sekunder och när sekunder blir noll minskar minuter, när minuter och sekunder == 0, boom. varför så? för varje sekund kan man checka för misstag?? lowkey dålig ide men en ide! lol

#ta bort detta sen ofc

buf = bytearray(128 * 64 // 8)

Buffer = framebuf.FrameBuffer(buf, 128, 64, framebuf.MONO_HLSB)

# Draw normal text into the small buffer







def scale():
    Buffer.fill(0)
    Buffer.text("TEXT", 0, 0, 1)

    # Scale it up
    scale = 2

    for y in range(128):
        for x in range(64):
            if Buffer.pixel(x, y):
                oled.fill_rect(x * scale, y * scale, scale, scale, 1)


def tid(m,s,start_tid,game): #minuter och sekunder som input 

    s_x_placement = 16    #66 
    s_y_placement = 10    #30 säger var klockan är på skärmen
    m_x_placement = 0   #50
    m_y_placement = s_y_placement

    if game == 1:
        passerad_tid = utime.ticks_ms() 
        runtime = utime.ticks_diff(passerad_tid,start_tid)
        #print(runtime)

        if m != 0 and s >= 10:
            oled.text(str(m) + ":", m_x_placement , m_y_placement, 1)
            oled.text(str(s), s_x_placement, s_y_placement, 1)
            oled.show()
            if runtime >= 1000:
                print("en sekund har gått")
                start_tid = utime.ticks_ms()
                oled.text(str(s), s_x_placement, s_y_placement, 0)
                oled.show()
                s = s - 1
            return m,s,start_tid,game
        
            
        elif m != 0 and s <= 9 and s != 0:
            oled.text(str(m) + ":", m_x_placement , m_y_placement, 1)
            oled.text("0" + str(s), s_x_placement, s_y_placement, 1)
            oled.show()
            if runtime >= 1000:
                print("en sekund har gått")
                start_tid = utime.ticks_ms()
                oled.text("0" + str(s), s_x_placement, s_y_placement, 0)
                oled.show()
                s = s - 1
            return m,s,start_tid,game

        elif m != 0 and s == 0:
            oled.text(str(m) + ":", m_x_placement , m_y_placement, 1)
            oled.text("0" + str(s), s_x_placement, s_y_placement, 1)
            oled.show()
            if runtime >= 1000:
                print("en sekund har gått")
                start_tid = utime.ticks_ms()
                oled.text("0" + str(s), s_x_placement, s_y_placement, 0)
                oled.show()
                s = 59
                oled.text(str(m) + ":", m_x_placement , m_y_placement, 0)
                m = m - 1
            return m,s,start_tid
            
        elif m == 0 and s >= 10:
            oled.text(str(m) + ":", m_x_placement , m_y_placement, 1)
            oled.text(str(s), s_x_placement, s_y_placement, 1)
            oled.show()
            if runtime >= 1000:
                print("en sekund har gått")
                start_tid = utime.ticks_ms()
                oled.text(str(s), s_x_placement, s_y_placement, 0)
                oled.show()
                s = s - 1
            return m,s,start_tid,game
            
        elif m == 0 and s <= 9 and s != 0:
            oled.text(str(m) + ":", m_x_placement , m_y_placement, 1)
            oled.text("0" + str(s), s_x_placement, s_y_placement, 1)
            oled.show()
            if runtime >= 1000:
                print("en sekund har gått")
                start_tid = utime.ticks_ms()
                oled.text("0" + str(s), s_x_placement, s_y_placement, 0)
                oled.show()
                s = s - 1
            return m,s,start_tid,game
        
        elif m == 0 and s == 0:
            game = 0
            oled.text(str(m) + ":", m_x_placement , m_y_placement, 0)
            oled.text("BOOM", 45, 29, 1)
            oled.show()
            print("Boom")
            return m,s,start_tid,game

def main(minuter, sekunder):
    game = 1 #startar spelet
    start_tid = utime.ticks_ms()
    while game == 1:
        #print("new loop")
        #print(connected_modules())
        antal_misstag = mistakes()
        print(completed_modules())
        if solved(completed_modules(), connected_modules()) == 1:
            game = 0
            oled.fill(0)
            oled.show
            for i in range(0,5):
                oled.text("Win", 0, 0, 1)
                oled.show()
                time.sleep(0.7)
                oled.text("Win", 0, 0, 0)
                oled.show()
                time.sleep(0.7)
                i = i + 1

        elif antal_misstag == 3:
            game = 0
            oled.fill(0)
            oled.show()
            print("boom")
            oled.text("Boom",0,0,1)
            oled.show()

        else:
            tiden = tid(minuter,sekunder,start_tid,game)
            minuter = tiden[0] #type: ignore
            sekunder = tiden[1] #type: ignore
            start_tid = tiden[2] #type: ignore
            game = tiden[3] #type: ignore


#print(completed_2.value())
#while True:
 #   print(connected_modules(),"connected")
  #  print(completed_modules(),"completed")
   # solved(connected_modules(), completed_modules())
   # time.sleep(0.5)
    #time.sleep(1)
main(0,5) #minuter sekunder
#while True:
 #   print(connected_Modules())
