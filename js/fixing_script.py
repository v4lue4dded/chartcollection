import os
import re


# Usage
directory = '.'

for filename in os.listdir(directory):
    print(filename)
    if filename.endswith(".js"):  # Check for JavaScript files
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Move super(...) to the start of the constructor
        content = re.sub(
            r'(constructor\(\.\.\.args\) {)\s*(.*?)(\s*super\(\.\.\.args\);)',
            r'\1\n        super(...args);\n        \2',
            content,
            flags=re.DOTALL
        )

        # Rename 'Cls' to 'Cls<filename>' where filename is modified
        class_name = 'Cls' + re.sub(r'\W', '', filename.split('.')[0])
        content = re.sub(r'\bCls\b', class_name, content)

        # Write the modified content back to the file
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)
