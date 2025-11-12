#!/usr/bin/env python3
import math #provides gcd function

# Includes answers for parts A-C

"""
Fermants Little Theorem (FLT)
    n must be prime

Euler's Theorem
    n and a are COPRIMES -- no common factors between a and n
        Need a gcd function to verify co-primes


gcd(n,a) =/= 1 -> a and n are NOT co-primes -> FLT
gcd(n,a) = 1 -> a and n ARE co-primes -> Euler's
"""

def euler_totient(n):
    poo = 0 #temp storage variable

    for i in range (1, n):
        if (math.gcd(i, n) == 1): #gcd(i,n) = coprimes
            poo += 1
        #if gcd(i, n) =/= -- not coprimes (no nothing)

    return poo

def prime_question_mark(n):

    """
    Boolean Function
        True = numbers are prime
        False = numbers NOT prime
    """

    if n < 2: 
        return False
    
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0: 
            return False
        
    return True

        
def modular_inverse(a, n):
    #if there's no modular invese -- stop
    if math.gcd(a, n) != 1: #there exists no modular inverse
        return None
    
    #fermant's theorem only works on prime numbers
    if prime_question_mark(n): #if returns True
        return pow(a, (n-2), n)
    else: #not prime overall
        poopoo = euler_totient(n)
        return pow(a, (poopoo - 1), n)


if __name__ == "__main__":
    """
        Part a: a = 4, n = 7
        Part b: a = 5, n = 12
        Part c: a = 6, n = 13
    """
    values = [(4, 7), (5, 12), (6, 13)]

    for (a, n) in values:
        inverse = modular_inverse(a, n)
        print(f"When a = {a} and n = {n}: inverse (a^(-1)) mod n = {inverse}")