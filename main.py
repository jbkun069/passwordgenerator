import random
import string

def generate_password(length=12, use_uppercase=True, use_digits=True, use_symbols=True):
    # Define character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase if use_uppercase else ""
    digits = string.digits if use_digits else ""
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?" if use_symbols else ""

    # Combine selected character sets
    all_chars = lowercase + uppercase + digits + symbols
    if not all_chars:
        return "Error: No characters selected!"

    # Generate password
    password = "".join(random.choice(all_chars) for _ in range(length))
    return password
