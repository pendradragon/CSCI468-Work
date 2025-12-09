from math import gcd

def phi(n):
    """Compute Euler's Totient function φ(n)"""
    result = n
    p = 2
    while p * p <= n:
        #Findings a prime number
        if n % p == 0:
            # The number is prrime
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result

# Given numbers
numbers = [928, 929, 932, 933, 934, 935, 936]

for n in numbers:
    print(f"phi({n}) = {phi(n)}")
