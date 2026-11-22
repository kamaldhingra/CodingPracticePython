str = "abcddefgghijklmnopppqqrrstuvvviuoo"

key = ""
char_dict = {}
i=0
while i<len(str)-1:
    key = ""
    for j in range(len(str[i: ])):
        cmp = str[i:][j]
        if cmp not in key:
            key = key+cmp
        else:
            break
    i = i + j
    char_dict[key] = len(key)

print(char_dict)
max_key =  max(char_dict , key = char_dict.get)
print(max_key)