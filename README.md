# DNAVault
## 🔒 DNA Encryption with AES and Post-Quantum Key Exchange (Kyber)

## 📚 Overview
This project provides a secure, post-quantum cryptographic framework for encrypting DNA sequences. It combines:
- **AES-128** for symmetric encryption of DNA data.
- **Kyber** (a NIST-selected post-quantum algorithm) for secure key encapsulation and exchange.

It is designed to secure sensitive genomic information against both classical and quantum attacks, making it suitable for use in bioinformatics, healthcare, and genetic research fields where data confidentiality is paramount.

In October 2023, Hackers got nearly 7 million people’s data from 23andMe ([The Guardian](https://www.theguardian.com/technology/2024/feb/15/23andme-hack-data-genetic-data-selling-response)). Less than two years later, the copmany filed for bankruptcy in March 2025 ([Reuters](https://www.reuters.com/business/healthcare-pharmaceuticals/dna-testing-firm-23andme-files-chapter-11-bankruptcy-sell-itself-2025-03-24/)).

---

## 🖼️ Implementation

```mermaid
flowchart TD
    subgraph "DNA Preprocessing"
        A1[Read DNA from file] --> A2[Map bases to binary<br/>A=00, G=01, C=10, T=11]
        A2 --> A3[Pad sequence to multiple of 16]
        A3 --> A4[Convert to 4x4 matrices]
    end
    
    subgraph "Kyber Key Exchange"
        B1[Generate random polynomial A] --> B2[Generate secret s and noise e]
        B2 --> B3[Compute pk = A·s + e]
        B3 --> B4[Encapsulation: Generate u,v]
        B4 --> B5[SHA-256 key derivation]
    end
    
    subgraph "AES Encryption"
        C1[Format Kyber key as 4x4 matrix] --> C2[Key Expansion: Generate 10 round keys]
        C2 --> C3[Initial AddRoundKey]
        C3 --> C4[9 Rounds: SubBytes → ShiftRows → MixColumns → AddRoundKey]
        C4 --> C5[Final Round: SubBytes → ShiftRows → AddRoundKey]
    end
    
    subgraph "Integration Layer"
        D1[Read multiple DNA sequences] --> D2[Process each sequence]
        D2 --> D3[Encrypt each 4x4 block]
        D3 --> D4[Verify round-trip integrity]
        D4 --> D5[Output results to file]
    end
    
    A4 --> C1
    B5 --> C1
    C5 --> D3
