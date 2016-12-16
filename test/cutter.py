from socket import *
counter = socket(AF_INET, SOCK_STREAM)
app = socket(AF_INET, SOCK_STREAM)
HOST = '212.20.40.53'
PORT = 4002
ADDR = (HOST, PORT)
BUFSIZE = 1024  # Размер буфера
app.bind(('', 9090))
app.listen(1)

while(1):
    conn, addr = app.accept()
    print('connected:', addr)
    while(True):
        client = socket(AF_INET, SOCK_STREAM)
        client.settimeout(1)
        client.connect(ADDR)
        app_data = conn.recv(1024)
        if app_data == b'':
            break
        print("from_app " + str(app_data))
        client.send(app_data)
        data = client.recv(BUFSIZE)
#Костыли
        count = 0
        if data.find(b'\xff\xff', 0, 2) != -1:
            print("cut " + str(data))
            data = client.recv(BUFSIZE)
#Буфферизация
        if data.find(b'\x01', 0, len(data)) != -1:
            flag = True
            while(flag):
                try:
                    data = data + client.recv(BUFSIZE)
                    count += 1
                except:
                    print("last packet")
                    flag = False
#
        print("packets = "+str(count)+" length " + str(len(data)))
        print("from_counter " + str(data))
        conn.send(data)
        client.close()



