import binascii

# Initial Permutation Table
INITIAL_PERMUTATION_TABLE = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

# PC-2 Permutation Table
PC_2_PERMUTATION_TABLE = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

# Number of Left Shifts for Each Round
LEFT_SHIFTS = [
    1, 1, 2, 2, 2, 2, 2, 2,
    1, 2, 2, 2, 2, 2, 2, 1
]

def permute(bits, permutation):
    return [bits[i-1] for i in permutation]

def circular_left_shift(bits, n):
    return bits[n:] + bits[:n]

def generate_subkeys(key):
   
    key = binascii.hexlify(key.encode())
    key = bin(int(key, 16))[2:].zfill(64)

    
    key = permute(key, INITIAL_PERMUTATION_TABLE)

    
    left_half = key[:32]
    right_half = key[32:]

    subkeys = []

    for i in range(16):
        
        left_half = circular_left_shift(left_half, LEFT_SHIFTS[i])
        right_half = circular_left_shift(right_half, LEFT_SHIFTS[i])

        
        combined_half = left_half + right_half
        subkey = permute(combined_half, PC_2_PERMUTATION_TABLE)

        subkeys.append(subkey)

    return subkeys

key = "0123456789ABCDEF"
subkeys = generate_subkeys(key)
for i, subkey in enumerate(subkeys):
    print("Subkey {}: {}".format(i+1, subkey))
