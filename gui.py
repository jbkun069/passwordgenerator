import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip
from main import generate_password, calculate_strength

# Define color schemes for light/dark modes
THEMES = {
    "light": {
        "background": "#FFFFFF",
        "foreground": "#000000",
        "button_bg": "#F0F0F0",
        "entry_bg": "#FFFFFF",
        "entry_fg": "#000000",
    },
    "dark": {
        "background": "#2D2D2D",
        "foreground": "#FFFFFF",
        "button_bg": "#3D3D3D",
        "entry_bg": "#3D3D3D",
        "entry_fg": "#FFFFFF",
    }
}

# Function to build the GUI
def build_gui():
    # Create the main window
    window = tk.Tk()
    window.title("Password Generator")
    window.geometry("500x400")

    # Variables to store user choices
    password_length = tk.IntVar(value=12)
    use_uppercase = tk.BooleanVar(value=True)
    use_digits = tk.BooleanVar(value=True)
    use_symbols = tk.BooleanVar(value=True)
    exclude_similar = tk.BooleanVar(value=False)
    custom_charset = tk.StringVar()
    generated_password = tk.StringVar()
    password_history = []
    password_strength = tk.StringVar(value="Strength: ")

    # Track the current theme
    current_theme = tk.StringVar(value="light")

    # Function to toggle themes
    def toggle_theme():
        new_theme = "dark" if current_theme.get() == "light" else "light"
        current_theme.set(new_theme)
        apply_theme(new_theme)

    # Apply the selected theme
    def apply_theme(theme):
        colors = THEMES[theme]
        style = ttk.Style()

        # Configure main window background
        window.configure(bg=colors["background"])

        # Configure ttk styles
        style.theme_use("clam")  # A theme that allows customization
        style.configure(".", background=colors["background"], foreground=colors["foreground"])
        style.configure("TButton", background=colors["button_bg"])
        style.configure("TEntry", fieldbackground=colors["entry_bg"], foreground=colors["entry_fg"])
        style.configure("TCheckbutton", background=colors["background"], foreground=colors["foreground"])

        # Update all widgets
        for widget in window.winfo_children():
            widget.update()

    # Function to handle password generation
    def on_generate():
        try:
            # Get password length and validate it
            length = password_length.get()
            if not isinstance(length, int) or length <= 0:
                messagebox.showerror("Error", "Password length must be a positive integer.")
                return

            # Check if at least one character type is selected
            if not (use_uppercase.get() or use_digits.get() or use_symbols.get() or custom_charset.get()):
                messagebox.showerror("Error", "Select at least one character type (uppercase, digits, symbols, or custom characters).")
                return

            # Generate password
            password = generate_password(
                length=length,
                use_uppercase=use_uppercase.get(),
                use_digits=use_digits.get(),
                use_symbols=use_symbols.get(),
                exclude_similar=exclude_similar.get(),
                custom_charset=custom_charset.get()
            )
            generated_password.set(password)

            # Calculate and display password strength
            strength = calculate_strength(password)
            password_strength.set(f"Strength: {strength}")

            # Add to password history
            password_history.append(password)
            update_history()

        except tk.TclError:  # Catch non-integer input (e.g., text in the length field)
            messagebox.showerror("Error", "Password length must be a number.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    # Function to update password history
    def update_history():
        history_text.delete("1.0", tk.END)
        for pwd in password_history[-5:]:  # Show last 5 passwords
            history_text.insert(tk.END, f"{pwd}\n")

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

    # Theme Toggle Button
    theme_btn = ttk.Button(
        frame,
        text="🌞" if current_theme.get() == "light" else "🌙",
        command=toggle_theme,
        width=3
    )
    theme_btn.grid(row=0, column=2, padx=10)

    # Checkboxes
    ttk.Checkbutton(frame, text="Uppercase Letters", variable=use_uppercase).grid(row=1, column=0, sticky="w")
    ttk.Checkbutton(frame, text="Digits", variable=use_digits).grid(row=2, column=0, sticky="w")
    ttk.Checkbutton(frame, text="Symbols", variable=use_symbols).grid(row=3, column=0, sticky="w")
    ttk.Checkbutton(frame, text="Exclude Similar Characters", variable=exclude_similar).grid(row=4, column=0, sticky="w")

    # Custom Character Set
    ttk.Label(frame, text="Custom Characters:").grid(row=5, column=0, sticky="w")
    custom_entry = ttk.Entry(frame, textvariable=custom_charset)
    custom_entry.grid(row=5, column=1, sticky="w")

    # Generate Button
    generate_btn = ttk.Button(frame, text="Generate Password", command=on_generate)
    generate_btn.grid(row=6, column=0, pady=10)

    # Password Display
    password_entry = ttk.Entry(frame, textvariable=generated_password, width=30, state="readonly")
    password_entry.grid(row=7, column=0, pady=10)

    # Password Strength
    ttk.Label(frame, textvariable=password_strength).grid(row=7, column=1, padx=10)

    # Copy Button
    copy_btn = ttk.Button(frame, text="Copy to Clipboard", command=on_copy)
    copy_btn.grid(row=7, column=2, padx=10)

    # Password History
    ttk.Label(frame, text="Password History:").grid(row=8, column=0, sticky="w")
    history_text = tk.Text(frame, height=5, width=40, state="normal")
    history_text.grid(row=9, column=0, columnspan=3)

    # Apply initial theme
    apply_theme(current_theme.get())

    # Run the application
    window.mainloop()

# Run the GUI
if __name__ == "__main__":
    build_gui()