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
## 🧠 How It Works (Like a Tiny Crypto Wallet)

You can think of this tool as a very simple, local-only version of a **cryptocurrency wallet**, but for **encrypted sentences** instead of coins.

### 🏦 The Core Idea

- In a crypto wallet:
  - Your **private key / seed phrase** controls access to your funds.
  - If someone gets the private key, they can spend everything.
  - If you lose it, your funds are gone forever.

- In this tool:
  - Your **password or passphrase** is like the **private key / seed phrase**.
  - Your **encrypted token** is like the **on-chain data / encrypted balance**.
  - If someone gets *both* the token **and** the password, they can read the message.
  - If you lose the password, the message is effectively lost forever.

The program never stores your password; it only uses it to derive a key, encrypt/decrypt, and then it’s gone from memory.

---

### 🔑 From Password to Encryption Key (like deriving a wallet key)

In a crypto wallet, your **seed phrase** is turned into a long secret key using specific algorithms.

In this tool, your **password or passphrase** is turned into a 256-bit key using:

- **PBKDF2-HMAC-SHA256**  
- A random **salt** (like extra randomness so the same password doesn’t always give the same key)
- Many **iterations** (to slow down brute-force attacks)

Rough steps:

1. You choose a password or let the tool generate a passphrase.
2. The program generates a random **salt**.
3. PBKDF2 uses:  
   `password + salt + iterations → 256-bit key`
4. That key is used with **AES-256-GCM** for encryption/decryption.

Think of it like:  
> *“Take my secret phrase and stretch it into a strong, wallet-style key.”*

---

### 🔒 Encrypting (like sending coins to an address that only your key can unlock)

When you encrypt a sentence:

1. A random **salt** is created (for key derivation).
2. A random **nonce** is created (a one-time value for AES-GCM).
3. Your password + salt → **key** (via PBKDF2).
4. AES-256-GCM encrypts the sentence into **ciphertext** and attaches an **auth tag** to detect tampering.
5. The program packs everything together as:
   ```text
   salt || nonce || ciphertext

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
