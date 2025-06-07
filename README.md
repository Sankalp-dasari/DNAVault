# Post-Quantum DNA Encryption

This project demonstrates **quantum-resistant encryption** of DNA sequences using a hybrid cryptographic approach:
- **AES-128** for fast, symmetric encryption of DNA data blocks.
- **Kyber Key Encapsulation** for secure post-quantum key exchange, ensuring resilience against quantum attacks.

It is designed to showcase **end-to-end DNA data encryption and decryption** with post-quantum security guarantees, following a block cipher methodology adapted for genomic data.

---

## 🚀 Features
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

---

## 🧩 Architecture Overview
``` mermaid
flowchart TB
subgraph "AES Encryption/Decryption"
B1[Encode DNA → Binary] --> B2[Form 4×4 Matrices] --> B3[AES Encrypt Blocks]
B4[AES Decrypt Blocks] --> B5[Decode Binary → DNA]
end
subgraph "Kyber Key Exchange"
    A1[Kyber Key Generation] --> A2[Public Key Distribution]
    A3[Key Encapsulation] --> A4[Shared Secret Key Derivation]
end

A4 --> B3
A4 --> B4
```
---

## 🔒 Security Design

| Component      | Detail                                             |
|:---------------|:----------------------------------------------------|
| **Symmetric Cipher** | AES-128 block cipher (custom, 10 rounds) |
| **Key Exchange**     | Kyber (Lattice-based KEM, simplified implementation) |
| **Data Mapping**     | DNA bases mapped to 2-bit binary: `A=00`, `G=01`, `C=10`, `T=11` |
| **Block Size**       | 16 DNA bases per AES block (32 bits → 128 bits) |
| **Quantum Resistance** | Kyber resists Shor’s algorithm and quantum attacks |
---
## 📂 Project Structure
- `aes.py` – AES-128 custom implementation
- `dna_utils.py` – DNA sequence encoding and decoding utilities
- `kyber.py` – Kyber key encapsulation (simplified)
- `main.py` – End-to-end workflow: DNA encryption & decryption
- `human.txt` – Input DNA sequences (example)
- `encrypted_output.txt` – Output file with encrypted & decrypted sequences
---
## ⚙️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/dna-pqc.git
   cd dna-pqc

## 📚 References
NIST Post-Quantum Cryptography Standardization

AES (Advanced Encryption Standard) - FIPS PUB 197

Kyber: Module-Lattice-Based Key Encapsulation Mechanism

## 📜 License
This project is released under the MIT License.
