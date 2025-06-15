# DNAVault

---

## Overview
In October 2023, 23andMe suffered a significant data breach in which hackers accessed the personal information of over 7 million users ([The Guardian](https://www.theguardian.com/technology/2024/feb/15/23andme-hack-data-genetic-data-selling-response)). Less than two years later, the company filed for bankruptcy in March 2025 ([Reuters](https://www.reuters.com/business/healthcare-pharmaceuticals/dna-testing-firm-23andme-files-chapter-11-bankruptcy-sell-itself-2025-03-24/)).

As cyberattacks become increasingly sophisticated and the advent of quantum computing threatens traditional cryptographic methods, the need for resilient security protocols is more critical than ever. In response to these emerging threats, we have implemented a robust solution: a system that employs the Advanced Encryption Standard (AES) for encrypting sensitive user data, combined with Kyber, a post-quantum cryptographic scheme, to ensure secure and quantum-resistant key exchange.

This project demonstrates **quantum-resistant encryption** of DNA sequences using a hybrid cryptographic approach:
- **AES-128** for fast, symmetric encryption of DNA data blocks.
- **Kyber Key Encapsulation** for secure post-quantum key exchange, ensuring resilience against quantum attacks.

It is designed to showcase **end-to-end DNA data encryption and decryption** with post-quantum security guarantees making it suitable for use in bioinformatics, healthcare, and genetic research fields where data confidentiality is paramount.

[LINK TO THE PROJECT](https://dna-vault.vercel.app/)

## Features
- **AES-128 Encryption**:  
  Custom implementation of AES operating on 4×4 matrices of 8-bit binary strings.
- **Kyber Key Exchange**:  
  Lattice-based key encapsulation providing post-quantum security (NIST PQC standard family).
- **DNA Sequence Support**:  
  Encoding and decoding of DNA (`A`, `G`, `C`, `T`) to binary form compatible with AES block size.
- **End-to-End Encryption/Decryption**:  
  Encryption of real DNA datasets, decryption, and validation of correctness.
- **Post-Quantum Ready**:  
  Quantum-safe key generation using Kyber ensures long-term security.

## Comparisons
### Key Generation Time (Kyber vs RSA) ([IEEE Xplore](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10956786))

| Algorithm          | Duration (ms) |
|--------------------|--------------|
| Kyber-512          | 0.21         |
| Kyber-768          | 0.27         |
| Kyber-1024         | 0.33         |
| RSA-3072-Base64    | 484.74       |
| RSA-7680-Base64    | 19329.88     |
| RSA-15360-Base64   | 186792.53    |

On average, the Kyber-DNA algorithm is approximately **2.5507× $10^5$** times faster compared to the RSA-Base64 algorithm at key generation.

### Classical and Quantum Attack Performance (DES vs AES vs RSA) ([IEEE Xplore](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7298334))

| **Factor**               | **DES**                             | **AES**                              | **RSA**                         |
|---------------------------|-------------------------------------|--------------------------------------|----------------------------------|
| **Possible Keys**         | 2⁵⁶ ≈ 7.2×10¹⁶                     | 2¹²⁸, 2¹⁹², 2²⁵⁶                    | Variable (RSA-2048 ≈ 112-bit equiv) |
| **Time to Break (Classical)** | ~1 day (modern hardware)         | ~10¹⁸ years (AES-128 brute-force)    | RSA-2048: ~10¹⁵ years (factoring, classical) |
| **Time to Break (Quantum)** | ~ seconds (Grover, too small key)  | AES-128: 2⁶⁴ operations (~0.6 years with ideal Grover) | RSA-2048: polynomial time (minutes to hours, post-quantum) |
| **Operations to Break**   | 2⁵⁶ brute-force                     | 2¹²⁸ brute-force; 2⁶⁴ Grover quantum | Shor's Algorithm: polynomial in log(n) |

AES can withstand both classical and quantum attacks well and is considered strong and is classified as safe for "top secret" information by the NSA.

## Architecture Overview
``` mermaid
flowchart TB
subgraph "AES Encryption/Decryption"
B1[Encode DNA → Binary] --> B2[Form 4×4 Matrices] --> B3[AES Encrypt Blocks]
B4[AES Decrypt Blocks] --> B5[Decode Binary → DNA]
end
subgraph "Kyber Key Exchange"
    A1[Kyber Key Generation] --> A2[Public Key Distribution]
    A2 --> A3
    A3[Key Encapsulation] --> A4[Shared Secret Key Derivation]
end

A4 --> B3
A4 --> B4
```
---

## Security Design

| Component      | Detail                                             |
|:---------------|:----------------------------------------------------|
| **Symmetric Cipher** | AES-128 block cipher (custom, 10 rounds) |
| **Key Exchange**     | Kyber (Lattice-based KEM, simplified implementation) |
| **Data Mapping**     | DNA bases mapped to 2-bit binary: `A=00`, `G=01`, `C=10`, `T=11` |
| **Block Size**       | 16 DNA bases per AES block (32 bits → 128 bits) |
| **Quantum Resistance** | Kyber resists Shor’s algorithm and quantum attacks |
---
## Project Structure
- `aes.py` – AES-128 custom implementation
- `dna_utils.py` – DNA sequence encoding and decoding utilities
- `kyber.py` – Kyber key encapsulation (simplified)
- `main.py` – End-to-end workflow: DNA encryption & decryption
- `human.txt` – Input DNA sequences (example)
- `encrypted_output.txt` – Output file with encrypted & decrypted sequences
---
## Installation

1. **Clone the repository**:
   ```bash
   git clone git@github.com:Sankalp-dasari/DNAVault.git
   cd DNAVault

## References
- Bos, J. W., Ducas, L., Kiltz, E., Lepoint, T., Lyubashevsky, V., Schanck, J. M., Schwabe, P., & Seiler, G. (2017). _CRYSTALS-Kyber: A CCA-Secure Module-Lattice-Based KEM_. Retrieved from [https://pq-crystals.org/kyber/](https://pq-crystals.org/kyber/)

- National Institute of Standards and Technology (NIST). (2001). _Announcing the Advanced Encryption Standard (AES)_. (FIPS PUB 197). U.S. Department of Commerce. Retrieved from [https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197-upd1.pdf](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197-upd1.pdf)

- Aggarwal, D., Brennen, G. K., Lee, T., Santha, M., & Tomamichel, M. (2023). Quantum attacks on public-key cryptosystems. _IEEE Transactions on Information Theory_, 69(8), 5208–5253. [https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10956786](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10956786)

- Bernstein, D. J., & Lange, T. (2015). Post-quantum cryptography. _IEEE Security & Privacy_, 13(5), 14–19. [https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7298334](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7298334)

## License
This project is released under the MIT License.
