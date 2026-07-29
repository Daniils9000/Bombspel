
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


mistake_pin = Pin(15, Pin.IN) #Pin in i pico som är kopplad till alla modulers "damn de fucka upp" pin

start_game_pin = Pin(1, Pin.IN)

module_1 = Pin(9, Pin.IN) 
module_2 = Pin(11, Pin.IN)
module_3 = Pin(13, Pin.IN) # modules siffror är definerade som om man hade läst en bok, timern är upp åt vänster, så module 1 är i mitten och upp, module 2 är höger upp, module 3 är ner vänster osv
module_4 = Pin(22, Pin.IN)
module_5 = Pin(20, Pin.IN)

completed_1 = Pin(10, Pin.IN)
completed_2 = Pin(12, Pin.IN) 
completed_3 = Pin(14, Pin.IN) #Pinsen som är inkopplade till "jag är löst" output pinen på varje modul
completed_4 = Pin(21, Pin.IN)
completed_5 = Pin(19, Pin.IN)


module_list = [module_1, module_2, module_3, module_4, module_5] #Lista med alla moduler, kopplade och okopplade
mistake_list = [] 

buf = bytearray(128 * 64 // 8) #skapar en kanvas för buffern basically

Buffer = framebuf.FrameBuffer(buf, 128, 64, framebuf.MONO_HLSB) #buffer där man skriver saker i och sedan gör dem sakerna större med scale()




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
        print("Bomb is solved")
        return 1

def mistakes():
    if mistake_pin.value() == 1:  #när pico pinen kopplad till mistag pinnen på modulerna är HIGH -> Lägg till ett misstag till listan        
        mistake_list.append("X")
        #LÄGG TILL BUZZER HÄR
        time.sleep(0.150)
        print(mistake_list)
    return len(mistake_list) #1, 2, 3 misstag i nummer istället för att krånga med en list
 
def boom(mistakes):
    if mistakes == 3: # Om 3 misstag sker ger den ut en etta
        return 0 #stänger av spelet


buf = bytearray(128 * 64 // 8)

buffer = framebuf.FrameBuffer(buf, 128, 64, framebuf.MONO_HLSB)



def scale_and_draw(): #skalar och ritar/tar bort sak från skärmen. om man vill att den ska rita sätt variabeln till 1, om man vill att den ska ta bort = 0. nollan är egentligen användbar enbart i remove from screen funktionen
    x_scale = 4                       #vet inte hur jag ska implementera skalan in i remove lättare än så, så det får vara såhär.
    y_scale = 6
    for y in range(2,10):
        for x in range(1,32): #konstiga värden men dem är optimerade till positionen på skärmen och prestanda, sen är prestandan ganska ass pga scale loopsen men, vet ej hur jag gör annorlunda.
            if buffer.pixel(x, y):
                oled.fill_rect(x * x_scale, y * y_scale, x_scale, y_scale, 1)
    oled.show()



def draw_buffer_minutes(m,m_x,m_y): #m = minuter, m_x är minut position på skärmen i x led, samma med m_y fast y led
        buffer.text(str(m) + ":", m_x, m_y, 1) 
        scale_and_draw()


def draw_buffer_seconds(s,s_x,s_y):    #s = sekunder, resten same shit
        if s >= 10:
            buffer.text(str(s),s_x,s_y,1) 
            scale_and_draw()
        elif s < 10:
            buffer.text("0" + str(s), s_x, s_y, 1)
            scale_and_draw()


def remove_from_screen(what_to_remove):                             #Om man ska byta ut sekund -> what_to_remove = 1. Om minut -> 0. När minuten minskar så behöver man ersätta minuten och sekunderna, så båda ska bort. Om bara sekund, aaa du. 
                                                                    #Hela funktionen är egentligen bypass så att man inte behöver använda sig av scale, den drar ned prestandan som faan.
    if what_to_remove == 0: #Om minuten och sekunden ska bytas ut  
        oled.fill_rect(0, 0, 30, 64, 0) # tar bort minuten,
        oled.fill_rect(60, 0, 128, 64, 0) # tar bort minuten,
        buffer.fill(0)
        oled.show()
    elif what_to_remove == 1: #Om bara sekunden ska bytas ut
        oled.fill_rect(60, 0, 128, 64, 0) # tar bort minuten,
        buffer.fill(0)
        oled.show()
    elif what_to_remove == 2: #hela skärmen
        oled.fill_rect(0, 0, 128, 64, 0) # tar bort minuten,
        buffer.fill(0)
        oled.show()  




def tid(m,s,start_tid,game, delay_compensation, misstag):       #minuter och sekunder som input, game är "är spelet igång", blir game 0 => "basically" game over. 
    s_x_placement = 16               #                          #varje misstag gör så att tiden går fortare
    s_y_placement = 3                #                          #Delay_compensation För att countra problemet med att det blir typ 70 ms för mycket varje gång en "sekund" går. Den tickar över liksom och blir till 1070ms då den räknar sekunden
    m_x_placement = 0                #                          #utan den blir bombens 5 minuter = 6m  fucked upp, jävla scale funktion asså. Och endå blir bombens 5 minuter = 5 min 5 sec nu även efter kompenseringen, blir ej bättre än så
    m_y_placement = s_y_placement    #dem här bestämmer var timern är, rör ej

    if game == 1:
        passerad_tid = utime.ticks_ms() 
        runtime = utime.ticks_diff(passerad_tid,start_tid) #tiden går 1% fortare med varje misstag
        time_modifier = 1000 * (1 - 0.08*misstag)             # gör så att tiden går 8% fortare med varje misstag så totalt 16% max, kan tweakas sen
        print(time_modifier)

        if m != 0 and s !=0:
            draw_buffer_minutes(m,m_x_placement,m_y_placement)      #ritar minut och 
            draw_buffer_seconds(s,s_x_placement,s_y_placement)      #sekund i buffern och ritar det på skärmen skalad
            if runtime >= time_modifier:
                start_tid = utime.ticks_ms() - delay_compensation                        
                remove_from_screen(1)   #tar bort förra sekunden från skärmen så att ny sekund kan ritas, rensar också buffern av samma skäl
                s = s - 1
            return m,s,start_tid,game
        

        elif m != 0 and s == 0:
            draw_buffer_minutes(m,m_x_placement,m_y_placement)
            draw_buffer_seconds(s,s_x_placement,s_y_placement)

            if runtime >= time_modifier:
                start_tid = utime.ticks_ms() - delay_compensation
                remove_from_screen(0)
                s = 59
                m = m - 1
            return m,s,start_tid,game


            
        elif m == 0 and s != 0:
            draw_buffer_minutes(m,m_x_placement,m_y_placement)      #ritar minut och 
            draw_buffer_seconds(s,s_x_placement,s_y_placement)      #sekund i buffern och ritar det på skärmen skalad
            if runtime >= time_modifier:
                start_tid = utime.ticks_ms() - delay_compensation                        
                remove_from_screen(1)   #tar bort förra sekunden från skärmen så att ny sekund kan ritas, rensar också buffern av samma skäl
                s = s - 1
            return m,s,start_tid,game
                    
        
        elif m == 0 and s == 0:
            game = 0
            oled.fill(0)
            buffer.text("BOOM", m_x_placement, m_y_placement, 1) 
            scale_and_draw()
            print("BOOM")
            return m,s,start_tid,game
    else:
        return m,s,start_tid,game





def main(minuter, sekunder, delay_compensation):
    game = 1 #startar spelet
    start_tid = utime.ticks_ms() - delay_compensation 

    while game == 1:
        antal_misstag = mistakes()


        if solved(completed_modules(), connected_modules()) == 1:
            game = 0 
            tiden = tid(minuter,sekunder,start_tid,game,delay_compensation,antal_misstag) #tiden är en tuple (m,s,start_tid,game) vi behöver bara minuter och sekunder

            #lägg till buzzer här
            
            while start_game_pin.value() == 0 and game == 0:
                draw_buffer_minutes(tiden[0],0,3)   #type: ignore   
                draw_buffer_seconds(tiden[1],16,3)  #type: ignore
                time.sleep(0.8)

                remove_from_screen(2) 

                print("solved test type shi")
                time.sleep(0.8)


        elif antal_misstag == 3:
            game = 0
            oled.fill(0)
            buffer.fill(0)
            oled.show()
            print("boom") #----
            buffer.text("BOOM",0,3,1)
            scale_and_draw()


        else:
            tiden = tid(minuter,sekunder,start_tid,game,delay_compensation,antal_misstag)
            minuter = tiden[0] #type: ignore
            sekunder = tiden[1] #type: ignore
            start_tid = tiden[2] #type: ignore         #den gillar inte att jag lägger in "tomma" värden för dem är tomma tills koden körs? tror jag iaf, går att ignorera verkar de som
            game = tiden[3] #type: ignore


    


#print(completed_2.value())
#while True:
 #   print(connected_modules(),"connected")
  #  print(completed_modules(),"completed")
   # solved(connected_modules(), completed_modules())
   # time.sleep(0.5)
    #time.sleep(1)
main(0,6,70) #minuter sekunder
#while True:
