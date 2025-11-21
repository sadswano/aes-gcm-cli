"""
main.py

Simple command-line AES-GCM encryption tool with:
- Password-based key derivation (PBKDF2-HMAC-SHA256)
- Optional random passphrase generation
- Basic strength estimation feedback

Usage:
    python main.py
"""

from __future__ import annotations

import base64
import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from passphrase_utils import ask_for_password_or_passphrase


# ---------- Key derivation ----------

def derive_key(password: str, salt: bytes, iterations: int = 200_000) -> bytes:
    """
    Derive a 256-bit key from a password using PBKDF2-HMAC-SHA256.

    Args:
        password: The user-provided password or passphrase.
        salt:     Random bytes; must be stored with the ciphertext.
        iterations: Number of PBKDF2 iterations (higher = slower but stronger).

    Returns:
        A 32-byte key suitable for AES-256.
    """
    password_bytes = password.encode("utf-8")

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,          # 32 bytes = 256-bit key
        salt=salt,
        iterations=iterations,
    )

    return kdf.derive(password_bytes)


# ---------- Encryption / Decryption ----------

def encrypt(plaintext: str, password: str) -> str:
    """
    Encrypt a UTF-8 string with AES-GCM using a key derived from the password.

    The returned value is a URL-safe base64 string that encodes:
        salt || nonce || ciphertext

    Args:
        plaintext: The text to encrypt.
        password:  The password or passphrase.

    Returns:
        A base64-encoded token (string).
    """
    # 1. Random salt for PBKDF2
    salt = os.urandom(16)

    # 2. Derive key from password + salt
    key = derive_key(password, salt)

    # 3. Create AES-GCM cipher
    aesgcm = AESGCM(key)

    # 4. Random nonce (12 bytes is standard for GCM)
    nonce = os.urandom(12)

    # 5. Encrypt (no associated data -> None)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)

    # 6. Pack salt + nonce + ciphertext into a single blob
    packed = salt + nonce + ciphertext

    # 7. Encode as URL-safe base64 for easy copy/paste
    token = base64.urlsafe_b64encode(packed).decode("utf-8")
    return token


def decrypt(token: str, password: str) -> str:
    """
    Decrypt a token produced by `encrypt`.

    The token is expected to be:
        base64(salt || nonce || ciphertext)

    Args:
        token:    The base64-encoded token.
        password: The password or passphrase used for encryption.

    Returns:
        The decrypted plaintext (string).

    Raises:
        Exception if decryption fails (e.g., wrong password or corrupted data).
    """
    # 1. Decode base64 token into raw bytes
    packed = base64.urlsafe_b64decode(token.encode("utf-8"))

    # 2. Extract salt (first 16 bytes), nonce (next 12), ciphertext (rest)
    salt = packed[:16]
    nonce = packed[16:28]
    ciphertext = packed[28:]

    # 3. Derive the same key again
    key = derive_key(password, salt)

    # 4. Decrypt and verify authentication tag
    aesgcm = AESGCM(key)
    plaintext_bytes = aesgcm.decrypt(nonce, ciphertext, None)

    return plaintext_bytes.decode("utf-8")


# ---------- CLI Menu ----------

def print_menu() -> None:
    """Print the main menu."""
    print("=== AES-GCM Sentence Encryption Tool ===")
    print("  1) Encrypt a sentence")
    print("  2) Decrypt a sentence")
    print("  0) Exit")


def handle_encrypt() -> None:
    """Handle the 'encrypt' menu option."""
    plaintext = input("\nEnter the sentence you want to ENCRYPT:\n> ").strip()

    if not plaintext:
        print("Nothing to encrypt (empty input).")
        return

    password = ask_for_password_or_passphrase()

    token = encrypt(plaintext, password)

    print("\n--- ENCRYPTION RESULT ---")
    print("Encrypted token (save this somewhere safe):")
    print(token)
    print()


def handle_decrypt() -> None:
    """Handle the 'decrypt' menu option."""
    token = input("\nEnter the encrypted token:\n> ").strip()
    if not token:
        print("No token provided.")
        return

    password = input("Enter the password or passphrase used for encryption:\n> ").strip()

    try:
        plaintext = decrypt(token, password)
    except Exception:
        print("\n!! Decryption failed.")
        print("Possible reasons:")
        print("  - Wrong password or passphrase")
        print("  - Corrupted or incomplete token")
        print("  - Token was not created by this program")
        print()
        return

    print("\n--- DECRYPTION RESULT ---")
    print("Decrypted sentence:")
    print(plaintext)
    print()


def main() -> None:
    """Entry point for the CLI tool."""
    while True:
        print_menu()
        choice = input("Enter your choice (0/1/2): ").strip()

        if choice == "1":
            handle_encrypt()
        elif choice == "2":
            handle_decrypt()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 0, 1, or 2.\n")


if __name__ == "__main__":
    main()
