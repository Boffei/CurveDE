import cv2
import numpy as np
import os
import pytesseract
import re


image_folder = 'image_folder'
result_folder = 'axis_folder'
os.makedirs(result_folder, exist_ok=True)


for image_file in os.listdir(image_folder):

    image_path = os.path.join(image_folder, image_file)
    image = cv2.imread(image_path)


    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    edges = cv2.Canny(gray, 50, 150, apertureSize=3)


    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)


    min_distance_horizontal = float("inf")
    min_distance_vertical = float("inf")
    horizontal_line = None
    vertical_line = None
    for line in lines:
        x1, y1, x2, y2 = line[0]
        distance = np.sqrt((x1 - 0) ** 2 + (image.shape[0] - y1) ** 2)
        if abs(x2 - x1) > abs(y2 - y1):
            if distance < min_distance_horizontal:
                min_distance_horizontal = distance
                horizontal_line = line
        else:  #
            if distance < min_distance_vertical:
                min_distance_vertical = distance
                vertical_line = line


    if horizontal_line is not None and vertical_line is not None:
        x1, y1, x2, y2 = horizontal_line[0]
        x3, y3, x4, y4 = vertical_line[0]
        intersection_x = int(((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / (
                    (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)))
        intersection_y = int(((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / (
                    (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)))
        print("Intersection point for {}: ({}, {})".format(image_file, intersection_x, intersection_y))
        cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 3)
        cv2.line(image, (x3, y3), (x4, y4), (0, 0, 255), 3)
        output_filepath = os.path.join(result_folder, image_file)
        cv2.imwrite(output_filepath, image)


        cropped_image1 = gray[0:intersection_y, 0:intersection_x]
        cropped_image2 = gray[intersection_y:image.shape[0], intersection_x:image.shape[1]]


        data1 = pytesseract.image_to_data(cropped_image1, config="--psm 6", output_type=pytesseract.Output.DICT)
        data2 = pytesseract.image_to_data(cropped_image2, config="--psm 6", output_type=pytesseract.Output.DICT)


        num_blocks1 = len(data1['text'])
        num_blocks2 = len(data2['text'])


        result_file = os.path.splitext(image_file)[0] + '.txt'
        result_path = os.path.join(result_folder, result_file)


        with open(result_path, 'w', encoding='utf-8') as file:
            file.write("origin: ({}, {})".format(intersection_x, intersection_y) + "\n")
            file.write("vertical axis point：" + "\n")
            selected_lines1 = []
            for i in range(len(data1['left'])):
                if int(data1['conf'][i]) > 0 and re.match(r'^[\d.]+$', data1['text'][i].strip()):
                    text = re.sub(r'\W', '', data1['text'][i])
                    if text:
                        if int(text) >= 100:
                            x, y, w, h = data1['left'][i], data1['top'][i], data1['width'][i], data1['height'][i]
                            x_center = int((2 * x + w) / 2)
                            y_center = int((2 * y + h) / 2)

                            selected_lines1.append((text, x_center, y_center))

            if len(selected_lines1) >= 2:
                selected_lines1.sort(key=lambda line: abs(line[1] - intersection_x))
                file.write("text: {}, coordinate: ({}, {})".format(selected_lines1[0][0], intersection_x,
                                                             selected_lines1[0][2]) + "\n")
                file.write("text: {}, coordinate: ({}, {})".format(selected_lines1[1][0], intersection_x,
                                                             selected_lines1[1][2]) + "\n")
                Py = abs((float(selected_lines1[0][0]) - float(selected_lines1[1][0])) / (
                    selected_lines1[0][2] - selected_lines1[1][2]))
                file.write("Py: {:.6f}".format(Py))


            file.write("\nhorizontal axis point：" + "\n")
            selected_lines2 = []
            for i in range(num_blocks2):
                if int(data2['conf'][i]) > 0:
                    x, y, w, h = data2['left'][i], data2['top'][i], data2['width'][i], data2['height'][i]
                    text = data2['text'][i]
                    if re.match(r'^[\d.]+$', text.strip()):
                        x += intersection_x
                        y += intersection_y
                        if text.startswith("0") and "." not in text:
                          text = "0." + text[1:]
                        if text.count('.') <= 1:
                          selected_lines2.append((text, int((2 * x + w) / 2), int((2 * y + h) / 2)))

            if len(selected_lines2) >= 2:
                selected_lines2.sort(key=lambda line: (abs(line[2] - intersection_y), line[0].count('0')))
                file.write("text: {}, coordinate: ({}, {})".format(selected_lines2[0][0], selected_lines2[0][1],
                                                             intersection_y) + "\n")
                file.write("text: {}, coordinate: ({}, {})".format(selected_lines2[1][0], selected_lines2[1][1],
                                                             intersection_y) + "\n")

                Px = abs((float(selected_lines2[0][0]) - float(selected_lines2[1][0])) / (
                        selected_lines2[0][1] - selected_lines2[1][1]))
                file.write("Px: {:.6f}".format(Px))
            elif len(selected_lines2) == 1:
                file.write("text: {}, coordinate: ({}, {})".format(selected_lines2[0][0], selected_lines2[0][1],
                                                             intersection_y) + "\n")

    else:
        print("No intersection point found for {}.".format(image_file))

    # 输出成功保存
    print("save to：{}".format(result_path))
