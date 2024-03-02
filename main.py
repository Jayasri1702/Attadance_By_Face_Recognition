M = '133457799BBCDFF1'   # the given hexadecimal format

# Convert hexadecimal to binary
key = bin(int(M, 16))[2:].zfill(64)

print("ORIGINAL 64 BIT KEY : ",key)   # Output: 0001001100110100010101111001100110011011101011101011111101110000


# 56-bit permutation table
pc1_table = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 
             59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36, 63, 55, 47, 39, 
             31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 
             29, 21, 13, 5, 28, 20, 12, 4]

# Apply the permutation
permuted_key = ''
for index in pc1_table:
    permuted_key += key[index-1]

print("56 BIT PERMUTATION : ",permuted_key)   # Output: 11110000110011001010101011110101010101100110011110001111


# Divide the key into two halves
left_half = permuted_key[:28]
right_half = permuted_key[28:]

# Define the shift table for each round
shift_table = {1: 1, 2: 1, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 8: 2, 9: 1, 10: 2, 11: 2, 12: 2, 13: 2, 14: 2, 15: 2, 16: 1}

# Perform circular left shifts on each half depending on the round
for i in range(1, 17):
    left_shifted = left_half[shift_table[i]:] + left_half[:shift_table[i]]
    right_shifted = right_half[shift_table[i]:] + right_half[:shift_table[i]]
    print(f"Round {i}: \nLeft half: {left_shifted},\n Right half: {right_shifted}")
 

# Combine the two halves
combined_key = left_half + right_half

# 48-bit permutation table for subkeys
pc2_table = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 
             26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40, 
             51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]

# Generate 16 subkeys
subkeys = []
for i in range(1, 17):
    # Determine the number of positions to shift each half
    if i in [1, 2, 9, 16]:
        shift_count = 1
    else:
        shift_count = 2
        
    # Perform circular left shift on each half
    left_shifted = left_half[shift_count:] + left_half[:shift_count]
    right_shifted = right_half[shift_count:] + right_half[:shift_count]
    
    # Combine the shifted halves
    combined_shifted = left_shifted + right_shifted
    
    # Apply the permutation 2 table
    subkey = ''
    for index in pc2_table:
        subkey += combined_shifted[index-1]
    
    subkeys.append(subkey)
    # Update the left and right halves for the next round
    left_half = left_shifted
    right_half = right_shifted
    

# Print the resulting subkeys
print(subkeys)

for i in range(16):
    # Get the current subkey
    subkey = subkeys[i]
    
    # Perform the XOR operation
    result = ''
    for j in range(len(left_shifted)):
        if left_shifted[j] != right_shifted[j] != subkey[j]:
            result += '1'
        else:
            result += '0'
    
    # Print the result for the current subkey
    print(f"K {i+1}: {result}")
    




