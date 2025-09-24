import os
import re


def read_origin_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()


        px_pattern = r"Px: ([+-]?\d+\.\d+)"
        py_pattern = r"Py: ([+-]?\d+\.\d+)"


        origin_pattern = r"原点: \((\d+), (\d+)\)"


        px_match = re.search(px_pattern, text)
        py_match = re.search(py_pattern, text)
        origin_match = re.search(origin_pattern, text)

        if px_match and py_match and origin_match:
            Px = float(px_match.group(1))
            Py = float(py_match.group(1))
            origin_x = int(origin_match.group(1))
            origin_y = int(origin_match.group(2))
            return Px, Py, origin_x, origin_y
    return None



def process_coordinate_file(file_path, Px, Py, origin_x, origin_y):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.readlines()


    with open(file_path, 'w', encoding='utf-8') as file:
        for line in data:
            matches = re.findall(r'\[(\d+),\s(\d+)\]', line)
            for match in matches:
                x = int(match[0])
                y = int(match[1])
                new_x = round((x - origin_x) * Px, 4)
                new_y = round((origin_y - y) * Py, 4)
                line = line.replace(f"[{x}, {y}]", f"[{new_x}, {new_y}]")
            file.write(line)
def process_files_in_folders(coord_folder, origin_folder):
    coord_files = []
    origin_files = []


    for file_name in os.listdir(coord_folder):
        coord_file_path = os.path.join(coord_folder, file_name)
        if os.path.isfile(coord_file_path) and file_name.endswith('.txt'):
            coord_files.append(coord_file_path)


    for file_name in os.listdir(origin_folder):
        origin_file_path = os.path.join(origin_folder, file_name)
        if os.path.isfile(origin_file_path) and file_name.endswith('.txt'):
            origin_files.append(origin_file_path)


    coord_filenames = [re.sub(r'\D', '', os.path.splitext(os.path.basename(file_name))[0]) for file_name in coord_files]


    for i, coord_file in enumerate(coord_files):
        coord_filename = coord_filenames[i]
        for origin_file in origin_files:
            origin_filename = re.sub(r'\D', '', os.path.splitext(os.path.basename(origin_file))[0])
            if coord_filename == origin_filename:
                origin_data = read_origin_file(origin_file)
                if origin_data:
                    Px, Py, origin_x, origin_y = origin_data
                    process_coordinate_file(coord_file, Px, Py, origin_x, origin_y)



coord_folder = 'pixel_point'
origin_folder = 'axis_folder'
process_files_in_folders(coord_folder, origin_folder)
