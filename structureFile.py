import os

def get_directory_structure(startpath):
    structure = []
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        structure.append(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            structure.append(f"{subindent}{f}")
    return structure

def save_to_txt(filepath, structure):
    with open(filepath, 'w', encoding='utf-8') as f:
        for line in structure:
            f.write(line + '\n')

# Example usage:
start_path = "C:\\Users\\fanxianzhe"  # Change this to your desired directory
directory_structure = get_directory_structure(start_path)
save_to_txt('directory_structure.txt', directory_structure)
# 获取所有的目录结构