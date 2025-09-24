import os
import re
import numpy as np
from scipy.stats import linregress


folder_path = 'pixel_point'


file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.txt')]


output_directory = 'result'
os.makedirs(output_directory, exist_ok=True)



def find_max_coordinates(line):
    pattern = r'\[(.*?), (.*?)\]'
    matches = re.findall(pattern, line)
    coordinates = np.array([list(map(float, m)) for m in matches])
    max_x_coord = tuple(coordinates[coordinates[:, 0].argmax()])
    max_y_coord = tuple(coordinates[coordinates[:, 1].argmax()])
    coordinates = coordinates[:int(len(coordinates) / 2)]


    slope_changes = np.diff(coordinates[:, 1]) / np.diff(coordinates[:, 0])


    max_slope_index = np.argmax(slope_changes)


    slope_changes_after_max_slope = np.diff(slope_changes[max_slope_index:])
    if len(slope_changes_after_max_slope) == 0:
        max_slope_change_index = 10
    else:

      max_slope_change_index = max_slope_index + np.argmax(slope_changes_after_max_slope)


    line_coordinates = coordinates[:max_slope_change_index + 1]

    slope, intercept, r_value, p_value, std_err = linregress(line_coordinates[:, 0], line_coordinates[:, 1])
    slope = round(slope, 4)

    if max_x_coord[0] < 1:
        intercept = round(-0.002 * slope, 2)
    else:
        intercept = round(-0.2 * slope, 2)



    distances = np.abs(slope * coordinates[max_slope_index + 1:, 0] + intercept - coordinates[max_slope_index + 1:,1])
    max_fit_index_after_max_slope = np.argmin(distances)


    max_fit_index =max_slope_index + max_fit_index_after_max_slope + 1
    max_fit_coord = tuple(coordinates[max_fit_index])

    return max_x_coord, max_y_coord, slope, intercept, max_fit_coord



for file_path in file_paths:
    output_path = os.path.join(output_directory, os.path.splitext(os.path.basename(file_path))[0] + '.txt')
    with open(output_path, 'w') as outfile:
        with open(file_path, 'r') as file:
            for line in file:
                max_x_coord, max_y_coord, slope, intercept, max_fit_coord = find_max_coordinates(line)
                output = f"[{max_x_coord[0]}, {max_x_coord[1]}], [{max_y_coord[0]}, {max_y_coord[1]}], [{max_fit_coord[0]}, {max_fit_coord[1]}] {slope}\n"
                outfile.write(output)

print("finish")