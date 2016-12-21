from excel import *
from counters import *
from bd import *
from float_spt import *

import random
import cgi
import binascii
from datetime import datetime
from crccheck.crc import CrcModbus

counter_merc = {
    'sn': '',
    'energy': ''}

commands = {"merc": "00 00 01 b0",
            "start": "FF FF FF FF FF FF FF FF FF FF FF FF FF",
            "vkt-7": "FF FF 00 10 3F FF 00 00 CC 80 00 00 00 64 54",
            "spt943": "3F 00 00 00 00 BF 16",
            "speed": "10 01 42 02 00 00 00 ba 16",
            "tt1": "10 00 90 01 00 05 00 3F 00 00 00 00 8B 31 16",
            "pr1": "10 01 90 19 00 05 00 3f 00 00 00 00 29 79"}

obj = {}

def get_(this):  # Quick calculation
    if this > 10:
        data = str(hex(this)[2:]) + "00"
    else:
        data = "0" + str(hex(this)[2:]) + "00"
    data_byte = bytearray.fromhex(data)
    crc = CrcModbus.calchex(data_byte)
    crc_byte = bytearray.fromhex(crc)
    crc_byte.reverse()
    return data_byte + crc_byte

def crc_merc(data):  # Quick calculation
    data_byte = bytearray.fromhex(data)
    crc = CrcModbus.calchex(data_byte)
    crc_byte = bytearray.fromhex(crc)
    crc_byte.reverse()
    return data_byte + crc_byte

def put_to_base(id, base_counters):
    id = int(id)
    if base_counters[id]['counter_type'] == "spt943":                                                                       #Пока много кастылей
        res = get_from_counter(base_counters[id]['ip'], int(base_counters[id]['port']),  bytearray.fromhex("FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF "))
        res = get_from_counter(base_counters[id]['ip'], int(base_counters[id]['port']), add_cs_spt("3F 00 00 00 00",1))
        res = get_from_counter(base_counters[id]['ip'], int(base_counters[id]['port']), add_cs_spt("52 04 02 2C 00",1))
#       Первый
        begin_pos = 0
        for i, current in enumerate(res):
            if current == 16:
                begin_pos = i
        current = str(float_from_byte(bytearray(res[begin_pos + 3:begin_pos + 7])))
        print("<br>G1 " + current)
        current = str(float_from_byte(bytearray(res[begin_pos + 7:begin_pos + 11])))
        print("<br>G2 " + current)
        current = str(float_from_byte(bytearray(res[begin_pos + 11:begin_pos + 15])))
        print("<br>G3 " + current)
        current = str(float_from_byte(bytearray(res[begin_pos + 15:begin_pos + 19])))
        print("<br>P1 " + current)
        current = str(float_from_byte(bytearray(res[begin_pos + 19:begin_pos + 23])))
        print("<br>P2 " + current)
        current = str(float_from_byte(bytearray(res[begin_pos + 23:begin_pos + 27])))
        print("<br>t1 " + current)
        current = str(float_from_byte(bytearray(res[begin_pos + 27:begin_pos + 31])))
        print("<br>t2 " + current)
        current = str(float_from_byte(bytearray(res[begin_pos + 31:begin_pos + 35])))
        print("<br>dt " + current)
        current = str(float_from_byte(bytearray(res[begin_pos + 35:begin_pos + 39])))
        print("<br>t3 " + current)
        current = str(float_from_byte(bytearray(res[begin_pos + 39:begin_pos + 43])))
        print("<br>tх " + current)
        current = str(float_from_byte(bytearray(res[begin_pos + 43:begin_pos + 47])))
        print("<br>tв " + current)

