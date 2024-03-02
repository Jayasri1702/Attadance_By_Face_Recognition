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
 
print("")
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
    
print("")
# Print the resulting subkeys
print("SUBKEYS : " ,subkeys)



def apply_expansion_table(subkey):
    expansion_table = [
        31,  0,  1,  2,  3,  4,
         3,  4,  5,  6,  7,  8,
         7,  8,  9, 10, 11, 12,
        11, 12, 13, 14, 15, 16,
        15, 16, 17, 18, 19, 20,
        19, 20, 21, 22, 23, 24,
        23, 24, 25, 26, 27, 28,
        27, 28, 29, 30, 31,  0
    ]
    expanded_subkey = ''
    for index in expansion_table:
        expanded_subkey += subkey[index]
    return expanded_subkey

# Apply the expansion table to each subkey
expanded_subkeys = [apply_expansion_table(subkey) for subkey in subkeys]
print("")
# Print the result
print("APPLY EXPANSION TABLE FOR THE 16 SUBKEYS : ",  expanded_subkeys)


# Define the input lists
right_shifted = ['1010101011001100111100011110', '1010101011001100111100011110',
                 '0101010110011001111000111101', '0101010110011001111000111101',
                 '0101010110011001111000111101', '0101010110011001111000111101',
                 '0101010110011001111000111101', '0101010110011001111000111101',
                 '10101010110011001111000111101', '0101010110011001111000111101',
                 '0101010110011001111000111101', '0101010110011001111000111101',
                 '0101010110011001111000111101', '0101010110011001111000111101',
                 '0101010110011001111000111101','1010101011001100111100011110']

expanded_keys = ['000011110110100000000101011101011111111111111000',
                 '101111110011110101011101011011110011111011110110',
                 '001010101011111111111001010001010100001000000100',
                 '101110100101010101011011111010101101011011110110',
                 '101111111001011101011000000000001111111101010110',
                 '001100000111110100001010100111111100001010100000',
                 '011101011001010000001001010110101111111110101101',
                 '111110101111110001010100000111110101011000000011',
                 '111100000001011011110111111101010111111101011011',
                 '010110100011111110100110101000001111110111110101',
                 '000100000010101011111111111010100111111011111100',
                 '001110101010101110100011111110101011110010101000',
                 '010010101111111000001011111010100011111111110101',
                 '001011111110101000000111110110101111111110100100',
                 '110111111111110010100011110001011010100111111011',
                 '011001010110100111111011110001010110100001011101']

# Apply XOR operation on the corresponding elements of the lists
result = []
for i in range(len(right_shifted)):
    xor = ""
    for j in range(len(right_shifted[i])):
        if right_shifted[i][j] == expanded_keys[i][j]:
            xor += "0"
        else:
            xor += "1"
    result.append(xor)
print("")
# Print the result
print( " APPLYING XOR OPERATION : " ,result)

# Define the S-box table
S1= [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
         [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
         [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
         [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]]
 
S2=[[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
         [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
         [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
         [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]]

S3=[[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
         [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
         [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
         [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]]
 
S4=[[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
         [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
         [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
         [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]]
 
S5=[[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
         [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
         [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
         [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]]
 
S6=[[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
         [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
         [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
         [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]]
 
S7=[[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
         [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
         [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
         [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]]
 
S8=[[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
         [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
         [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
         [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]] 

# Define the S-box tables
S_BOX_TABLES = [S1, S2, S3, S4, S5, S6, S7, S8]

# Apply the S-box tables to the input binary strings
output = ''
for i in range(8):
    # Extract the current 6-bit block from the input string
    block = result[i*6:(i+1)*6]
    
    # Extract the row and column indices for the current S-box table
    row = int(block[0] + block[5], 2)
    col = int(block[1:17], 2)
    
    # Look up the value in the S-box table
    s_box_value = S_BOX_TABLES[i][row][col]
    
    # Convert the S-box value to binary and append it to the output string
    output += bin(s_box_value)[2:].zfill(4)

print(output)




