import pickle

def read_bd():
    # Чтение структкры из файла
    input = open('cgi-bin/data.pkl', 'rb')
    # input = open('data.pkl', 'rb')
    base_counters = pickle.load(input)
    input.close()
    return base_counters


def save_bd(base_counters):
    # Консервация в файл
    output = open('cgi-bin/data.pkl', 'wb')
    pickle.dump(base_counters, output, 4)
    output.close()


def pop_bd(id):
    base_counters = read_bd()
    base_counters.pop(id)
    save_bd(base_counters)