#       Второй
        res = get_from_counter(base_counters[id]['ip'], int(base_counters[id]['port']), add_cs_spt("52 34 02 2C 00", 1))

        begin_pos = 0
        for i, current in enumerate(res):
            if current == 16:
                begin_pos = i
        current = str(float_from_byte(bytearray(res[begin_pos + 3:begin_pos + 7])))
        print("<br>G1 " + current)
        current = str(float_from_byte(bytearray(res[begin_pos + 7:begin_pos + 11])))
        print("<br>G2 " + current)
        current = str(float_from_byte(bytearray(res[begin_pos + 11:begin_pos + 15])))
        print("<br>G3 " + current)
        current = str(float_from_byte(bytearray(res[begin_pos + 15:begin_pos + 19])))
        print("<br>P1 " + current)
        current = str(float_from_byte(bytearray(res[begin_pos + 19:begin_pos + 23])))
        print("<br>P2 " + current)
        current = str(float_from_byte(bytearray(res[begin_pos + 23:begin_pos + 27])))
        print("<br>t1 " + current)
        current = str(float_from_byte(bytearray(res[begin_pos + 27:begin_pos + 31])))
        print("<br>t2 " + current)
        current = str(float_from_byte(bytearray(res[begin_pos + 31:begin_pos + 35])))
        print("<br>dt " + current)
        current = str(float_from_byte(bytearray(res[begin_pos + 35:begin_pos + 39])))
        print("<br>t3 " + current)
        current = str(float_from_byte(bytearray(res[begin_pos + 39:begin_pos + 43])))
        print("<br>tх " + current)
        current = str(float_from_byte(bytearray(res[begin_pos + 43:begin_pos + 47])))
        print("<br>tв " + current)


    elif base_counters[id]['counter_type'] == "merc":
        try:
            IP = base_counters[id]['ip']
            PORT = int(base_counters[id]['port'])
            hex_from_int(int(base_counters[id]['nt']))
            nt = hex_from_int(int(base_counters[id]['nt']))
            now_time = datetime.now()
            res = get_from_counter(IP, PORT, crc_merc(nt+" 01 01 01 01 01 01 01 01"))
            last = {'energy': 'Нет данных',
                                   'voltage1': 'Нет данных',
                                   'voltage2': 'Нет данных',
                                   'voltage3': 'Нет данных',
                                   'current1': 'Нет данных',
                                   'current2': 'Нет данных',
                                   'current3': 'Нет данных'}
            energy = get_from_counter(IP, PORT, crc_merc(nt+" 05 00 00"))
            energy = energy[1:5]
            last['energy'] = str(get_merc_energy(energy,100))
            voltage = get_from_counter(IP, PORT, crc_merc(nt+" 08 11 11"))[2:4]
            last['voltage1'] = str(get_merc_energy(voltage,100))
            voltage = get_from_counter(IP, PORT, crc_merc(nt+" 08 11 12"))[2:4]
            last['voltage2'] = str(get_merc_energy(voltage,100))
            voltage = get_from_counter(IP, PORT, crc_merc(nt+" 08 11 13"))[2:4]
            last['voltage3'] = str(get_merc_energy(voltage,100))
            current = get_from_counter(IP, PORT, crc_merc(nt+" 08 11 21"))[2:4]
            last['current1'] = str(get_merc_energy(current,1000))
            current = get_from_counter(IP, PORT, crc_merc(nt+" 08 11 22"))[2:4]
            last['current2'] = str(get_merc_energy(current,1000))
            current = get_from_counter(IP, PORT, crc_merc(nt+" 08 11 23"))[2:4]
            last['current3'] = str(get_merc_energy(current,1000))
            base_counters[id]['time'] = str(now_time.strftime("%Y-%m-%d %H:%M:%S"))
            base_counters[id]['owner']= 'good'
            base_counters[id]['last'].update(last)
            base_counters[id]['times'].update({now_time : last})

        except TypeError:
            base_counters[id]['owner'] = 'bad'
            print("Счётчик недоступен")
    save_bd(base_counters)

def get():
    if counter_type == "spt943":
        res = get_from_counter(ip, int(port), add_cs_spt('spt943', nt))
    elif counter_type == "merc":
        res = get_from_counter(ip, int(port), crc_merc("00 01 01 01 01 01 01 01 01"))
        counter_merc['sn'] = get_from_counter(ip, int(port), crc_merc("00 08 00"))
        counter_merc['sn'] = binascii.hexlify(bytearray(counter_merc['sn']))
        counter_merc['energy'] = get_from_counter(ip, int(port), crc_merc("00 05 00 00"))
        counter_merc['energy'] = binascii.hexlify(bytearray(counter_merc['energy']))

def get_merc_energy(original,divider):
    norm = bytes([c for t in zip(original[1::2], original[::2]) for c in t])
    return (int.from_bytes(norm, byteorder='big') / divider)

def hex_from_int(NT):
    if NT < 16:
        NT = '0' + hex(int(NT))[2:]
    else:
        NT = hex(int(NT))[2:]
    return NT

