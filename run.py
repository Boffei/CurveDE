import infer
import line_utils
import os
import glob
import cv2
import numpy as np

if __name__ == "__main__":
    img_dir = "demo"
    ckpt = "line.pth"
    config = "lineformer_swin_t_config.py"
    device = "cpu"

    infer.load_model(config, ckpt, device)

    img_paths = glob.glob(os.path.join(img_dir, "*.*"))  # Collect all images in the folder

    for img_path in img_paths:
        img = cv2.imread(img_path)  # BGR format

        line_dataseries = infer.get_dataseries(img, to_clean=False)

        # Save coordinates of line keypoints
        coords = line_utils.points_to_array(line_dataseries)
        coords_np = np.array(coords)  # Convert to NumPy array
        # Reshape the coordinates array and save with brackets and commas
        reshaped_coords = []
        for line_coords in np.split(coords_np, len(line_dataseries)):
            reshaped_coords.append(f"[{','.join(map(str, line_coords.reshape(-1, 2)))}]")
        coords_path = os.path.join("check", "coordinates_" + os.path.basename(img_path) + ".txt")
        with open(coords_path, 'w') as f:
            f.write('\n'.join(reshaped_coords))

        # Visualize extracted line keypoints
        img_with_lines = line_utils.draw_lines(img, coords)

        # Save image with lines
        img_with_lines_path = os.path.join("check", "processed_" + os.path.basename(img_path))
        cv2.imwrite(img_with_lines_path, img_with_lines)


#@InProceedings{10.1007/978-3-031-41734-4_24,
# author="Lal, Jay
# and Mitkari, Aditya
# and Bhosale, Mahesh
# and Doermann, David",
# editor="Fink, Gernot A.
# and Jain, Rajiv
# and Kise, Koichi
# and Zanibbi, Richard",
# title="LineFormer: Line Chart Data Extraction Using Instance Segmentation",
# booktitle="Document Analysis and Recognition - ICDAR 2023",
# year="2023",
# publisher="Springer Nature Switzerland",
# address="Cham",
# pages="387--400",
# abstract="Data extraction from line-chart images is an essential component of the automated document understanding process, as line charts are a ubiquitous data visualization format. However, the amount of visual and structural variations in multi-line graphs makes them particularly challenging for automated parsing. Existing works, however, are not robust to all these variations, either taking an all-chart unified approach or relying on auxiliary information such as legends for line data extraction. In this work, we propose LineFormer, a robust approach to line data extraction using instance segmentation. We achieve state-of-the-art performance on several benchmark synthetic and real chart datasets. Our implementation is available at https://github.com/TheJaeLal/LineFormer.",
# isbn="978-3-031-41734-4"
# }
