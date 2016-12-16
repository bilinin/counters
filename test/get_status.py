import time
from crccheck.crc import CrcModbus

from datetime import datetime
from socket import *
import os
import pickle


commands = {"merc" : "00 00 01 B0",
            "start" : "FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF ",
            "vkt-7":"FF FF 00 10 3F FF 00 00 CC 80 00 00 00 64 54",
            "spt943":"3F 00 00 00 00 BF 16",
            "speed":"10 01 42 02 00 00 00 ba 16",
            "tt1":"10 00 90 01 00 05 00 3F 00 00 00 00 8B 31 16",
            "pr1":"10 01 90 19 00 05 00 3f 00 00 00 00 29 79"}

obj = {}

def get_t_12(HOST,PORT):
    ADDR = (HOST, PORT)
    BUFSIZE = 1
    client = socket(AF_INET, SOCK_STREAM)
    client.settimeout(3)
    try:
        client.connect((ADDR))
        #client.send(b'0x0D')
        #data = client.recv(BUFSIZE)
        data = 'Подключено'
        client.close()
    except ConnectionRefusedError:
        data = "Ошибка"
        log_this(HOST + "  недоступен телепорт\n")
    except timeout:
        data = "Не подключено"
        log_this(HOST+"  недоступен телепорт\n")
    return data

def byte_command(command):
    return bytearray.fromhex(commands[command])

def get_merc_info(HOST, PORT, NT):
    get = get_(NT)
    #print(get)
    ADDR = (HOST, PORT)
    BUFSIZE = 100                #Размер буфера
    client = socket(AF_INET, SOCK_STREAM)
    client.settimeout(3)
    try:
        client.connect((ADDR))
        #client.send(bytearray.fromhex(commands['vkt-7']))) #ВКТ-7
        client.send(get)  # Меркурий 00 00 01 B0
        time.sleep(2)
        #client.send(bytearray.fromhex("08 00"))
        #client.send(byte_command('start'))
        #client.send(byte_command('spt943'))
        data = client.recv(BUFSIZE)
        #data = "доступен"
        client.close()
    except ConnectionRefusedError:
        data = "Ошибка"
        log_this(HOST + "  недоступен счётчик\n")
    except timeout:
        data = "недоступен"
        log_this(HOST + "  недоступен счётчик\n")
    return data

def get_from_c(HOST,PORT, command):
    ADDR = (HOST, PORT)
    BUFSIZE = 100                #Размер буфера
    client = socket(AF_INET, SOCK_STREAM)
    client.settimeout(3)
    try:
        client.connect((ADDR))
        #client.send(byte_command('start'))
        #time.sleep(2)
        client.send(byte_command(command))
        #client.send(bytearray.fromhex(data))
        #time.sleep(1)
        #data = client.recv(BUFSIZE)
        data = client.recv(BUFSIZE)
        client.close()
    except ConnectionRefusedError:
        data = "Ошибка"
        log_this(HOST + "  недоступен счётчик\n")
    except timeout:
        data = "Счётчик недоступен"
        log_this(HOST + "  недоступен счётчик\n")
    return data

def make_html():
    f = open('index.html', 'w')
    f.write("""<!DOCTYPE HTML>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Мониторинг</title>
                </head>
                <body>
            <center>
            <table border=1>
                <tr>
                        <td>Адресс</td>
                        <td>IP</td>
                        <td>Пинг</td>
                        <td>Телепорт</td>
                        <td>Счётчик</td>
                        <td>Время</td>
                </tr>

            """)

    input = open('ip_s.pkl', 'rb')
    obj = pickle.load(input)
    input.close()

    for current in obj:
        f.write("""<tr>
                    <td>""" + obj[current]['adress'] + """</td>
                    <td>""" + current + """</td>
                    <td>""" + obj[current]['router'] + """</td>
                    <td>""" + obj[current]['t-12'] + """</td>
                    <td>""" + obj[current]['counter'] + """</td>
                    <td>""" + obj[current]['time'] + """</td>
         </tr>
        """)

    f.write('</table></center>')
    f.close()

def get_info():
    for hostname in hostnames:
        # response = os.system("ping " + hostname+"  -n 1")
        response = os.system("ping -c 4 " + hostname)
        # and then check the response...
        if response == 0:
            print(hostname, 'доступен!')
            obj[hostname] = {'router': 'good',
                             'adress': hostnames[hostname]['adress'],
                             't-12': get_t_12(hostname, hostnames[hostname]['port']),
                             'counter': get_merc_info(hostname, hostnames[hostname]['port'], hostnames[hostname]['NT']),
                             'time': datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")}

        else:
            log_this(hostname + "  недоступен роутер\n")
            print(hostname, 'недоступен')
            # obj[hostname] = {'router': 'no ping', 'adress': hostnames[hostname],'t-12':get_t_12(hostname,4001)}
            obj[hostname] = {'router': 'no ping',
                             'adress': hostnames[hostname]['adress'],
                             't-12': get_t_12(hostname, hostnames[hostname]['port']),
                             'counter': get_merc_info(hostname, hostnames[hostname]['port'], hostnames[hostname]['NT']),
                             'time': datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")}
    output = open('ip_s.pkl', 'wb')
    pickle.dump(obj, output, 4)
    output.close()

def log_this(what):
    f = open('log.txt', 'a')
    f.write(what)
    f.close()


def get_(this):# Quick calculation
    if this>10:
        data = str(hex(this)[2:])+"00"
    else:
        data = "0"+str(hex(this)[2:]) + "00"
    data_byte = bytearray.fromhex(data)
    crc = CrcModbus.calchex(data_byte)
    crc_byte = bytearray.fromhex(crc)
    crc_byte.reverse()
    return data_byte+crc_byte
#while 1:
#get_info()
#make_html()
import binascii
binascii.hexlify(bytearray())

#res = get_from_counter("212.164.230.203", 4001, 'spt943')
#res = get_from_counter("212.164.217.137", 4001, 'merc')
res = get_merc_info("212.164.217.137", 4001, 68)
#res = get_merc_info("212.20.42.202", 21160, 235)

print(binascii.hexlify(bytearray(res)))