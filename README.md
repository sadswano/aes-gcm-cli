#  AES-GCM Sentence Encryption Tool

A small, educational Python CLI tool for **encrypting and decrypting sentences** using modern cryptography:

-  **AES-256-GCM** for encryption  
-  **PBKDF2-HMAC-SHA256** for password-based key derivation  
-  Optional **random passphrase generator** (multi-word)  
-  Basic **strength estimation** (entropy-based)

> ️ This project is meant for learning and personal use.  
> It’s not a replacement for battle-tested, audited security tools in production.

---

##  Features

- Encrypt any sentence or short text into a **single token** (base64 string)
- Decrypt the token back to the original text with the correct password/passphrase
- Choose between:
  - Typing your **own password**, or  
  - Generating a **random passphrase** of multiple words
- Rough **strength estimation** for:
  - Generated passphrases (based on wordlist size & word count)
  - User-typed passwords (based on length & character variety)
- Simple **terminal menu** – no extra UI needed

---

##  Project Structure

Suggested layout:

```text
encryption-tool/
├─ main.py               # CLI app: menu, encrypt/decrypt
├─ passphrase_utils.py   # wordlist loading, passphrase gen, strength estimation
├─ wordlist.txt          # source words for passphrases (one per line)
├─ requirements.txt      # Python dependencies
└─ README.md             # this file
