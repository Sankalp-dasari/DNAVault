# class AES:
# Implements AES encryption and decryption from scratch.

class Encryption:
    def __init__(self, plaintext):
        self.paintext = plaintext
        self.sblock = None # Define S-Block and permute values
        self.predefined = None # Used in the mix_columns function
        self.roundkey = None # Used in the round_key function

    # Return State Array
    def sub_bytes(self):
        pass

    # Return shifted state array
    def shift_rows(self):
        pass

    # Return new state array
    def mix_columns(self):
        pass

    # Return Final State Array
    def round_key(self):
        pass