
import cgi
form = cgi.FieldStorage()
action =    form.getfirst("ip", "none")
port =    form.getfirst("port", "4001")
counter_type = form.getfirst("counter_type", "none")
nt = form.getfirst("nt", "none")
print("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Проверка счётчиков</title>
        </head>
        <body>
            <center>
            <H1>Проверка приборов учёта</H1><BR>
            <form action="/cgi-bin/monitor.py">
                <table border=1>
                    <tr>
                        <td>IP:
                            <input type="text" name="ip" value='"""+action+"""'><BR>
                        </td>
                        <td>
                            Порт счётчика:
                            <input type="text" name="port" value='"""+port+"""'><BR>
                        </td>
                        <td align="center">
                            <select size="3" multiple name="counter_type">
                                <option disabled>Выберите тип</option>
                                <option selected value="spt943">СПТ943</option>
                                <option value="merc">Меркурий</option>
                            </select><BR>
                        </td>
                        <td>
                            Сетевой номер(NT):
                            <input type="text" name="nt" value='"""+str(nt)+"""'><BR>
                            <input type="submit" value="Проверить">
                         </td>
                    </tr>
            </form>""")


import time
from crccheck.crc import CrcModbus

from datetime import datetime
from socket import *
import os
import pickle


commands = {"merc" : " ",
            "start" : "FF FF FF FF FF FF FF FF FF FF FF FF FF",
            "vkt-7":"FF FF 00 10 3F FF 00 00 CC 80 00 00 00 64 54",
            "spt943":"3F 00 00 00 00 BF 16",
            "speed":"10 01 42 02 00 00 00 ba 16",
            "tt1":"10 00 90 01 00 05 00 3F 00 00 00 00 8B 31 16",
            "pr1":"10 01 90 19 00 05 00 3f 00 00 00 00 29 79"}

obj = {}

def get_port_access(HOST, PORT):
    ADDR = (HOST, PORT)
    client = socket(AF_INET, SOCK_STREAM)
    client.settimeout(3)
    try:
        client.connect((ADDR))
        data = 'Подключено'
        client.close()
    except ConnectionRefusedError:
        data = "Ошибка недоступен порт "+str(PORT)
        log_this(HOST + "  недоступен порт "+str(PORT)+" \n")
    except timeout:
        data = "Не подключено, недоступен порт "+str(PORT)
        log_this(HOST+"  недоступен порт "+str(PORT)+" \n")
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
        #client.send(bytearray.fromhex("08 00"))
        #client.send(byte_command('start'))
        #client.send(byte_command('spt943'))
        data = client.recv(BUFSIZE)
        data = binascii.hexlify(bytearray(data))
        client.close()
    except ConnectionRefusedError:
        data = "Ошибка"
        log_this(HOST + "  недоступен счётчик\n")
    except timeout:
        data = "недоступен"
        log_this(HOST + "  недоступен счётчик\n")
    return data

def get_from_counter(HOST, PORT, command):
    ADDR = (HOST, PORT)
    BUFSIZE = 100                #Размер буфера
    client = socket(AF_INET, SOCK_STREAM)
    client.settimeout(3)
    try:
        client.connect((ADDR))
        client.send(byte_command('start'))
        time.sleep(2)
        client.send(byte_command(command))
        #client.send(bytearray.fromhex(data))
        #time.sleep(1)
        data = client.recv(BUFSIZE)
        data = client.recv(BUFSIZE)
        data = binascii.hexlify(bytearray(data))
        client.close()
    except ConnectionRefusedError:
        data = "Ошибка"
        log_this(HOST + "  недоступен счётчик\n")
    except timeout:
        data = "Счётчик недоступен"
        log_this(HOST + "  недоступен счётчик\n")
    return data

def get_info():
    for hostname in hostnames:
        # response = os.system("ping " + hostname+"  -n 1")
        response = os.system("ping -c 4 " + hostname)
        # and then check the response...
        if response == 0:
            print(hostname, 'доступен!')
            obj[hostname] = {'router': 'good',
                             'adress': hostnames[hostname]['adress'],
                             't-12': get_port_access(hostname, hostnames[hostname]['port']),
                             'counter': get_merc_info(hostname, hostnames[hostname]['port'], hostnames[hostname]['NT']),
                             'time': datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")}

        else:
            log_this(hostname + "  недоступен роутер\n")
            print(hostname, 'недоступен')
            # obj[hostname] = {'router': 'no ping', 'adress': hostnames[hostname],'t-12':get_t_12(hostname,4001)}
            obj[hostname] = {'router': 'no ping',
                             'adress': hostnames[hostname]['adress'],
                             't-12': get_port_access(hostname, hostnames[hostname]['port']),
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


def add_cs_spt(data,NT):
    data_byte = bytearray.fromhex(NT+data)
    byte_sum = 0
    for by in data_byte:
        byte_sum += by
    result = hex(0xFF^byte_sum)
    result = result[len(result)-2:len(result)]
    return "10 "+ NT + " " + data + " " + result+" 16"

#while 1:
#get_info()
#make_html()
import binascii
def get():
    if counter_type == "spt943":
        res = get_from_counter(action, int(port), add_cs_spt('spt943', nt))
    elif counter_type == "merc":
        res = get_merc_info(action, int(port), int(nt))

    print("<tr><td>Роутер:")
    print(get_port_access(action, int(80)))
    print("</td><td>Телепорт-12: ")
    print(get_port_access(action, int(port)))
    print("</td><td>Телепорт-12 WEB: ")
    print(get_port_access(action, int(88)))
    print("</td><td><BR>Счётчик: -->")
    print("...")
    print("<BR>Счётчик: <--")
    print(res)
    print("</td></tr></table>")

get()


