#!/usr/bin/env python3

"""Use the SQUARE AND MULTIPLY ALGO
    Steps: 
        1. Convert e to binary form
            1.1 Can be done w/ the built in bin() function
        2. Initalize result to 1
        3. Iterate through each bit of e go from the most significant bit to least significant
            3.1 If the CURRENT BIT == 1, multiply the result by x
        4. Reduce by modulo m
"""

def square_and_multiply(x, e, m):
    binary_e = bin(e)[2:] #binary version of e

    pee = 1 # temp variable that is going to hold the value of (x^poo) mod m
    poo = 0 #the exponent value that is used 

    for bit in binary_e:
        #square step -- should always be done
        pee = (pee ** 2) % m
        poo = pee * 2

        #printing after every iteration step to make my life easier when transferring to paper
        print("\tSquare Step:")
        print(f"\t\tSquared bit: {bit}")
        print( f"\t\tExponent (in binary): {bin(poo)[2:]}")
        print(f"\t\tResult of the square: {pee}")

        #Multiply step -- should only be done when bit == 1
        if (bit == '1'):
            pee = (pee * x) % m
            poo = poo + 1

            #printing after every iteration
            print("\tMultiplication Step:")
            print(f"\t\tMultiplied Bit: {bit}")
            print(f"\t\tMultiplication Result: {pee}")

    print(f"***Final Result***\t {x}^{e} mod {m} = {pee}")    

if __name__ == "__main__":
    values = [(2, 79, 101), (3, 197, 101), (5, 54, 151), (8, 127, 151)]

    for (x, e, m) in values:
        print(f"When x = {x}, e = {e}, m = {m}") #to keep which problem I'm on separate, I will forget
        square_and_multiply(x, e, m)