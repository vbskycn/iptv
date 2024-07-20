import os

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def replace_non_ascii(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        
        new_content = ''.join(char if is_ascii(char) else '?' for char in content)
        
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f"Processed file: {filename}")
    except Exception as e:
        print(f"Error processing file {filename}: {e}")

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            replace_non_ascii(file_path)

if __name__ == "__main__":
    directory = r'D:\systemdata\文档\GitHub\iptv\taibiao'
    process_directory(directory)
    print("Finished processing all files.")
