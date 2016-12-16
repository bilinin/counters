from datetime import datetime

test_variable = b'\x00\x9f\x01\x96\xf1\xff\xff\xff\xff\x01\x00(E\xff\xff\xff\xffS\xb4'
original = test_variable[1:5]

def get_merc_energy(original):
    norm = bytes([c for t in zip(original[1::2], original[::2]) for c in t])
    return (int.from_bytes(norm,byteorder='big')/100)

print(str(test_variable))

now_time = datetime.now()

print(now_time)
