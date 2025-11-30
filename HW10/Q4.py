"""
Things to write:
    Square and multiply algorithm (I think I'm going to pull this from a previous HW)

    EEA (used to compute the INVERSE) -- used in decryption

    Elgamal Encryption 

    Elgamal Decryption
"""

#!/usr/bin/env python3

#square and multiply -- I'm just going to pull this from HW#9 Question 2
def square_n_multiply(x, e, m):
    binary_e = bin(e)[2:] #binary version of e
    
    pee = 1 # temp variable that is going to hold the value of (x^poo) mod m
    poo = 0 #the exponent value that is used 

    for bit in binary_e:
        #square step -- should always be done
        pee = (pee ** 2) % m
        poo = pee * 2

        """#printing after every iteration step to make my life easier when transferring to paper
        print("\tSquare Step:")
        print(f"\t\tSquared bit: {bit}")
        print( f"\t\tExponent (in binary): {bin(poo)[2:]}")
        print(f"\t\tResult of the square: {pee}")"""

        #Multiply step -- should only be done when bit == 1
        if (bit == '1'):
            pee = (pee * x) % m
            poo = poo + 1

            """#printing after every iteration
            print("\tMultiplication Step:")
            print(f"\t\tMultiplied Bit: {bit}")
            print(f"\t\tMultiplication Result: {pee}")"""

    print(f"\t\t***Square and Multiply Result***\t {x}^{e} mod {m} = {pee}")
    return pee

#modular inverse algo
def mod_inv(a, m):
    print(f"\t\tFinding the modular inverse of {a} mod {m}.")
    pee_old, pee = a, m #temp storage variables
    poo_old, poo = 1, 0
    tp_old, tp = 0, 1

    #Euclidian steps
    while pee != 0:
        q = pee_old // pee
        
        pee_old, pee = pee, pee_old - q * pee
        poo_old, poo = poo, poo_old - q * poo
        tp_old, tp = tp, tp_old - q * tp

    if pee_old != 1: 
        raise ValueError("No modular inverse exists!")
    

    inverse = poo_old % m
    print(f"\t\tModular inverse of {a} mod {m} is {inverse}")
    return inverse

#Elgamal Encryption
def elgamal_encrypt(p, alpha, beta, x, i):
    print("\t===ENCRYPTION===")

    pee = square_n_multiply(alpha, i, p)
    poo = square_n_multiply(beta, i, p)
    peepee = (x * poo) % p

    print(f"\t\tgamma = alpha^i mod p = {pee}")
    print(f"\t\ts = beta^i mod p = {poo}")
    print(f"\t\tdelta = x * s mod p = {peepee}")
    print(f"\t\tCiphertext = ({pee}, {peepee})")

    return pee, peepee

#Elgamal Decryption 
def elgamal_decrypt(p, d, gamma, delta):
    print(f"\t===DECRYPTION===")

    #compute (gamma)^d mod p
    pee = square_n_multiply(gamma, d, p)

    #Compute the inverse of p
    pee_inverse = mod_inv(pee, p)

    #Find the plaintext
    poo = (delta * pee_inverse) % p

    print(f"\t\tRecoveed plaintext = {poo}")

    return poo

if __name__ == "__main__":
    p = 467
    alpha = 2

    problems = [("a.", 105, 213, 33), ("b.", 105, 123, 33), ("c.", 300, 45, 248), ("d.", 300, 47, 248),]

    for problem, mister, pee, air in problems:
        print(f"PROBLEM {problem}: d = {mister}, i = {pee}, x = {air}")

        #compute the public key -- done via alpha^d mod p
        poo = square_n_multiply(alpha, mister, p)
        print(f"\tPublic Key beta = {poo}")

        #Encryption
        peepee, poopoo = elgamal_encrypt(p, alpha, poo, air, pee)
        #Decyrption
        plaintext = elgamal_decrypt(p, mister, peepee, poopoo)
        print(f"\t***Final plaintext x = {plaintext}***")        