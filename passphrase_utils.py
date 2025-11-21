"""
passphrase_utils.py

Utilities for working with passwords and passphrases:
- Loading a word list
- Generating random passphrases
- Estimating password/passphrase strength
- Interactive helper for asking the user
"""

from __future__ import annotations

import math
import secrets
from typing import List, Tuple


def load_word_list(path: str = "wordlist.txt") -> List[str]:
    """
    Load a word list from a text file.

    Each non-empty line in the file should contain a single word.
    Lines starting with '#' are treated as comments and ignored.
    """
    words: List[str] = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            word = line.strip()
            if word and not word.startswith("#"):
                words.append(word)

    if not words:
        raise ValueError("Word list is empty. Check your wordlist.txt file.")

    return words


# Load the word list once, when this module is imported.
WORD_LIST: List[str] = load_word_list("wordlist.txt")


def generate_passphrase(num_words: int = 6) -> str:
    """
    Generate a random passphrase by choosing `num_words` words
    from WORD_LIST using cryptographically secure randomness.

    Example output:
        "dragon-forest-galaxy-sunset-matrix-raven"
    """
    if num_words <= 0:
        raise ValueError("num_words must be positive")

    words = [secrets.choice(WORD_LIST) for _ in range(num_words)]
    return "-".join(words)


# ---------- Entropy / strength estimation ----------

def estimate_entropy_passphrase(num_words: int, wordlist_size: int) -> float:
    """
    Estimate entropy (in bits) of a passphrase created by picking
    `num_words` words from a list of size `wordlist_size`, assuming
    each word is chosen uniformly at random.

    Entropy ≈ num_words * log2(wordlist_size)
    """
    if num_words <= 0 or wordlist_size <= 1:
        return 0.0

    return num_words * math.log2(wordlist_size)


def estimate_entropy_password(password: str) -> float:
    """
    Rough entropy estimate for a user-typed password, based on which
    character sets are used (lowercase / uppercase / digits / symbols).

    This is heuristic and not a guarantee. It is only useful as a
    human-friendly indication of strength.
    """
    if not password:
        return 0.0

    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(not c.isalnum() for c in password)

    charset_size = 0
    if has_lower:
        charset_size += 26
    if has_upper:
        charset_size += 26
    if has_digit:
        charset_size += 10
    if has_symbol:
        # Rough guess of printable symbols
        charset_size += 32

    if charset_size == 0:
        return 0.0

    return len(password) * math.log2(charset_size)


def entropy_to_rating(entropy_bits: float) -> Tuple[str, int]:
    """
    Convert an entropy estimate (in bits) to a human-readable label
    and a 0–100 "score" for display.

    Returns:
        (label, score)
        e.g. ("Strong", 80)
    """
    if entropy_bits < 30:
        return "VERY WEAK", 10
    if entropy_bits < 40:
        return "Weak", 25
    if entropy_bits < 60:
        return "Okay", 40
    if entropy_bits < 80:
        return "Moderate", 60
    if entropy_bits < 100:
        return "Strong", 80

    return "VERY STRONG", 95


def print_strength_info(entropy_bits: float) -> None:
    """
    Print a friendly summary of the estimated strength.
    """
    label, score = entropy_to_rating(entropy_bits)
    print(f"Estimated strength: {label} (~{entropy_bits:.1f} bits, score {score}/100)")
    print("Note: this is only an estimate, not a guarantee.\n")


def ask_for_password_or_passphrase() -> str:
    """
    Ask the user whether they want to type their own password
    or have a random passphrase generated for them.

    Returns the chosen password/passphrase.
    """
    print("\nChoose password option:")
    print("  1) Type my own password")
    print("  2) Generate a random passphrase for me")

    choice = input("Enter 1 or 2: ").strip()

    # ----- Option 2: generated passphrase -----
    if choice == "2":
        num_str = input("How many words in the passphrase? (recommended: 6–12): ").strip()

        try:
            num_words = int(num_str)
        except ValueError:
            print("Invalid number, using 6 words by default.")
            num_words = 6

        if num_words < 4:
            print("Too short, using 6 words for better security.")
            num_words = 6
        elif num_words > 20:
            print("That's quite long. Limiting to 20 words.")
            num_words = 20

        password = generate_passphrase(num_words)
        entropy = estimate_entropy_passphrase(num_words, len(WORD_LIST))

        print("\n=== GENERATED PASSPHRASE ===")
        print(password)
        print_strength_info(entropy)
        print("!! IMPORTANT: Save this passphrase. You need it to decrypt later. !!\n")
        return password

    # ----- Default: user-typed password -----
    password = input("Enter your password:\n> ").strip()

    entropy = estimate_entropy_password(password)
    print()
    print_strength_info(entropy)

    return password
