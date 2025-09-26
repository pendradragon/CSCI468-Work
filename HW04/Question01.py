# S1 box definition (4 rows × 16 cols)
S1 = [
    [14, 4, 13, 1,  2, 15, 11, 8,  3, 10,  6, 12,  5,  9,  0,  7],
    [ 0,15,  7, 4, 14,  2, 13, 1, 10,  6, 12, 11,  9,  5,  3,  8],
    [ 4, 1, 14, 8, 13,  6,  2,11, 15, 12,  9,  7,  3, 10,  5,  0],
    [15,12,  8, 2,  4,  9,  1, 7,  5, 11,  3, 14, 10,  0,  6, 13]
]

def s1_lookup(x):
    """Takes the specified value of x (6-bits long)
         returns 4-bit integer output from S1
    """
    
    b5 = (x >> 5) & 1 #sixth bit of x
    b4 = (x >> 4) & 1 #fifth bit of x
    b3 = (x >> 3) & 1 #fourth bit of c
    b2 = (x >> 2) & 1 #third bit of x
    b1 = (x >> 1) & 1 #secon bit of x
    b0 = x & 1 #first bit of x

    row = (b5 << 1) | b0       # outer bits
    col = (b4 << 3) | (b3 << 2) | (b2 << 1) | b1  # inner 4 bits
    return S1[row][col]

def bits(n, width):
    """How to format the strings
        Ensure that the numbers are being compared correctly -- they are in the same format during comparison
    """
    return format(n, f'0{width}b')

def XORFunction(x1, x2):
    y1 = s1_lookup(x1)
    y2 = s1_lookup(x2)
    lhs = y1 ^ y2
    rhs = s1_lookup(x1 ^ x2)

    print(f"x1={bits(x1,6)}, x2={bits(x2,6)}")
    print(f"S1(x1)={bits(y1,4)}, S1(x2)={bits(y2,4)}")
    print(f"S1(x1) XOR S1(x2)={bits(lhs,4)}")
    print(f"x1 XOR x2={bits(x1^x2,6)}, S1(x1 XOR x2)={bits(rhs,4)}")
    
    print("-"*50) #using to tell the pieces of the assignment apart

if __name__ == "__main__":
    """"Testing the Cases in parts A, B, and C
        x syntax: 0b<6 values of x in assigment>
    """
    pairs = [
        (0b000000, 0b000001), #part a
        (0b111111, 0b100000), #part b
        (0b101010, 0b010101) #part c
    ]
    for x1, x2 in pairs:
        XORFunction(x1, x2)
