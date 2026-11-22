def get_permutations(s):
    # Base case: if string is empty or has one character
    if len(s) <= 1:
        return [s]
    result = []
    # Loop through each character in the string
    for i in range(len(s)):
        # Pick one character
        char = s[i]
        # Get the remaining characters
        remaining = s[:i] + s[i+1:]
        # Recursively get permutations of the remaining string
        for perm in get_permutations(remaining):
            result.append(char + perm)
    return result

# Example usage
perms = get_permutations("abcd")
for p in perms:
    print(p)