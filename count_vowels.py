str = "python for ai programming"
vowels = ['a', 'e', 'i', 'o', 'u']
count = 0
for c in str:
    if c in vowels:
        print(c)
        count = count +1

print(count)