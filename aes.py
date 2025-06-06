# class AES:
# Implements AES encryption and decryption from scratch.

import numpy as np # Imported for Matrix Calculation

class Encryption:
    def __init__(self, plaintext):

        self.plaintext = plaintext

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

        
        # Convert to binary strings
        self.s_box = np.empty((16, 16), dtype=object)
        for i in range(16):
            for j in range(16):
                self.s_box[i, j] = format(self.s_box_hex[i][j], '08b')

        # Pre-defined Matrix for the Mix Column Step
        self.pre_defined = np.array([
            [0x02, 0x03, 0x01, 0x01],
            [0x01, 0x02, 0x03, 0x01],
            [0x01, 0x01, 0x02, 0x03],
            [0x03, 0x01, 0x01, 0x02]
        ])
        
        # Round Key
        self.round = np.array([
            ['10101100', '00011001', '00101000', '01010111'],
            ['01110111', '11111010', '11010001', '01011100'],
            ['01100110', '11011100', '00101001', '00000000'],
            ['11110011', '00100001', '01000001', '01101010']
        ])

    # Return State Array
    def sub_bytes(self):

        # Set up a zero matrix of the size of plaintext
        state_array = np.zeros_like(self.plaintext)
        
        # Get dimensions of plaintext
        rows, cols = self.plaintext.shape
        
        # Populate the state array matrix
        for i in range(rows):
            for j in range(cols):
                byte = self.plaintext[i, j] # Take the value from the plaintext
                row_in_sbox = int(byte[:4], 2) # First 4-bit sequence (The row) (eg. 1101 1110 --> row_in_sbox = D {13})
                col_in_sbox = int(byte[4:], 2) # Next 4-bit sequence (The column) (eg. 1101 1110 --> col_in_sbox = E {14})
                state_array[i, j] = self.s_box[row_in_sbox, col_in_sbox] # Add the value from S-box into the state array matrix
                
        print(f"Substitue Bytes: \n{state_array}")

        return state_array
    
    """
    Return shifted state array
    Row 0 --> No Shift
    Row 1 --> Shift left by 1
    Row 2 --> Shift left by 2
    Row 3 --> Shift left by 3
    """
    def shift_rows(self, state_array):

        shifted_rows = state_array # Store Matrix to be shifted
        row, col = state_array.shape # Obtain size of the matrix

        # Loop through each row
        for i in range(row):
            shifted_rows[i] = np.roll(state_array[i], shift=(-1 * i)) # Roll the elements in the matrix to the left
        
        print(f"Shift Rows: \n{shifted_rows}")

        return shifted_rows

    def gf_multiply(self, a, b):
        result = 0
        while b:
            if b & 1: 
                result ^= a
            if a & 0x80: 
                a = (a << 1) ^ 0x1b 
            else:
                a <<= 1 
            b >>= 1
        return result & 0xff 


    def mix_columns(self, shifted_rows):        
        int_matrix = np.zeros((4, 4), dtype=np.uint8)
        for i in range(4):
            for j in range(4):
                int_matrix[i, j] = int(shifted_rows[i, j], 2)
        result = np.zeros((4, 4), dtype=np.uint8)
        for col in range(4):
            column = int_matrix[:, col]
            for row in range(4):
                result[row, col] = (
                    self.gf_multiply(self.pre_defined[row, 0], column[0]) ^
                    self.gf_multiply(self.pre_defined[row, 1], column[1]) ^
                    self.gf_multiply(self.pre_defined[row, 2], column[2]) ^
                    self.gf_multiply(self.pre_defined[row, 3], column[3])
                )
        mixed_columns = np.empty((4, 4), dtype=object)
        for i in range(4):
            for j in range(4):
                mixed_columns[i, j] = format(result[i, j], '08b')
        
        print(f"Mix Column: \n{mixed_columns}")
        return mixed_columns

    # Return Final State Array
    def round_key(self, new_state_array):
        row, col = new_state_array.shape # Size of the matrix
        final_state_array = np.empty_like(new_state_array) # Empty matrix to be populated
        for i in range(row):
            for j in range(col):
                # Convert binary strings to integers, XOR them, then convert back to binary
                byte1 = int(new_state_array[i, j], 2)
                byte2 = int(self.round[i, j], 2)
                xor_result = byte1 ^ byte2
                final_state_array[i, j] = format(xor_result, '08b')
        print(f"Add Round Key: \n{final_state_array}")
        return final_state_array
    
    def encrypt(self):
        state = self.plaintext

        print("=== AES ENCRYPTION START ===")
        print(f"Initial Plaintext:\n{state}")

        # Initial round: only AddRoundKey
        print("\n[Round 0] Initial AddRoundKey")
        state = self.round_key(state)

        # 9 Main Rounds: SubBytes -> ShiftRows -> MixColumns -> AddRoundKey
        for round_num in range(1, 10):
            print(f"\n[Round {round_num}]")
            state = self.sub_bytes()
            state = self.shift_rows(state)
            state = self.mix_columns(state)
            state = self.round_key(state)

        # Final Round: SubBytes -> ShiftRows -> AddRoundKey (no MixColumns)
        print("\n[Round 10] Final Round")
        state = self.sub_bytes()
        state = self.shift_rows(state)
        state = self.round_key(state)

        print("\n=== AES ENCRYPTION COMPLETE ===")
        print(f"Final Ciphertext:\n{state}")

        return state



# Test the implementation
plaintext = np.array([
    ['11101010', '00000100', '01100101', '10000101'],
    ['10000011', '01000101', '01011101', '10010110'],
    ['01011100', '00110011', '10011000', '10110000'],
    ['11110000', '00101101', '10101101', '11000101']
 ])

enc = Encryption(plaintext)
ciphertext = enc.encrypt()