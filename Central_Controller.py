
#Viktigt att påpeka att jag skriver denna kod jättesent och är pisstrött, många funktioner går säkert att kombinera till en men whatever, det kan man göra imorn :skull: 



import machine
import framebuf
import time
import random
from machine import Pin

Module_1 = Pin(9, Pin.IN) 
Module_2 = Pin(11, Pin.IN)
Module_3 = Pin(13, Pin.IN) # modules siffror är definerade som om man hade läst en bok, timern är upp åt vänster, så module 1 är i mitten och upp, module 2 är höger upp, module 3 är ner vänster osv
Module_4 = Pin(22, Pin.IN)
Module_5 = Pin(20, Pin.IN)

Mistake_pin = Pin(15, Pin.IN) #Pin in i pico som är kopplad till alla modulers "damn de fucka upp" pin

Completed_1 = Pin(10, Pin.IN)
Completed_2 = Pin(12, Pin.IN) 
Completed_3 = Pin(14, Pin.IN) #Pinsen som är inkopplade till "jag är löst" output pinen på varje modul
Completed_4 = Pin(21, Pin.IN)
Completed_5 = Pin(19, Pin.IN)


Module_list = [Module_1, Module_2, Module_3, Module_4, Module_5] #Lista med alla moduler, kopplade och okopplade
Connected_modules = []
Mistake_list = [] 


def Module_connection_check(): 
    for i in range(0,len(Module_list)): #checkar vilka moduler är inkopplade och skapar en lista som representerar detta, om inkopplade moduler = 1, 3, 4, då blir listan [1,0,1,1,0]...

        if Module_list[i].value() == 1:   #så kan man sen jämföra tex om bomben är klar genom att se om avklarade modul listan är samma som modul listan
            Connected_modules.append(1)

        else:
            Connected_modules.append(0)
    return Connected_modules
        

def Completed_modules():
    Completed_list = [Completed_1.value(), Completed_2.value(), Completed_3.value(), Completed_4.value(), Completed_5.value()] #Skapar en lista med värden 0 och 1 som man kan sen jämföra med "kopplade moduler" listan                                                                                                      # är dem samma så är bomben löst, för alla tillgängliga moduler är lösta liksom, 
    return Completed_list                                                                                                      #Behöver checkas hela tiden så är innuti funktionen

def Solved(Completed_list, Connected_modules):
    if Completed_list == Connected_modules: #Jämför Klara moduler med kopplade moduler, är alla moduler som är kopplade klara? Ja -> bomben e löst
        #gör nått här idunno
        print("Bomb is solved")

def Mistakes():
    if Mistake_pin.value() == 1: #när pico pinen kopplad till mistag pinnen på modulerna är HIGH -> Lägg till ett misstag till listan 
        Mistake_list.append("X")
    return len(Mistake_list) #1, 2, 3 misstag i nummer istället för att krånga med en list
 
def Boom(Mistakes):
    if Mistakes == 3: # Om 3 misstag sker ger den ut en etta
        return 1

x = 0

while x != 1:
    Number_of_Mistakes = Mistakes()
    print(Mistake_list,Number_of_Mistakes,"number of mistakes") #Bara test, men insåg här att det är viktigt att ha delay, typ 0.2 sekunder för annars blir 1 misstag = 1000 misstag, man ska ge den tid att hinna registrera
    time.sleep(0.2)
    print(Boom(Number_of_Mistakes))
    if Boom(Number_of_Mistakes) == 1:
        x = 1
print("Boom")



#print("Connected Modules:", Module_connection_check()) # printar vilka moduler är inkopplade
#print("Completed Modules:", Completed_modules()) # printar vilka moduler är avklarade
#Solved(Completed_modules(),Module_connection_check())
#ha en loop som minskar sekunder och när sekunder blir noll minskar minuter, när minuter och sekunder == 0, boom. varför så? för varje sekund kan man checka för misstag?? lowkey dålig ide men en ide! lol