def print_monitoring(base_counters):
    print("""
        <table border=1>
            <tr>
                <td>Объект</td>
                <td>Тип счётчика</td>
                <td>Время опроса</td>
                <td>Состояние</td>
                <td>ОПРОС</td>
                <td>РЕДАКТИРОВАТЬ</td>
                <td>УДАЛЕНИЕ</td>
            </tr>
    """)
    for current in base_counters:
        try:
            print("""
                    <tr>
                        <td>""" + base_counters[current]['label'] + """</td>
                        <td>""" + base_counters[current]['counter_type'] + """</td>
                        <td>""" + base_counters[current]['time'] + """</td>
                        <td>""" + base_counters[current]['owner'] + """</td>
                        <td><a href='/cgi-bin/monitor.py?action=opros&id=""" + str(current) + """'> ОПРОСИТЬ<a/></td>
                        <td><a href='/cgi-bin/monitor.py?label="""+base_counters[current]['label'] +"""&ip="""+ base_counters[current]['ip'] +"""&port="""+ base_counters[current]['port'] +"""&nt="""+ base_counters[current]['nt'] +"""'>РЕДАКТИРОВАТЬ<a/></td>
                        <td><a href='/cgi-bin/monitor.py?action=del&id=""" + str(current) + """'> УДАЛИТЬ <BR><a/></td>
                    </tr>
            """)
            print("")
        except KeyError:
            print("Запись удалена<BR>")
    print("</table>")

def print_list_counters_el(base_counters):
    print("""
        <table border=1>
            <BR>Счётчики электроэнергии
            <tr>
                <td>Объект</td>
                <td>Тип счётчика</td>
                <td>Энергия кВтч</td>
                <td>V фаза 1</td>
                <td>V фаза 2</td>
                <td>V фаза 3</td>
                <td>I фаза 1</td>
                <td>I фаза 2</td>
                <td>I фаза 3</td>
                <td>Время опроса</td>
                <td>Состояние</td>
                <td>ОПРОС</td>
                <td>УДАЛЕНИЕ</td>
            </tr>
    """)
    for current in base_counters:
        try:
            if(base_counters[current]['counter_type'] == "merc"):
                print("""
                        <tr>
                            <td>""" + base_counters[current]['label'] + """</td>
                            <td>""" + base_counters[current]['counter_type'] + """</td>
                            <td>""" + base_counters[current]['last']['energy'] + """</td>
                            <td>""" + base_counters[current]['last']['voltage1'] + """</td>
                            <td>""" + base_counters[current]['last']['voltage2'] + """</td>
                            <td>""" + base_counters[current]['last']['voltage3'] + """</td>
                            <td>""" + base_counters[current]['last']['current1'] + """</td>
                            <td>""" + base_counters[current]['last']['current2'] + """</td>
                            <td>""" + base_counters[current]['last']['current3'] + """</td>
                            <td>""" + base_counters[current]['time'] + """</td>
                            <td>""" + base_counters[current]['owner'] + """</td>
                            <td><a href='/cgi-bin/monitor.py?action=opros&id=""" + str(current) + """'> ОПРОСИТЬ<a/></td>
                            <td><a href='/cgi-bin/monitor.py?action=del&id=""" + str(current) + """'> УДАЛИТЬ <BR><a/></td>
                        </tr>
                """)
                print("")
        except KeyError:
            print("Запись удалена<BR>")
    print("</table>")

def print_list_counters_tep(base_counters):
    print("""
        <table border=1>
            <BR>Счётчики тепла
            <tr>
                <td>Объект</td>
                <td>Тип счётчика</td>
                <td>G1</td>
                <td>G2</td>
                <td>G3</td>
                <td>P1</td>
                <td>P2</td>
                <td>t1</td>
                <td>t2</td>
                <td>dt</td>
                <td>t3</td>
                <td>tх</td>
                <td>tв</td>
                <td>Время опроса</td>
                <td>Состояние</td>
                <td>ОПРОС</td>
                <td>УДАЛЕНИЕ</td>
            </tr>
    """)
    for current in base_counters:
        try:
            if(base_counters[current]['counter_type'] == "spt943"):
                print("""
                        <tr>
                            <td>""" + base_counters[current]['label'] + """</td>
                            <td>""" + base_counters[current]['counter_type'] + """</td>
                            <td>G1</td>
                            <td>G2</td>
                            <td>G3</td>
                            <td>P1</td>
                            <td>P2</td>
                            <td>t1</td>
                            <td>t2</td>
                            <td>dt</td>
                            <td>t3</td>
                            <td>tх</td>
                            <td>tв</td>
                            <td>""" + base_counters[current]['time'] + """</td>
                            <td>""" + base_counters[current]['owner'] + """</td>
                            <td><a href='/cgi-bin/monitor.py?action=opros&id=""" + str(current) + """'> ОПРОСИТЬ<a/></td>
                            <td><a href='/cgi-bin/monitor.py?action=del&id=""" + str(current) + """'> УДАЛИТЬ <BR><a/></td>
                        </tr>
                """)
                print("")
        except KeyError:
            print("Запись удалена<BR>")
    print("</table>")







