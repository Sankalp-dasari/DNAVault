# AES ENCRYPTION AND DECRYPTION

import numpy as np  # Python library for matrix mulitplication and mathematical calculations

"""
AES Class for Encrypting and Decrypting Data.

This implementation performs AES-128 bit block cipher encryption and decryption, 
where each state is represented as a 4x4 matrix of 8-bit binary strings.

This class uses:
- SubBytes
- ShiftRows
- MixColumns
- AddRoundKey
- Key Expansion (to generate round keys)

Integration with Kyber (Post-Quantum Cryptography) is also demonstrated to replace 
the AES round key with a key generated via a quantum-secure key exchange."""
class Encryption:
    def __init__(self, plaintext):
        self.plaintext = plaintext
        self.current_state = plaintext.copy()  # Track current state

        # Standard AES S-box (Substitution Box) for the Substitution Bytes step
        self.s_box_hex = [
            [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76],
            [0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0],
            [0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15],
            [0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75],
            [0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84],
            [0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF],
            [0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8],
            [0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2],
            [0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73],
            [0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB],
            [0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79],
            [0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08],
            [0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A],
            [0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E],
            [0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF],
            [0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16]
        ]

        # Convert S-box hex values to 8-bit binary strings
        self.s_box = np.empty((16, 16), dtype=object)
        for i in range(16):
            for j in range(16):
                self.s_box[i, j] = format(self.s_box_hex[i][j], '08b')

        # Inverse S-box for decryption
        self.inv_s_box_hex = [
            [0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB],
            [0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB],
            [0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E],
            [0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25],
            [0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92],
            [0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84],
            [0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06],
            [0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B],
            [0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73],
            [0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E],
            [0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B],
            [0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4],
            [0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F],
            [0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF],
            [0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61],
            [0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D]
        ]

        # Convert inverse S-box to binary strings
        self.inv_s_box = np.empty((16, 16), dtype=object)
        for i in range(16):
            for j in range(16):
                self.inv_s_box[i, j] = format(self.inv_s_box_hex[i][j], '08b')

        # Pre-defined Matrix for the Mix Column Step
        self.pre_defined = np.array([
            [0x02, 0x03, 0x01, 0x01],
            [0x01, 0x02, 0x03, 0x01],
            [0x01, 0x01, 0x02, 0x03],
            [0x03, 0x01, 0x01, 0x02]
        ])

        # Inverse Mix Columns matrix for decryption
        self.inv_pre_defined = np.array([
            [0x0E, 0x0B, 0x0D, 0x09],
            [0x09, 0x0E, 0x0B, 0x0D],
            [0x0D, 0x09, 0x0E, 0x0B],
            [0x0B, 0x0D, 0x09, 0x0E]
        ])
        
        # Initial Round key for encryption (Could be replaced for Kyber
        self.round_key = np.array([
            ['10101100', '01110111', '01100110', '11110011'],
            ['00011001', '11111010', '11011100', '00100001'],
            ['00101000', '11010001', '00101001', '01000001'],
            ['01010111', '01011100', '00000000', '01101010']
        ])

        # Store all round keys
        self.list_of_round_keys = []

        # Add the initial round key to the list of round keys
        self.list_of_round_keys.append(self.round_key)


        # Round Constants used in Key Expansion
        self.round_const = np.array([
            ['00000001', '00000000', '00000000', '00000000'],
            ['00000010', '00000000', '00000000', '00000000'],
            ['00000100', '00000000', '00000000', '00000000'],
            ['00001000', '00000000', '00000000', '00000000'],
            ['00010000', '00000000', '00000000', '00000000'],
            ['00100000', '00000000', '00000000', '00000000'],
            ['01000000', '00000000', '00000000', '00000000'],
            ['10000000', '00000000', '00000000', '00000000'],
            ['00011011', '00000000', '00000000', '00000000'],
            ['00110110', '00000000', '00000000', '00000000'],
            ['01101100', '00000000', '00000000', '00000000']
        ])

        # Keeps track of the round counter
        self.round_counter = 0

    
    def sub_bytes(self, state_array):
        """
        Byte Substitution using AES S-Box — Non-linear transformation
        """
        result = np.zeros_like(state_array) # Matrix to store the result
        rows, cols = state_array.shape # Dimensions of the state array
        
        # Iterate over all elements of the state arrat matrix
        for i in range(rows):
            for j in range(cols):
                byte = state_array[i, j] # Extract byte
                row_in_sbox = int(byte[:4], 2) # Store the row number
                col_in_sbox = int(byte[4:], 2) # Store the column number
                result[i, j] = self.s_box[row_in_sbox, col_in_sbox] # Insert the corresponding value from the S-Box into the result
        return result # Return the result

 
    def shift_rows(self, state_array):
        """
        Shift rows left by their row index
        1st row --> no shift
        2nd row --> circular left shift by one
        3rd row --> circular left shift by two
        4th row --> circular left shift by three
        """   
        shifted_rows = state_array.copy() # Copy of the state array
        rows, cols = state_array.shape # Dimensions of the state array

        # Iterate through the rows
        for i in range(rows):
            shifted_rows[i] = np.roll(state_array[i], shift=(-1 * i)) # Shift each row by their row index
        return shifted_rows # Return the shifted matrix


    def gf_multiply(self, a, b):
        """
        Perform multiplication in Galois Field GF(2^8)

        This function performs the multiplication of two bytes (a and b) in GF(2^8)
        following the Russian Peasant Multiplication method combined with modular reduction.
        """

        result = 0 # Initialize the result to 0

        while b:
            if b & 1: 
                result ^= a # Addition in GF(2^8) is XOR
            if a & 0x80: # If the highest bit (8th bit) of a is 1, overflow occurs
                a = (a << 1) ^ 0x1b # Shift left and reduce modulo 0x11b
            else:
                a <<= 1  # If no overflow, simple left shift by 1
            # Move to the next bit of b
            b >>= 1 # Shift b right by 1 to process the next bit
        return result & 0xff 


    def mix_columns(self, shifted_rows):
        """
        MixColumns step — Linear mixing of bytes within each column
        """
        # Convert binary strings to integers
        int_matrix = np.zeros((4, 4), dtype=np.uint8)
        for i in range(4):
            for j in range(4):
                int_matrix[i, j] = int(shifted_rows[i, j], 2)
        
        result = np.zeros((4, 4), dtype=np.uint8)
        
        # Apply MixColumns transformation
        for col in range(4):
            column = int_matrix[:, col]
            for row in range(4):
                result[row, col] = (
                    self.gf_multiply(self.pre_defined[row, 0], column[0]) ^
                    self.gf_multiply(self.pre_defined[row, 1], column[1]) ^
                    self.gf_multiply(self.pre_defined[row, 2], column[2]) ^
                    self.gf_multiply(self.pre_defined[row, 3], column[3])
                )
        
        # Convert back to binary strings
        mixed_columns = np.empty((4, 4), dtype=object)
        for i in range(4):
            for j in range(4):
                mixed_columns[i, j] = format(result[i, j], '08b')
        return mixed_columns
    

    def key_expansion(self, counter):
        """
        Apply Key Expansion

        Expand round keys for AES.
            - RotWord: Rotate last word
            - SubWord: Substitute using S-box
            - XOR with previous word and Rcon
        """

        # Extract 4 words
        wa = self.list_of_round_keys[counter][:, 0]
        wb = self.list_of_round_keys[counter][:, 1]
        wc = self.list_of_round_keys[counter][:, 2]
        wd = self.list_of_round_keys[counter][:, 3]
        
        temp = wd # Keep the value of original value
        
        # Left Shift
        wd = np.roll(wd, shift=-1)
        
        # Sub Bytes
        for i in range(len(wd)):
            row_in_sbox = int(wd[i][:4], 2)
            col_in_sbox = int(wd[i][4:], 2)
            wd[i] = self.s_box[row_in_sbox, col_in_sbox]


        # XOR with Round Constant
        RC = self.round_const[counter]
        wd = np.array([int(x, 2) for x in wd], dtype=np.uint8)
        RC = np.array([int(x, 2) for x in RC], dtype=np.uint8)
        wd = wd ^ RC

        # Set new Words

        # Convert to integers for performing XOR operation
        wa = np.array([int(x, 2) for x in wa], dtype=np.uint8)
        wb = np.array([int(x, 2) for x in wb], dtype=np.uint8)
        wc = np.array([int(x, 2) for x in wc], dtype=np.uint8)
        temp = np.array([int(x, 2) for x in temp], dtype=np.uint8)

        wa = wa ^ wd
        wb = wb ^ wa
        wc = wc ^ wb
        wd = temp ^ wc

        # Convert back to bitstrings
        wa = np.array([format(x, '08b') for x in wa], dtype=object)
        wb = np.array([format(x, '08b') for x in wb], dtype=object)
        wc = np.array([format(x, '08b') for x in wc], dtype=object)
        wd = np.array([format(x, '08b') for x in wd], dtype=object)

        # Generate 4 4x1 column matrices
        wa = np.transpose(wa)
        wb = np.transpose(wb)
        wc = np.transpose(wc)
        wd = np.transpose(wd)

        # Stack all 4x1 column matrices into a 4x4 matrix (round key)
        new_round_key = np.column_stack((wa, wb, wc, wd))

        # Add new key to list of round keys
        self.list_of_round_keys.append(new_round_key)


    def add_round_key(self, state_array, round_num=None):
        """
        Apply Round Key Transformation
        XOR the state with the round key
        """
        rows, cols = state_array.shape # Obtain size of matrix
        result = np.empty_like(state_array) # Result matrix to store output of function
        
        # If this is the initial round, then use the initial round key, else use the round key
        # from the list for corresponding round
        if round_num is None:
            round_key = self.list_of_round_keys[self.round_counter]
            self.round_counter += 1
        else:
            round_key = self.list_of_round_keys[round_num]

        # Perform XOR operation
        for i in range(rows):
            for j in range(cols):
                byte1 = int(state_array[i, j], 2) # Extract byte in the form of integer
                byte2 = int(round_key[i, j], 2) # Extract byte in the form of integer
                xor_result = byte1 ^ byte2 # XOR The operation
                result[i, j] = format(xor_result, '08b') # Convert back to bitstring

        return result
    

    def encrypt(self):
        """
        Perform AES-128 Encryption on a 4x4 plaintext state matrix.
        The AES encryption algorithm transforms a plaintext block into a ciphertext block
        """
        self.round_counter = 0 # Set the round counter to 0
        state = self.plaintext.copy() # Create a copy of the plaintext

        # Generate all the round keys using key expansion
        for i in range(10):
            enc.key_expansion(counter=i)

        self.round_counter = 0 # Reset the round counter for keeping track of number of rounds of encryption

        state = self.add_round_key(state) # Add the initial round key

        # Perform 10 rounds of encryption
        for round_num in range(1, 10):
            state = self.sub_bytes(state)
            state = self.shift_rows(state)
            state = self.mix_columns(state)
            state = self.add_round_key(state)

        # Perform the last round of encryption (all steps except mix columns)
        state = self.sub_bytes(state)
        state = self.shift_rows(state)
        state = self.add_round_key(state)

        return state

    # ===================== DECRYPTION METHODS =====================

    def inv_sub_bytes(self, state_array):
        """
        Apply Inverse SubBytes transformation.
        Each byte in the state matrix is replaced using the inverse S-Box (InvS-Box).
        """
        result = np.zeros_like(state_array) # Create an empty matrix to store result of function
        rows, cols = state_array.shape
        
        # Iterate over each byte in the state matrix
        for i in range(rows):
            for j in range(cols):
                byte = state_array[i, j] # Retrieve the byte
                row_in_sbox = int(byte[:4], 2) # Use first 4 bits for row index
                col_in_sbox = int(byte[4:], 2) # Use last 4 bits for column index
                result[i, j] = self.inv_s_box[row_in_sbox, col_in_sbox] # Substitute using inv_s_box
               
        return result

    def inv_shift_rows(self, state_array):
        """
        Apply Inverse ShiftRows transformation
        Reverses the ShiftRows step by cyclically shifting each row to the right
        by the row number
        """
        shifted_rows = state_array.copy()
        rows, cols = state_array.shape

        # Shift right instead of left (positive shift)
        for i in range(rows):
            shifted_rows[i] = np.roll(state_array[i], shift=i)
        
        return shifted_rows

    def inv_mix_columns(self, state_array):
        """
        Apply Inverse MixColumns transformation.
        Reverses the MixColumns step by multiplying each column of the state
        by the inverse MixColumns matrix over GF(2^8).
        """
        # Convert binary strings to integers
        int_matrix = np.zeros((4, 4), dtype=np.uint8)
        for i in range(4):
            for j in range(4):
                int_matrix[i, j] = int(state_array[i, j], 2)
        
        result = np.zeros((4, 4), dtype=np.uint8)
        
        # Apply Inverse MixColumns transformation
        for col in range(4):
            column = int_matrix[:, col]
            for row in range(4):
                result[row, col] = (
                    self.gf_multiply(self.inv_pre_defined[row, 0], column[0]) ^
                    self.gf_multiply(self.inv_pre_defined[row, 1], column[1]) ^
                    self.gf_multiply(self.inv_pre_defined[row, 2], column[2]) ^
                    self.gf_multiply(self.inv_pre_defined[row, 3], column[3])
                )
        
        # Convert back to binary strings
        inv_mixed_columns = np.empty((4, 4), dtype=object)
        for i in range(4):
            for j in range(4):
                inv_mixed_columns[i, j] = format(result[i, j], '08b')
        
        return inv_mixed_columns

    def decrypt(self, ciphertext):
        """
        Perform AES decryption on a ciphertext block.
        AES decryption involves applying the inverse transformations in the reverse order
        of the encryption process to recover the original plaintext.
        """
        state = ciphertext.copy()
        # Initial round: AddRoundKey with the last (10th) round key
        state = self.add_round_key(state, 10)

        # 9 full inverse rounds
        for round_num in range(9, 0, -1):
            state = self.inv_shift_rows(state)
            state = self.inv_sub_bytes(state)
            state = self.add_round_key(state, round_num)
            state = self.inv_mix_columns(state)

        # Final round (no MixColumns)
        state = self.inv_shift_rows(state)
        state = self.inv_sub_bytes(state)
        state = self.add_round_key(state, 0)

        return state

