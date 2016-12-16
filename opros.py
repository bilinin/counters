from base import *

def opros():
    base = read_bd()
    for current in base:
            print(current)
            put_to_base(current,base)
            print("Опрос " + str(current)+" удачно ")

#while(1):
opros()