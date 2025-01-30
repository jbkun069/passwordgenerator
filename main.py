import random
import string

def generate_password(length=12, use_uppercase=True, use_digits=True, use_symbols=True, exclude_similar=False, custom_charset=""):
    # Define character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase if use_uppercase else ""
    digits = string.digits if use_digits else ""
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?" if use_symbols else ""

    # Combine selected character sets
    all_chars = lowercase + uppercase + digits + symbols

    # Exclude similar characters
    if exclude_similar:
        all_chars = all_chars.translate(str.maketrans('', '', 'l1IoO0'))

    # Add custom characters if provided
    all_chars += custom_charset

    if not all_chars:
        return "Error: No characters selected!"

    # Generate password
    password = "".join(random.choice(all_chars) for _ in range(length))
    return password

def calculate_strength(password):
    length = len(password)
    categories = [0, 0, 0, 0]  # lowercase, uppercase, digits, symbols
    for char in password:
        if char in string.ascii_lowercase:
            categories[0] = 1
        elif char in string.ascii_uppercase:
            categories[1] = 1
        elif char in string.digits:
            categories[2] = 1
        else:
            categories[3] = 1

    strength = sum(categories)  # Number of categories used
    return 'Weak' if strength == 1 else 'Moderate' if strength == 2 else 'Strong' if strength == 3 else 'Very Strong'

# Example usage:
if __name__ == "__main__":
    password = generate_password(length=15, exclude_similar=True, custom_charset="@$")
    strength = calculate_strength(password)
    print(f"Generated Password: {password} (Strength: {strength})")