def add(base_counters):
    next_ = random.randint(1, 9999999999)
    print("Добавлена запись " + str(next_) + "<BR> ")
    """
    next_counter = {next_: {'label': label,
                            'ip': ip,
                            'port': port,
                            'counter_type': counter_type,
                            'nt': nt,
                            'sn': 'Нет данных',
                            'energy': 'Нет данных',
                            'voltage1': 'Нет данных',
                            'voltage2': 'Нет данных',
                            'voltage3': 'Нет данных',
                            'current1': 'Нет данных',
                            'current2': 'Нет данных',
                            'current3': 'Нет данных',
                            'time': 'Нет данных',
                            'owner':'Нет данных'
                            }}
    """
    next_counter = {next_: {'label': label,
                            'ip': ip,
                            'port': port,
                            'counter_type': counter_type,
                            'nt': nt,
                            'sn': 'Нет данных',
                            'last':{'energy':'',
                                    'voltage1':'',
                                    'voltage2': '',
                                    'voltage3': '',
                                    'current1': '',
                                    'current2': '',
                                    'current3': ''},
                            'times':{},
                            'time': 'Нет данных',
                            'owner': 'Нет данных'
                            }}
    base_counters.update(next_counter)
    save_bd(base_counters)

form = cgi.FieldStorage()
ip = form.getfirst("ip", "none")
port = form.getfirst("port", "4001")
counter_type = form.getfirst("counter_type", "none")
nt = form.getfirst("nt", "none")
label = form.getfirst("label", "none")
action = form.getfirst("action", "none")
id = form.getfirst("id", "none")
print("Content-type: text/html\n")

def header():
    print("""<!DOCTYPE HTML>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Проверка счётчиков</title>
        </head>
        <body>
            <center>
            <H1>Проверка приборов учёта</H1><BR>
            <a href='/cgi-bin/monitor.py?action=monitor_page'> Мониторинг </a>
            <a href='/cgi-bin/monitor.py?action=data_page'> Показания </a>
            <a href='/cgi-bin/monitor.py?action=add_page'> Добавление </a>
            <a href='/cgi-bin/monitor.py?action=test_page'> Тест </a>
            <a href='/cgi-bin/monitor.py?action=report'> Отчёты </a><BR>""")

def add_new_form():
    print("""

            <form action="/cgi-bin/monitor.py">
                <input type="hidden" name="action" value="add">
                Добавление нового счётчика
                <table border=1>
                    <tr>
                        <td>Адрес:
                             <input type="text" name="label" value='""" + label + """'><BR>
                        </td>
                        <td>IP:
                             <input type="text" name="ip" value='""" + ip + """'><BR>
                        </td>
                        <td>
                            Порт счётчика:
                            <input type="text" name="port" value='""" + port + """'><BR>
                        </td>
                        <td align="center">
                            <select size="3" multiple name="counter_type">
                                <option disabled>Выберите тип</option>
                                <option  value="spt943">СПТ943</option>
                                <option selected value="merc">Меркурий</option>
                            </select><BR>
                        </td>
                        <td>
                            Сетевой номер(NT):
                            <input type="text" name="nt" value='""" + str(nt) + """'><BR>
                            <input type="submit" value="Добавить">
                        </td>
                    </tr>
            </form>""")
header()

base_counters = read_bd()
if action == "add":
    add(base_counters)
elif action == "add_page":
    add_new_form()
elif action == "del":
    pop_bd(int(id))
elif action == "opros":
    put_to_base(int(id), base_counters)
elif action == 'report':
    bd = read_bd()
    make_report(bd)
    print("<a href='../output.xls'>Скачать отчёт</a>")
elif action == 'monitor_page':
    base_counters = read_bd()
elif action == 'test_page':
    print(base_counters)
#print_monitoring(base_counters)
print_list_counters_el(base_counters)
print_list_counters_tep(base_counters)