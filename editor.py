import customtkinter as ctk
from tkinter import filedialog
from tkcode import CodeEditor
import sys
import io

# Initialize root window with customtkinter
root = ctk.CTk()

# Set the window title and allow resizing and minimize/maximize
root.title("Code Editor")

# Set minimum size for the window to avoid too small a window
root.minsize(800, 600)

# Prompt the user to input the name of the file (code variable)
input_dialog = ctk.CTkInputDialog(title="Enter File Name", text="Enter the file name (without extension):")
code = input_dialog.get_input()

# If no input is provided, default to "aman"
if not code:
    code = "aman"

# Initialize the CodeEditor widget directly in the root window
code_editor = CodeEditor(
    root,
    width=99,
    height=25,
    language="python",
    background="black",
    highlighter="dracula",
    font="Consolas",
    autofocus=True,
    insertofftime=0,
    padx=10,
    pady=10,
)

# Create CTkOptionMenu to replace the traditional menu
options = ["Open", "Save", "Run"]

def option_selected(option):
    if option == "Open":
        open_file()
    elif option == "Save":
        save_file()
    elif option == "Run":
        run_code()

# Create the OptionMenu widget and pack it at the top of the window
option_menu = ctk.CTkOptionMenu(root, values=options, command=option_selected)
option_menu.pack(side="top", padx=10, pady=10, anchor="w")

# Pack the code editor after the OptionMenu
code_editor.pack(fill="both", expand=True)

# Create a Text widget for the output console
# Create a Text widget for the output console with dynamic resizing
output_console = ctk.CTkTextbox(root, wrap="word", font=("Arial", 12))
output_console.pack(fill="x", padx=10, pady=10)

# Function to run the code
def run_code():
    code_to_run = code_editor.content
    try:
        # Redirect stdout to capture the output
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        # Execute the code entered in the editor
        exec(code_to_run)

        # Get the output and display it in the console
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        # Insert output into the output console
        output_console.delete(1.0, ctk.END)  # Clear previous output
        output_console.insert(ctk.END, output)  # Show new output

    except Exception as e:
        output_console.delete(1.0, ctk.END)
        output_console.insert(ctk.END, f"Error: {e}")

# Function to save the code to a file
def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "w") as f:
            f.write(code_editor.content)

# Function to open a file and load it into the code editor
def open_file():
    file_path = filedialog.askopenfilename(defaultextension=".py", filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r") as f:
            code_editor.content = f.read()
            # Update the code editor content
            code_editor.set_text(code_editor.content)

# Start the main event loop
root.mainloop()
