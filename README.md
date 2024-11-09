# 🎼 Musical-Broccoli

A Python script to extract and display the Table of Contents (TOC) from `.epub` files. This project leverages `EbookLib` and `BeautifulSoup` for efficient EPUB parsing, ensuring secure and robust handling of user input.

## 📚 Project Overview

`musical-broccoli` is designed to help you extract and view the Table of Contents from EPUB files quickly. The script provides a user-friendly interface that allows you to select `.epub` files from either the current directory or a custom directory path. 

Key features include:
- **Input sanitization**: Protects against potential path traversal and invalid characters.
- **Directory and file validation**: Ensures that the provided paths are valid, accessible, and contain `.epub` files.
- **Robust error handling**: Handles various edge cases, such as missing files, permission issues, and malformed input.

## 🔒 Security and Validation

One of the core focuses of `musical-broccoli` is secure handling of user input:

### Input Sanitization Example
The `sanitize_input()` function ensures that the input directory path only contains alphanumeric characters, slashes, dashes, and spaces. This helps prevent potential security vulnerabilities like path traversal attacks.

```python
def sanitize_input(user_input):
    """Sanitize the input to prevent path traversal and invalid characters."""
    sanitized = re.sub(r'[^a-zA-Z0-9_\-/\\ ]', '', user_input)
    return str(Path(sanitized).resolve())
Directory Validation Example
The validate_directory_path() function ensures the provided directory is valid and accessible:

def validate_directory_path(file_path):
    """Ensure the provided path is a valid, accessible directory."""
    if not file_path:
        print("Error: No directory path provided.")
        logging.error("No directory path provided.")
        return False
    try:
        abs_path = os.path.abspath(sanitize_input(file_path))
        if not os.path.isdir(abs_path):
            print("Error: The path is not to a valid directory.")
            return False
        if not os.access(abs_path, os.R_OK):
            print("Error: Access denied.")
            return False
        return True
    except Exception as e:
        print(f"Error validating path: {e}")
        return False
🛠️ Setup Instructions

Prerequisites
Ensure you have Python 3.x installed along with the following libraries:

beautifulsoup4
EbookLib
lxml
Installation
Clone this repository:
git clone https://github.com/yourusername/musical-broccoli.git
cd musical-broccoli
Create a virtual environment:
python -m venv venv
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
Install the required packages:
pip install -r requirements.txt
Dependencies
The project requires the following packages:

beautifulsoup4==4.12.3
EbookLib==0.18
lxml==5.3.0
six==1.16.0
soupsieve==2.6
🚀 Usage

Running the Script
To run the script, simply use:

python scrapper.py
How to Use
Select an option:
Option 1: Use an .epub file from the current directory.
Option 2: Enter a custom directory path to search for .epub files.
Follow the prompts:
If a single .epub file is found, you'll be asked if you want to proceed.
If multiple files are found, you'll be prompted to choose one from the list.
Example Output
Select an option:
1. Use an .epub file in the current directory
2. Enter a directory path to search for .epub files
Enter your choice (1 or 2): 2
Enter the directory path of the .epub file: /Users/username/Documents/epubs
One .epub file found: example.epub
Do you want to proceed with this file? (y/n): y
Table of Contents:
 - Chapter 1: Introduction
 - Chapter 2: Getting Started
 - Chapter 3: Advanced Techniques
🧩 Error Handling

The script handles the following scenarios:

Invalid or inaccessible directory paths.
Missing .epub files.
Improper input during selection.
📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or suggestions.
