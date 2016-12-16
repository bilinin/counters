
from socket import *
def get_t_12(HOST,PORT):
    ADDR = (HOST, PORT)
    BUFSIZE = 1
    client = socket(AF_INET, SOCK_STREAM)
    try:
        client.connect((ADDR))
        client.send(b'0x0D')
        data = client.recv(BUFSIZE)
        #data = 'Подключено'
        client.close()
    except TimeoutError:
        data = 'Нет подключения'
    return data

data = get_t_12('92.127.157.209',4001)
print(data)