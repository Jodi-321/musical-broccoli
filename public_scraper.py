import os
import warnings
import logging
import re
from pathlib import Path
from ebooklib import epub
from bs4 import BeautifulSoup

# Suppressing known warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=FutureWarning)

logging.basicConfig(
    filename='epub_scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def sanitize_input(user_input):
    #Sanitize the input to prevent path traversal and invalid characters.
    # THis script will only allow alphanumeric characters, spaces, dashes, underscores, and slashes
    sanitized = re.sub(r'[^a-zA-Z0-9_\-/\\ ]', '', user_input)
    return str(Path(sanitized).resolve())

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
    
def search_epub_files(directory):
    # func to search for .epub in directory

    if not directory:
        print("Error: No directory specified.")
        return None
    
    try: 
        epub_files = [file for file in os.listdir(directory) if file.endswith('.epub')]
    except FileNotFoundError:
        print(f"Error: The directory '{directory}' does not exist.")
        return None
    except PermissionError:
        print(f"Error: Permission denied for directory '{directory}.")
        return None
    except Exception as e:
        print(f"Unexpected error accessing directory '{directory}':{e}")
        return None
    
    if not epub_files:
        print("No .epub files found in the current directoy.")
        return None
    
    #if one epub file is found, show to confirm
    if len(epub_files) == 1:
        print(f"One .epub file found: {epub_files[0]}")
        while True:
            confirm = input("Do you want to proceed with this file? (y/n)").strip().lower()
            if confirm == 'y':
                return os.path.abspath(os.path.join(directory, epub_files[0]))
            elif confirm == 'n':
                print("Operation cancelled by user.")
                return None
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
    
    #if multiple epubs are found, show options in console
    print("Multiple .epub files found")
    for index, file in enumerate(epub_files, start=1):
        print(f"{index}.{file}")

    #prompt user to select a file
    while True:
        try:
            choice = int(input("Enter the number of the file you want to select: "))
            if 1 <= choice <= len(epub_files):
                selected_file = epub_files[choice - 1]
                return os.path.abspath(os.path.join(directory, selected_file))
            else:
                print(f"Please enter a number between 1 and {len(epub_files)}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def pull_ToC(file_path):
    #pull out Table of Contents from the selected epub file.
    try:
        book = epub.read_epub(file_path)
        # Get the NCX file that contains the TOC
        toc = book.get_item_with_id('ncx')

        if not toc or not toc.content:
            print("Table of Contents not found.")
            logging.warning(f"No TOC found in the file: {file_path}")
            return
        
        print("Table of Contents:")
        # Use BS4 xml parser to parse the NCX content if necessary
        soup = BeautifulSoup(toc.content, features='xml')
        nav_points = soup.find_all('navPoint')

        if not nav_points:
            print("No entries found in the Table of COntents")
            return

        for nav_point in nav_points:
            #extract title
            label = nav_point.find('text').get_text() if nav_point.find('text') else "Untitled"
            print(f" - {label}")

            #Handle sub-chapters if necessary
            sub_nav_points = nav_point.find_all('navPoint')
            if sub_nav_points:
                for sub_nav in sub_nav_points:
                    sub_label = sub_nav.find('text').get_text() if sub_nav.find('text') else 'Untitled'
                    print(f" - {sub_label}")

        logging.info(f"Succesfully extracted TOC from: {file_path}")
    
    except Exception as e:
        logging.error(f"Error reading file {file_path}:{e}")
        print(f"Error reading file:{e}")

def get_file_path():
    #prompt user to enter a custom file path.
    while True:
        directory = input("Enter the directory path of the .epub file:").strip()
        if not directory:
            print("Error: Directory path cannot be empty. Please enter a valid path.")
        else:
            # Sanitize the input before returning
            return sanitize_input(directory)

def main():
    print("Select an option:")
    print("1. Use an .epub file in the current directory")
    print("2. Enter a directory path to search for .epub file")

    while True:
        choice = input("Enter your choice (1 or 2):").strip()
        if choice in ['1','2']:
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

    if choice == '1':
        file_path = search_epub_files('.')
    elif choice == '2':
        directory = get_file_path()
        if validate_directory_path(directory):
            file_path = search_epub_files(directory)
        else:
            #print("Invalid directory path. Exiting.")
            return
    else:
        print("Invalid choice. Exiting.")
        return
    
    if file_path:
        pull_ToC(file_path)

if __name__ == "__main__":
    main()