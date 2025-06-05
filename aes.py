# class AES:
# Implements AES encryption and decryption from scratch.

import numpy as np # Imported for Matrix Calculation
import sagemath

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

        # Pre-defined Matrix for the Mix Column Step
        self.pre_defined = np.array([
            [0x02, 0x03, 0x01, 0x01],
            [0x01, 0x02, 0x03, 0x01],
            [0x01, 0x01, 0x02, 0x03],
            [0x03, 0x01, 0x01, 0x02]
        ])
        
        # Round Key
        self.round = np.array([
            ['11001010', '01101100', '10101010', '00011101'],
            ['01010101', '11110000', '00110011', '10100101'],
            ['01111001', '00000011', '11001100', '01011010'],
            ['10111101', '00101101', '10011001', '11100011']
        ])

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
    """
    Return shifted state array
    Row 0 --> No Shift
    Row 1 --> Shift left by 1
    Row 2 --> Shift left by 2
    Row 3 --> Shift left by 3
    """
    def shift_rows(self, state_array):
        print(f"Before Shift: \n{state_array}")

        shifted_rows = state_array # Store Matrix to be shifted
        row, col = state_array.shape # Obtain size of the matrix

        # Loop through each row
        for i in range(row):
            shifted_rows[i] = np.roll(state_array[i], shift=(-1 * i)) # Roll the elements in the matrix to the left
        
        print(f"After Shift: \n{shifted_rows}")

        return shifted_rows


    """
    Return the new state array
    INCOMPLETE
    """
    def mix_columns(self, shifted_rows):
        row, col = shifted_rows.shape
        counter = 0
        for i in range(row):
            row_pre_defined = self.pre_defined[i, :]
            column_shifted = shifted_rows[:, i]
            for j in range(col):
                # Calculation of each term
                S_ij = None



    # Return Final State Array
    def round_key(self, new_state_array):
        row, col = new_state_array.shape # Size of the matrix
        final_state_array = np.zeros_like(new_state_array) # Zero matrix to be populated
        for i in range(row):
            for j in range(col):
                final_state_array[i, j] = new_state_array[i, j] ^ self.round[i, j] # Bitwise XOR operator
        print(f"New State Array: \n{final_state_array}")
        return final_state_array



plaintext = np.array([
    ['00001100', '11101010', '00111000', '01001110'],
    ['01011011', '11111111', '00100000', '01111011'],
    ['11001000', '00010001', '01011001', '11110101'],
    ['01000011', '00001010', '10010001', '11011110']
 ])

enc = Encryption(plaintext)
state_array = enc.sub_bytes()
shifted_rows = enc.shift_rows(state_array)
new_state_array = enc.mix_columns(shifted_rows)
final_state_array = enc.round_key(new_state_array)