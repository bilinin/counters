from base import *

IP =  '212.20.42.202'
PORT = 21160
i = 0
for nt in range(0,256):
    NT = hex_from_int(nt)
    current = get_from_counter(IP, PORT, crc_merc(NT+" 01 01 01 01 01 01 01 01"))
    print("Номер "+ str(i) + " " + str(current))
    i += 1