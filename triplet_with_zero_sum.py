input = [2,5,-6, 4,-3 ,1]
result = []
for i in range(len(input)-2):
    first = input[i]
    for k  in range(i+1, len(input)-1):
        second = input[k]
        for j in range (k+1, len(input)):
            temp = input[j]
            if first + second +temp == 0:
                comb = [first,second,temp]
                result.append(comb)
print('Triplet with Sum Zero',result)
