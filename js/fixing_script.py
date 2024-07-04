import os
import re

# Usage
directory = '.'

for filename in os.listdir(directory):
    if filename.endswith(".js"):  # Check for JavaScript files
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()

        # Pattern to find constructors and process them
        pattern = r'(constructor\s*\(([^)]*)\)\s*{)(.*?)(})'
        def process_constructor(m):
            js_constructor = m.group(0)
            print("---"*50)
            print("Original Constructor:", js_constructor)

            # Check for and handle super(...) calls with full line capture
            super_pattern = r'(\s*)super\(([^)]*)\);'
            super_search = re.search(super_pattern, js_constructor)
            if super_search:
                super_function_line = super_search.group(0)
                print("Found super function line:", super_function_line.strip())
                
                # Remove the existing super() line
                modified_constructor_body = re.sub(super_pattern, '', m.group(3), flags=re.DOTALL)
                
                # Insert the super() line at the beginning of the constructor
                js_constructor_new = f"{m.group(1)}{super_search.group(1)}{super_function_line.strip()}" + modified_constructor_body + m.group(4)
                print("Modified Constructor:", js_constructor_new)
                return js_constructor_new
            else:
                print("No super function line found.")
                return js_constructor  # Return as is if no super call

        # Replace constructors in the content
        content = re.sub(pattern, process_constructor, content, flags=re.DOTALL)

        # Additional processing such as class name replacement
        class_name = 'Cls' + re.sub(r'\W', '', filename.split('.')[0])
        content = re.sub(r'\bCls\b', class_name, content)

        # Write the modified content back to the file
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)
