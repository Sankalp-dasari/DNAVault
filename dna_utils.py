class dna_utils:
    def __init__(self):
        self.convert = {
            'A': '00',
            'G': '01',
            'C': '10',
            'T': '11'
        }
    
    def fileReader(self, filename):
         with open(filename, 'r') as file:
            dna_sequence = file.read()
            return dna_sequence
    
    def padding(self, dna_sequence):
        length = len(dna_sequence)
        remainder = length % 16
        if remainder != 0:
            dna_sequence += 'A' * (16 - remainder)
        
        return dna_sequence
    
    def dna_to_binary(self, dna_sequence):
        binaryForm = ""
        for base in dna_sequence:
                binaryForm += self.convert[base]
        
        return binaryForm
    
    def binary_to_matrices(self, binaryForm):
        matrices = []
        for i in range(0, len(binaryForm), 32):
            element = binaryForm[i:i+32]
            matrix = []
            for row in range(4):
                matrix_row = []
                for col in range(4):
                    bit_index = row * 8 + col * 2  
                    if bit_index + 1 < len(element):
                        matrix_row.append(element[bit_index:bit_index+2])
                    else:
                        matrix_row.append('00') 
                matrix.append(matrix_row)
            
            matrices.append(matrix)
        
        return matrices
    
    def encode(self, dna_sequence):
        paddedForm = self.padding(dna_sequence)
        binaryForm = self.dna_to_binary(paddedForm)
        matrices = self.binary_to_matrices(binaryForm)
        
        return matrices
    
    def print_matrices(self, matrices):
        for i, matrix in enumerate(matrices):
            print(f"\nMatrix {i + 1}:")
            for row in matrix:
                print(" ".join(row))

if __name__ == "__main__":
    dna_utils = dna_utils()
    
    file_dna = dna_utils.fileReader("dna_sequence_dataset.txt")
    if file_dna:
        print(f"Total length: {len(file_dna)} bases")
        matrices = dna_utils.encode(file_dna)
        if matrices:
            print(f"\nShowing all {len(matrices)} matrices:")
            dna_utils.print_matrices(matrices)