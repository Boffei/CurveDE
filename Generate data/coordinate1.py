

import os

input_folder = 'output_coordinates'
output_folder = 'modified_coordinates'

os.makedirs(output_folder, exist_ok=True)


txt_files = [filename for filename in os.listdir(input_folder) if filename.endswith('.txt')]

for filename in txt_files:
    with open(os.path.join(input_folder, filename), 'r') as f:
        lines = f.readlines()

    modified_coords = []

    for line in lines:
        coords = eval(line)
        modified_coords.append([[coord[0], coord[1] + 1] for coord in coords])
        modified_coords.append([[coord[0], coord[1] - 2] for coord in reversed(coords)])

    output_filename = filename.replace('.txt', '.txt')
    with open(os.path.join(output_folder, output_filename), 'w') as f:
        for coords in modified_coords:
            f.write(str(coords) + '\n')

print('coordinate modification and output')
