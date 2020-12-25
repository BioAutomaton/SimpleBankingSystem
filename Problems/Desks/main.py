from math import ceil

students = [int(input()) for i in range(3)]

tables = 0
for group in students:
    tables += ceil(group / 2)

print(tables)
