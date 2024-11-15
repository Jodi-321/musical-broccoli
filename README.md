
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
    sanitized = re.sub(r'[^a-zA-Z0-9_\-/ ]', '', user_input)
    return str(Path(sanitized).resolve())
```

### Directory Validation Example
The `validate_directory_path()` function ensures the provided directory is valid and accessible:

```python
def validate_directory_path(file_path):
    #Make sure user input is a valid, accessible directory. 
    if not file_path:
        print("Error: No directory path provided.")
        logging.error("No directory path provided.")
        return False

    try:
        # Sanitize input to remove any malicious characters
        sanitized_path = sanitize_input(file_path
                                        )
        #Convert to absolute path and resolve to prevent path traversal
        abs_path = os.path.abspath(sanitized_path)

        # Check if the path is a directory
        if not os.path.isdir(abs_path):
            logging.error(f"Provided path is not a directory: {file_path}")
            print("Error: The path is not to a valid directory.")
            return False
        
        # Check if the directory is accessible
        if not os.access(abs_path, os.R_OK):
            logging.error(f"Access denied for directory: {file_path}")
            print("Error: You do not have permission to access this directory.")
            return False
        return True
    except Exception as e:
        logging.error(f"Error validating directory path: {e}")
        print(f"Error: {e}")
        return False
```

## 🛠️ Setup Instructions

### Prerequisites

Ensure you have Python 3.x installed along with the following libraries:
- `beautifulsoup4`
- `EbookLib`
- `lxml`

### Installation

1. **Clone this repository**:
   ```bash
   git clone https://github.com/Jodi-321/musical-broccoli.git
   cd musical-broccoli
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

### Dependencies

The project requires the following packages:

```
beautifulsoup4==4.12.3
EbookLib==0.18
lxml==5.3.0
six==1.16.0
soupsieve==2.6
```

## 🚀 Usage

### Running the Script
To run the script, simply use:

```bash
python public_scraper.py
```

### How to Use

1. **Select an option**:
   - Option `1`: Use an `.epub` file from the current directory.
   - Option `2`: Enter a custom directory path to search for `.epub` files.

2. **Follow the prompts**:
   - If a single `.epub` file is found, you'll be asked if you want to proceed.
   - If multiple files are found, you'll be prompted to choose one from the list.

### Example Output

```
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
```

## 🧩 Error Handling

The script handles the following scenarios:

- Invalid or inaccessible directory paths.
- Missing `.epub` files.
- Improper input during selection.

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

