#! /usr/env/bin python3

#This is going to be for PART A of question 2

"""
Steps to complete
    1. Factors n
    2. Completes Euliers of n -- this should be stored as a temp variable for later use
    3. Selects the smallest possible e w/ the following conditions
        e > 1
        gcd(e, eulier(n)) = 1

    4. Computes the private exponent via Extended Euclid Algo
        d = e^(-1) (mod (eulier(n))) -> store d as a temp variable  you are going to use this later

    5. Signs x
        s = (x^d) mod n -> Save s as temp variable -> use s for verification
    
    6. Signature verification baby
        (s^e) mod n = x mod n
"""

import math

n = 11111
x = 1234 

def factorize(n):
    #Since n is small, I am going to do simple trial division
    for pee in range(2, (int(math.isqrt(n)) + 1)):
        if n % pee == 0:
            return pee, n // pee
        
    return None, None #if there is no factorization

def extended_gcd(a, b):
    if b == 0: 
        return (1, 0, a)
    
    mister, pee, air = extended_gcd(b, a % b) #recursive call
    poo = pee
    peepee = mister - (a // b) * pee

    return (poo, peepee, air)

def modular_inverse(a, m):
    mister, pee, air = extended_gcd(a, m)

    if air != 1:
        raise ValueError(f"No modular inverse for {a} mod {m} (gcd = {air})")
    
    return mister % m

if __name__ == "__main__":
    #factoring n
    pee, poo = factorize(n)
    if pee is None:
            raise SystemExit(f"Could not factor {n}. {n} may be prime or too large.")
    
    print(f"n = {n} factors as p = {pee} and q = {poo}") #printing so transferring to HW submission is easier

    #Complete eulier's phi of n
    peepee = (pee - 1) * (poo - 1)
    print(f"phi(n) = {peepee}")

    #Find the smallest value of e when e > 1 and gcd(e, phi) = 1
    CharlieKirk = None
    for ahhhhhhh in range(2, peepee):
        if math.gcd(ahhhhhhh, peepee) == 1:
            CharlieKirk = ahhhhhhh
            break

    if CharlieKirk is None:
        raise SystemExit(f"There was no value of e found")
    
    print(f"Chosen public exponent e = {CharlieKirk}")

    # compute the private exponent, d
    poopoo = modular_inverse(CharlieKirk, peepee)
    print(f"Private Exponent d = {poopoo}")

    #Compute the signnature
    iLoatheOpeningShifts = pow(x, poopoo, n)
    print(f"Signature s = {iLoatheOpeningShifts}")

    #Verification
    BigMoney = pow(iLoatheOpeningShifts, CharlieKirk, n)
    print(f"Verification (s^e) mod n = {BigMoney} (expected value: {x % n})\t\t{"Key is correct" if BigMoney == (x % n) else "Key is incorrect"}")
