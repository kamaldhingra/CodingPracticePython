num = 23506005
temp = num
sum=0
while(temp !=0):
    sum = sum + int(temp % 10)
    if temp!=0:
        temp = int(temp/10)
    print(temp)



print(sum)