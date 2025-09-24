import os


folder_path = 'modified_coordinates'


files = os.listdir(folder_path)


for file in files:

    if file.endswith('.txt'):

        file_path = os.path.join(folder_path, file)


        with open(file_path, 'r') as f:
            content = f.read()


        new_content = ''
        newline_count = 0
        for char in content:
            if char == '\n':
                newline_count += 1
                if newline_count in [1, 3, 5, 7, 9 ,11]:
                    continue
            new_content += char


        new_content = new_content.replace('][', ',')
        new_content = new_content.replace('[[', '[')
        new_content = new_content.replace(']]', ']')

        with open(file_path, 'w') as f:
            f.write(new_content)


