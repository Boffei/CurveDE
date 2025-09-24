import json
import os

def process_files(json_folder, txt_folder, output_folder):

    json_files = os.listdir(json_folder)
    json_files.sort()


    txt_files = os.listdir(txt_folder)
    txt_files.sort()


    for json_file in json_files:
        if json_file.endswith('.json'):

            txt_number = json_file[:-5]
            txt_file = [txt for txt in txt_files if txt_number == txt[:-4]]


            if len(txt_file) > 0:
                txt_file = txt_file[0]


                with open(os.path.join(json_folder, json_file), 'r') as f:
                    data = json.load(f)


                with open(os.path.join(txt_folder, txt_file), 'r') as f:
                    coordinates = f.readlines()


                for i, coord in enumerate(coordinates):
                    coords = coord.strip().split()
                    coords_str = " ".join(coords)
                    data['objects'][i % len(data['objects'])]['segmentation'].append(coords_str)


                output_file = os.path.join(output_folder, json_file)
                with open(output_file, 'w') as f:
                    json.dump(data, f, indent=4)


                replace_json_content(output_file)

def replace_json_content(file_path):

    with open(file_path, 'r') as file:
        data = json.load(file)


    updated_data = json.dumps(data, indent=4).replace('"[', '[')
    updated_data = updated_data.replace(']"', ']')


    with open(file_path, 'w') as file:
        file.write(updated_data)


json_folder = 'json'
txt_folder = 'modified_coordinates'
output_folder = 'jsonss'

process_files(json_folder, txt_folder, output_folder)
