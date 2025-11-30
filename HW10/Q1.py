"""
Public Key Computation
    Pub Key #1: 
        alpha^a mod p
    
    Pub Key #2:
        alpha^b mod p

Joint Diffe
    (Pub Key #2)^a mod p
    (Pub Key #1)^b mod p
"""
#!/usr/bin/env python3

def dhke(p, alpha, a, b):
    #compute the public key
    pee = pow(alpha, a, p)
    poo = pow(alpha, b, p)

    poopoo = pow(poo, a, p)
    peepee = pow(pee, b, p)

    return pee, poo, poopoo, peepee

if __name__ == "__main__":
    # defined by the given problem
    p = 467
    alpha = 2

    problems = [ ("a.", 3, 5), ("b.", 400, 134), ("c.", 228, 57),]

    for problem, a, b in problems: #print the label and everything to make transfer to pape easier
        print(f"{problem} a = {a} b = {b}")
        pee, poo, poopoo, peepee = dhke(p, alpha, a, b)
        print(f"\t Public Key A = (alpha^a) mod p = {pee}")
        print(f"\t Public Key B = (alpha^b) mod p = {poo}")
        print(f"\t Shared Key (B^a) mod p = {poopoo}")
        print(f"\t Shared Key (A^b) mod p = {peepee}")
        print(f"\t Keys Match? {'YES' if poopoo == peepee else 'NO'}")
