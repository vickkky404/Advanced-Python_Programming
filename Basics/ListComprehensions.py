# old method.
num = [1,2,3,4,5]
squared = []

for n in num:
    squared.append(n**2)



# new method using list comprehension.
squared = [n * 2 for n in num]
print(squared)