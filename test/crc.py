def add_cs_spt(data,NT):
    data_byte = bytearray.fromhex(NT+data)
    byte_sum = 0
    for by in data_byte:
        byte_sum += by
    result = hex(0xFF^byte_sum)
    result = result[len(result)-2:len(result)]
    return "10 "+ NT + " " + data + " " + result+" 16"

print(add_cs_spt("12 12 12","01"))