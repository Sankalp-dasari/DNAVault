# Coordinates the encryption process:
# - Takes DNA input
# - Encodes DNA to bytes
# - Kyber creates a round key for AES encryption
# - AES encrypts the DNA sequence
# - Simulates transmission of encrypted DNA + Kyber ciphertext
# - Decrypts Kyber using secret key 
# - Kyber Decryption gives AES key
# - AES is decrypted using round key
# - Decrypts DNA data and prints result
# - Original and Decrypted DNA data are verified 

from kyber import Kyber
from aes import Encryption
from dna_utils import dna_utils
import numpy as np

# initialise
dna_util = dna_utils()
kyber = Kyber()

# parsing input file 
dna_sequences = []
with open("human.txt", "r") as file:
    for line in file:
        dna_sequences.append(line.strip())
    
# Generate kyber key and AES key
A,s,pk = kyber.keygen()
(u, v), shared_key, m = kyber.encapsulate(pk, A)

# Format Kyber shared key into 4x4 binary AES round key
round_key_matrix = np.array([
    [format(byte, '08b') for byte in shared_key[i:i+4]]
    for i in range(0, 16, 4)
])

# Encrypt and Decrypt Each DNA Sequence
with open("encrypted_output.txt", "w") as outfile:
    for index, dna_seq in enumerate(dna_sequences):
        if not dna_seq:
            continue 

        matrices = dna_util.encode(dna_seq)
        encrypted_blocks = []
        decrypted_blocks = []

        for mat in matrices:
            plaintext_matrix = np.array([[format(int(cell, 2), '08b') for cell in row] for row in mat])

            # AES Encryption
            enc = Encryption(plaintext_matrix)
            enc.round_key = round_key_matrix
            enc.list_of_round_keys = [round_key_matrix]
            for i in range(10): 
             enc.key_expansion(counter=i)
            ciphertext = enc.encrypt()

            # AES Decryption
            dec = Encryption(plaintext_matrix)
            dec.round_key = round_key_matrix
            dec.list_of_round_keys = [round_key_matrix]
            for i in range(10):
             dec.key_expansion(counter=i)
            decrypted_matrix = dec.decrypt(ciphertext)

            # Store output
            encrypted_blocks.append(ciphertext)
            decrypted_blocks.append(decrypted_matrix)

        # Decode back to DNA
        encrypted_dna = dna_util.decode([[[cell[-2:] for cell in row] for row in block] for block in encrypted_blocks], len(dna_seq))
        decrypted_dna = dna_util.decode([[[cell[-2:] for cell in row] for row in block] for block in decrypted_blocks], len(dna_seq))

        # Write to output
        outfile.write(f"DNA {index+1}:\n")
        outfile.write(f"Original:  {dna_seq}\n")
        outfile.write(f"Encrypted: {encrypted_dna}\n")
        outfile.write(f"Decrypted: {decrypted_dna}\n")
        outfile.write(f"Match:     {dna_seq == decrypted_dna}\n\n")