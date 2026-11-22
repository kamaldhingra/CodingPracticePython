str = "python for ai programming"

char_dict = {}

for ch in str:
    if char_dict.get(ch):
        char_dict[ch] = char_dict[ch] + 1
    else:
        char_dict[ch] = 1

print(char_dict)