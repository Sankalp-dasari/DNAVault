# class AES:
# Implements AES encryption and decryption from scratch.

import numpy as np # Imported for Matrix Calculation

class Encryption:
    def __init__(self, plaintext):
        # Plaintext
        self.plaintext = plaintext

        # Create the S-Box matrix and convert to binary
        self.s_box = np.random.randint(0, 255, size=(16, 16), dtype=np.uint8) # Populate the matrix with random numbers from 0 to 255
        rows, cols = self.s_box.shape
        matrix = np.empty((rows, cols), dtype=object)

        # Convert all numbers to binary
        for i in range(rows):
            for j in range(cols):
                matrix[i, j] = format(self.s_box[i, j], '08b')        
        self.s_box = matrix
        
        # Round Key
        self.roundkey = None

    # Return State Array
    def sub_bytes(self):
        print(f"The S-Box Matrix: \n{self.s_box}")

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
                
        print(f"State Array: \n{state_array}")
        return state_array

    # Return shifted state array
    def shift_rows(self):
        pass

    # Return new state array
    def mix_columns(self):
        pass

    # Return Final State Array
    def round_key(self):
        pass

plaintext = np.array([
    ['00001100', '11101010', '00111000', '01001110'],
    ['01011011', '11111111', '00100000', '01111011'],
    ['11001000', '00010001', '01011001', '11110101'],
    ['01000011', '00001010', '10010001', '11011110']
 ])

enc = Encryption(plaintext)
enc.sub_bytes()