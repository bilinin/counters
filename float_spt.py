#from base import *


# Поправить обязательно потерянный ноль костыль на костыле писалось ночью ((((
def float_from_byte(current):
    current.reverse()
    oder =  current[0] - 127
    current = current[1:]
    mantiss = ''
    for i,curr_byte in enumerate(current):
        curr_mantis = bin(curr_byte)[2:]
        while(len(curr_mantis ) < 8):
            curr_mantis =  '0' + curr_mantis
        mantiss += curr_mantis
    mantiss = '1'+mantiss[1:]
    res = 0
    for i,cur in enumerate(mantiss):
        if int(cur) == 1:
            res = res + 2**(-i)
    res = res * (2**oder)
    return res
