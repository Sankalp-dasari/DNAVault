# DNA UTILITIES FOR ENCODING AND DECODING DNA SEQUENCES

"""
This class provides utilities to:
- Read DNA sequences from files.
- Convert DNA sequences to binary representations.
- Pad DNA sequences to lengths divisible by 16 for block processing.
- Organize binary data into 4x4 matrices suitable for block ciphers like AES.
- Decode matrices back into DNA sequences.

DNA bases are mapped as:
A -> 00
G -> 01
C -> 10
T -> 11
"""
class dna_utils:
    def __init__(self):
        # Mapping from DNA bases to 2-bit binary
        self.convert = {
            'A': '00',
            'G': '01',
            'C': '10',
            'T': '11'
        }

        # Reverse mapping from 2-bit binary back to DNA bases
        self.retain = {
            '00': 'A',
            '01': 'G',
            '10': 'C',
            '11': 'T'
        }
    
    def fileReader(self, filename):
         """
        Read DNA sequence from a file.
        Assumes the file contains a single-line or multi-line DNA string.
        """
         with open(filename, 'r') as file:
            dna_sequence = file.read()
            return dna_sequence
    

    def padding(self, dna_sequence):
        """
        Pad the DNA sequence to make its length a multiple of 16.
        This is required to form complete 4x4 matrices (each matrix needs 32 bits = 16 bases).
        """
        length = len(dna_sequence)
        remainder = length % 16
        if remainder != 0:
            dna_sequence += 'A' * (16 - remainder) # Add 'A' bases to the end to complete the block
        
        return dna_sequence
    
    def dna_to_binary(self, dna_sequence):
        """
        Convert a DNA sequence to a binary string.
        Each base is mapped to a 2-bit binary representation.
        """
        binaryForm = ""
        for base in dna_sequence:
                binaryForm += self.convert[base] # Append the binary value for each base
        
        return binaryForm
    
    def binary_to_matrices(self, binaryForm):
        """
        Break binary string into a list of 4x4 matrices.
        Each matrix is 4 rows × 4 columns with each element a 2-bit binary string,
        corresponding to a DNA base.
        """
        matrices = []

        # Process binary string in 32-bit chunks (16 DNA bases)
        for i in range(0, len(binaryForm), 32):
            element = binaryForm[i:i+32]
            matrix = []
            for row in range(4):
                matrix_row = []
                for col in range(4):
                    bit_index = row * 8 + col * 2  # Calculate starting bit index for each 2-bit block
                    if bit_index + 1 < len(element):
                        matrix_row.append(element[bit_index:bit_index+2]) # Slice 2 bits for each DNA base
                    else:
                        matrix_row.append('00') # Pad with '00' if incomplete
                matrix.append(matrix_row)
            
            matrices.append(matrix)
        
        return matrices
    
    def encode(self, dna_sequence):
        """
        Encode a DNA sequence into 4x4 matrices.

        Process:
        1. Pad the sequence to make it a multiple of 16.
        2. Convert the padded sequence to binary.
        3. Break the binary string into 4x4 matrices.
        """
        paddedForm = self.padding(dna_sequence) # Pad Sequence
        binaryForm = self.dna_to_binary(paddedForm) # Convert to binary
        matrices = self.binary_to_matrices(binaryForm) # Break into matrices
        
        return matrices
    
    def matrices_to_binary(self, matrices):
        """
        Convert 4x4 matrices back to a single binary string.
        Flattens all matrices row-by-row, cell-by-cell.
        """
        binaryForm = ""
        for matrix in matrices:
            for row in matrix:
                for cell in row:
                    binaryForm += cell # Concatenate 2-bit cells back to a single string
        return binaryForm
    
    def binary_to_dna(self, binaryForm):
        """
        Convert a binary string back to a DNA sequence.
        Every 2 bits correspond to one DNA base.
        """
        dna_sequence = ""
        for i in range(0, len(binaryForm), 2):
            binary_pair = binaryForm[i:i+2]
            if binary_pair in self.retain:
                dna_sequence += self.retain[binary_pair] # Convert each 2-bit to its base
        return dna_sequence
    
    def decode(self, matrices, original_length):
        """
        Decode 4x4 matrices back to the original DNA sequence.

        Process:
        1. Convert matrices to binary.
        2. Convert binary to DNA sequence.
        3. Truncate to original DNA length (before padding).
        """
        binaryForm = self.matrices_to_binary(matrices) # Matrix to binary
        dna_sequence = self.binary_to_dna(binaryForm) # Binary to DNA
        dna = dna_sequence[:original_length] # Removing padding bases
        return dna
    
    def print_matrices(self, matrices):
        """
        Print the list of 4x4 matrices and displays matrices in a readable format.
        """
        for i, matrix in enumerate(matrices):
            print(f"\nMatrix {i + 1}:")
            for row in matrix:
                print(" ".join(row))


"""
TEST DNA UTILITY CLASS
"""
if __name__ == "__main__":
    dna_utils = dna_utils()
    
    # Read DNA sequence from file
    file_dna = dna_utils.fileReader("dna_sequence_dataset.txt")
    if file_dna:
        print(f"Total length: {len(file_dna)} bases")
        matrices = dna_utils.encode(file_dna) # Encode the DNA sequence into matrices
        if matrices:
            print(f"\nShowing all {len(matrices)} matrices:")
            dna_utils.print_matrices(matrices) # Display all matrices
            print()
            print(dna_utils.decode(matrices, len(file_dna))) # Decode the matrices back into a DNA sequence