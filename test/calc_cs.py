#10 FF 3F 00 00 00 00
def calc_cs(data):
    data_byte = bytearray.fromhex(data)
    byte_sum = 0
    for by in data_byte:
        byte_sum += by
    result = hex(0xFF^byte_sum)
    result = result[len(result)-2:len(result)]
    return "10 " + data + " " + result+" 16"



data = "01 42 02 00 00 00"
print(calc_cs(data))



data = b'\x10\x01?T+\x03=\x16'

