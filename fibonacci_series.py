
"""It uses 3 variables"""
a=1
b=1

for i in range(6):
    temp = a+b
    print(temp)
    a=b
    b=temp
print('===================================')

"""It uses 2 variables"""
a=1
b=2
for i in range(6):
    print(b)
    b= b+a
    a= b-a