str = "{{()}[({}[])]}"
#str = "{{()}[({}][)]}"
mapping = {
    "{":"}",
    "(":")",
    "[":"]"
}

stack = [str[0]]
i=1
while i < len(str):
    if mapping.get(stack[-1]) == str[i]:
        stack.pop()
    else:
        stack.append(str[i])
    i = i+1

if len(stack) == 0:
    print('Expression is correct')
else:
    print("Wrong Expression")