"""
TEST AES ENCRYPTION/DECRYPTION
"""
if __name__ == "__main__":

    # Define a plaintext 4x4 block as a matrix of 8-bit binary strings
    plaintext = np.array([
        ['11101010', '00000100', '01100101', '10000101'],
        ['10000011', '01000101', '01011101', '10010110'],
        ['01011100', '00110011', '10011000', '10110000'],
        ['11110000', '00101101', '10101101', '11000101']
    ])

    
    # Create encryption object
    enc = Encryption(plaintext)
    
    # Encrypt
    ciphertext = enc.encrypt()
    decrypted = enc.decrypt(ciphertext)
    
    # Verify
    print(f"Original Plaintext:\n{plaintext}\n")
    print(f"Final Ciphertext:\n{ciphertext}\n")
    print(f"Decrypted Text:\n{decrypted}\n") 
        

 # ====================== KYBER + AES INTEGRATION ======================
# Testcase for generating a Kyber key to replace the AES round key
from kyber import Kyber


# Instantiate Kyber and generate keys
kyber = Kyber()
A, s, pk = kyber.keygen()
(u, v), shared_key, m = kyber.encapsulate(pk, A)

# Generate a new round key matrix from Kyber key (first 16 bytes)
new_key_matrix = np.array([
    [format(byte, '08b') for byte in shared_key[i:i+4]]
    for i in range(0, 16, 4)
])

# Define plaintext for AES
plaintext = np.array([
    ['11101010', '00000100', '01100101', '10000101'],
    ['10000011', '01000101', '01011101', '10010110'],
    ['01011100', '00110011', '10011000', '10110000'],
    ['11110000', '00101101', '10101101', '11000101']
])

# Instantiate AES with plaintext
enc = Encryption(plaintext)

# Override round key with Kyber-derived key
enc.round_key = new_key_matrix
enc.list_of_round_keys = [new_key_matrix]  # reset round keys

# Encrypt
ciphertext = enc.encrypt()

# Decrypt
decrypted = enc.decrypt(ciphertext)
