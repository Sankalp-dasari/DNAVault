# class kyber:
# Implements a simplified or full version of Kyber Key Encapsulation Mechanism.
# - keygen(): Generates public and secret keys.
# - encapsulate(): Generates a shared secret and ciphertext using public key.
# - decapsulate(): Recovers the shared secret from ciphertext using private key.

import numpy as np
import hashlib

class Kyber:
   def __init__(self, n = 256, q = 3329, sigma = 0.15, clamp = 4):
      self.n = n  #polynomial degree
      self.q = q  #modulus, we use a prime number for modular arithmetic and 3329 is chosen as it fits in 12 bits
      self.sigma = sigma  #standard deviation for noise
      self.clamp = clamp  #max noise value to limit extreme error which could cause decryption failure
     
   # Generates a random polynomial with coefficients in range [0, q-1]
   def randomPoly(self):
      """
      picks values between n and q and then calulates a polynomial using a(x) = a₀ + a₁·x + a₂·x² + ... + aₙ₋₁·xⁿ⁻¹ mod q
      for eg-  np.random.randint(0, 17, 4)  might return: [6, 3, 13, 10]
      then  the polynomial is calculated as a(x) = 6 + 3·x + 13·x² + 10·x³ mod 17
      """
      return np.random.randint(0, self.q, self.n) 

   def flatten_key_matrix(matrix):  
    """
    Converts a 4x4 matrix of 8-bit binary strings into a single byte array (16 bytes).
    """
    flat = []
    for row in matrix:
        for binary_str in row:
            flat.append(int(binary_str, 2))
    return bytes(flat)  # 16 bytes for AES-128


   # Generates a random array of integers from -clamp to clamp which is centered around 0. 
   # This is used to create the error noise polynomial(e) in the formula pk = A·s + e
   def noisePoly(self):
      """
      Generates a polynomial with small integer coefficients sampled from
      a discrete Gaussian distribution centered at 0.
      Coefficients are clamped to [-clamp, clamp].
      """
      noise = np.random.normal(0, self.sigma, self.n)
      return np.clip(np.round(noise), -self.clamp, self.clamp).astype(int)

   # Adds two polynomials
   def polyAdd(self, a, b):
      return (a + b) % self.q

   # Multiplies 2 polynomials using the convolve method and then limits it to a max degree of n(256).
   # This gives a good trade off between efficiency and calculation time
   def polyMul(self, a , b):
      result = np.convolve(a, b)[:self.n]
      return result % self.q
   
   #encodes 256 bits message into a polynomial
   def encodeMessage(self, m):
      #encodes 256 bits message into a polynomial
      bit_array = np.unpackbits(np.frombuffer(m, dtype=np.uint8)).astype(np.int32)
      high = int(self.q * 3 / 4)  # safer encoding for 1
      return (bit_array * high).astype(np.int32)


   
   # Decodes a polynomial back into a 256 bits message
   def decodeMessage(self, poly):
    threshold = self.q // 2  # 1664
    bits = (poly > threshold).astype(np.uint8)
    return np.packbits(bits).tobytes()
 
   # Generates a public key that is shared and is used in encapsulation.
   # A secret key that is kept private and is used in decapsulation
   # A public matrix polynomial 'A' that acts as a lattice generator
   def keygen(self):
      """
      Key Generation:
       - A is the public random polynomial (like the public matrix)
       - s is the secret polynomial (private key)
       - e is the noise
       - pk = A * s + e (mod q) is the public key
      """
      A = self.randomPoly() #Public Matrix A
      s = self.randomPoly() #Secret polynomial
      e = self.noisePoly() #error polynomial or noise
      pk = self.polyAdd(self.polyMul(A,s), e) #pk = A * s + e (mod q)
      return A,s,pk #return values

   # Encapsulates a shared secret and ciphertext using the public key.
   def encapsulate(self, pk, A):
      """
      Encapsulation:
       - r is a fresh random secret (like a temporary password)
       - e1, e2 are small noise vectors
       - u = A * r + e1 (mod q)
       - v = pk * r + e2 (mod q)
       - The shared AES key is derived by hashing (u || v || m)
      """
      r = self.randomPoly() # fresh secret for this session
      e1 = self.noisePoly() # error for u
      e2 = self.noisePoly() # error for v
      m = np.random.bytes(32)  #256 bit random message for AES key derivation (needed to derive a unique key for each session)
      m_encoded = self.encodeMessage(m)
      
      u = self.polyAdd(self.polyMul(A, r), e1)  # u = A·r + e1 
      # v = pk·r + m_encoded + e2
      v1 = self.polyMul(pk, r)
      v2 = self.polyAdd(v1, m_encoded)
      v = self.polyAdd(v2, e2)

      # Convert v to bytes and hash it to get a clean AES key
      combined = u.astype(np.uint16).tobytes() +v.astype(np.uint16).tobytes() + m
      shared_key = hashlib.sha256(combined).digest()  # 256-bit AES key

      return (u, v), shared_key, m  # ciphertext + derived AES key

    #Decapsulates the ciphertext using the shared secret key
   def decapsulate(self, u, v, s):
      """
      Decapsulation:
      -Uses the secret key s to recover the shared secret from ciphertext. v' = u.s
      -Then m is recovered from v' by decoding the polynomial. m = decode(v - v')
      -Computes shared key using SHA-256(u || v || m)
      """
      v_prime = self.polyMul(u, s)
      m_recovered = self.decodeMessage((v - v_prime) % self.q)
         
      combined = u.astype(np.uint16).tobytes() + v.astype(np.uint16).tobytes() + m_recovered
      shared_key = hashlib.sha256(combined).digest()
      return shared_key
   
   


