number_of_atoms = int(input())
final_quantity = int(input())

counter = 0
while number_of_atoms >= final_quantity:
    number_of_atoms /= 2
    counter += 1

print(counter * 12)
