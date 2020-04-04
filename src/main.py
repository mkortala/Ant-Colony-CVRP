from src.data_reader import read_data

path = './data_set_1.xlsx'

example_instance = read_data(path)

print(example_instance.demands)
print(example_instance.costs)
