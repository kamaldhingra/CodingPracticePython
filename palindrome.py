str1 = "kayyaka"
str2 = "akayyak"

if len(str1) != len(str2):
    print("Not Palindrome")
    exit(0)


""" With using loop"""
for i in range(int(len(str1)/2)):
    if str1[i] != str2[-i-1]:
        print("Not Palindrome")
        break
else:
    print("Palindrome -  With Loop")


""" Without using loop"""
strev = str2[::-1]
if str1 == strev:
    print("Palindrome - With Slice")
else:
    print("Not Palindrome - With Slice")
