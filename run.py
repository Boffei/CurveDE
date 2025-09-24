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
