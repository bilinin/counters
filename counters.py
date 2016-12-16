from socket import *

import binascii


def hex_from_int(NT):
    if NT < 16:
        NT = '0' + hex(int(NT))[2:]
    else:
        NT = hex(int(NT))[2:]
    return NT

def add_cs_spt(data, NT):
    NT = hex_from_int(int(NT))
    data_byte = bytearray.fromhex(NT + data)
    byte_sum = 0
    for by in data_byte:
        byte_sum += by
    result = hex(0xFF ^ byte_sum)
    result = result[len(result) - 2:len(result)]
    result = "10 " + NT + " " + data + " " + result + " 16"
    return bytearray.fromhex(result)

"""
def get_from_count(HOST, PORT, command):
    ADDR = (HOST, PORT)
    BUFSIZE = 100  # Размер буфера
    client = socket(AF_INET, SOCK_STREAM)
    client.settimeout(3)
    try:
        client.connect(ADDR)
        client.send(add_cs_spt("3F 00 00 00 00",1))
        data = client.recv(BUFSIZE)
        client.close()
    except ConnectionRefusedError:
        data = "Ошибка"
        log_this(HOST + "  недоступен счётчик\n")
    except timeout:
        data = "Счётчик недоступен"
        log_this(HOST + "  недоступен счётчик\n")
    return data
"""

def get_from_counter(HOST, PORT, send_data):
    ADDR = (HOST, PORT)
    BUFSIZE = 100  # Размер буфера
    client = socket(AF_INET, SOCK_STREAM)
    client.settimeout(3)
    try:
        client.connect(ADDR)
        client.send(send_data)
        ##################################################################
        print("--> ")
        print(binascii.hexlify(send_data))
        print("<BR>")

        ##################################################################


        data = client.recv(BUFSIZE)
        flag = True

##################################################################

        while (flag):
            try:
                data = data + client.recv(BUFSIZE)
            except:
                print("<-- ")
                print( binascii.hexlify(data))
                print("<BR>")
                flag = False

##################################################################

        client.close()
    except ConnectionRefusedError:
        data = "Ошибка"
        log_this(HOST + "  недоступен счётчик\n")
    except timeout:
        data = "Счётчик недоступен"
        log_this(HOST + "  недоступен счётчик\n")
    return data

def log_this(what):
    f = open('log.txt', 'a')
    f.write(what)
    f.close()
