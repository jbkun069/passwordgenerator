import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip

# Function to generate a password
def generate_password(length=12, use_uppercase=True, use_digits=True, use_symbols=True):
    lowercase = string.ascii_lowercase  # Always include lowercase
    uppercase = string.ascii_uppercase if use_uppercase else ""
    digits = string.digits if use_digits else ""
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?" if use_symbols else ""

    all_chars = lowercase + uppercase + digits + symbols
    password = "".join(random.choice(all_chars) for _ in range(length))
    return password

# Function to build the GUI
def build_gui():
    # Create the main window
    window = tk.Tk()
    window.title("Password Generator")
    window.geometry("400x300")

    # Variables to store user choices
    password_length = tk.IntVar(value=12)
    use_uppercase = tk.BooleanVar(value=True)
    use_digits = tk.BooleanVar(value=True)
    use_symbols = tk.BooleanVar(value=True)
    generated_password = tk.StringVar()

    # Function to handle password generation
    def on_generate():
        try:
            # Get password length and validate it
            length = password_length.get()
            if not isinstance(length, int) or length <= 0:
                messagebox.showerror("Error", "Password length must be a positive integer.")
                return

            # Check if at least one character type is selected
            if not (use_uppercase.get() or use_digits.get() or use_symbols.get()):
                messagebox.showerror("Error", "Select at least one character type (uppercase, digits, or symbols).")
                return

            # Generate password
            password = generate_password(
                length=length,
                use_uppercase=use_uppercase.get(),
                use_digits=use_digits.get(),
                use_symbols=use_symbols.get()
            )
            generated_password.set(password)

        except tk.TclError:  # Catch non-integer input (e.g., text in the length field)
            messagebox.showerror("Error", "Password length must be a number.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    # Function to copy password to clipboard
    def on_copy():
        password = generated_password.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Copied!", "Password copied to clipboard.")
        else:
            messagebox.showwarning("No Password", "Generate a password first!")

    # GUI Layout
    frame = ttk.Frame(window, padding=20)
    frame.pack(fill=tk.BOTH, expand=True)

    # Password Length
    ttk.Label(frame, text="Password Length:").grid(row=0, column=0, sticky="w")
    length_entry = ttk.Entry(frame, textvariable=password_length, width=5)
    length_entry.grid(row=0, column=1, sticky="w")

    # Checkboxes
    ttk.Checkbutton(frame, text="Uppercase Letters", variable=use_uppercase).grid(row=1, column=0, sticky="w")
    ttk.Checkbutton(frame, text="Digits", variable=use_digits).grid(row=2, column=0, sticky="w")
    ttk.Checkbutton(frame, text="Symbols", variable=use_symbols).grid(row=3, column=0, sticky="w")

    # Generate Button
    generate_btn = ttk.Button(frame, text="Generate Password", command=on_generate)
    generate_btn.grid(row=4, column=0, pady=10)

    # Password Display
    password_entry = ttk.Entry(frame, textvariable=generated_password, width=30, state="readonly")
    password_entry.grid(row=5, column=0, pady=10)

    # Copy Button
    copy_btn = ttk.Button(frame, text="Copy to Clipboard", command=on_copy)
    copy_btn.grid(row=5, column=1, padx=10)

    # Run the application
    window.mainloop()

# Run the GUI
if __name__ == "__main__":
    build_gui()