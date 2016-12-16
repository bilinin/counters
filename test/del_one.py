import  pickle
## Чтение структкры из файла
input = open('data.pkl', 'rb')
#input = open('data.pkl', 'rb')
base_counters = pickle.load(input)
input.close()
print(base_counters)

base_counters.pop(2)


# Консервация в файл
output = open('data.pkl', 'wb')
pickle.dump(base_counters, output, 4)
output.close()