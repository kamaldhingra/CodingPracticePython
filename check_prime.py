def is_prime(num):
    if num <= 1:
        return False
    print((num**0.5)+1)
    for i in range(2, int(num ** 0.5) + 1):
        print(i)
        if num % i == 0:
            return False
    return True


numb = 131
print(is_prime(numb))